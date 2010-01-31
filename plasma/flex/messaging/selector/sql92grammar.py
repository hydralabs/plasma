# Copyright (c) The Plasma Project.
# See LICENSE.txt for details.

"""
Grammar definition for a subset of SQL92 expressions.
"""
import threading

from plasma.flex.messaging.selector.sql92lexer import tokens
from plasma.flex.messaging.selector import (ParseError, IncompatibleTypeError,
    UnknownVariableError)
from plasma.flex.messaging.selector.matcher import Matcher

local = threading.local()

precedence = (
    ('nonassoc', 'BETWEEN', 'LIKE'),
    ('left', 'AND', 'OR'),
    ('nonassoc', 'EQ', 'NEQ', 'GT', 'GTE', 'LT', 'LTE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'UMINUS')
)

def p_expression(p):
    """expression : NUMBER
                  | BOOLEAN
                  | STRING
                  | variable"""
    p[0] = p[1]


def p_equality(p):
    """expression : expression EQ expression
                  | expression NEQ expression"""
    if p[2] == '=':
        p[0] = p[1] == p[3]
    elif p[2] == '<>':
        p[0] = p[1] != p[3]


def p_binary_logical_operators(p):
    """expression : expression AND expression
                  | expression OR expression"""
    if not isinstance(p[1], bool) or not isinstance(p[3], bool):
        raise IncompatibleTypeError(
            u'%s requires boolean operands; got %s and %s' %
            (p[2], type(p[1]), type(p[3])))
    if p[2] == 'AND':
        p[0] = p[1] and p[3]
    elif p[2] == 'OR':
        p[0] = p[1] or p[3]


def p_between(p):
    """expression : expression BETWEEN between_expr AND between_expr \
                        %prec BETWEEN"""
    if (not isinstance(p[1], (int, long, float)) or
        not isinstance(p[3], (int, long, float)) or
        not isinstance(p[5], (int, long, float))):
        raise IncompatibleTypeError(u'BETWEEN only works with numbers')
    p[0] = p[1] >= p[3] and p[1] <= p[5]


def p_not_between(p):
    """expression : expression NOT BETWEEN between_expr AND between_expr \
                        %prec BETWEEN"""
    if (not isinstance(p[1], (int, long, float)) or
        not isinstance(p[4], (int, long, float)) or
        not isinstance(p[6], (int, long, float))):
        raise IncompatibleTypeError(u'BETWEEN only works with numbers')
    p[0] = p[1] < p[4] or p[1] > p[6]


def p_between_expr(p):
    """between_expr : variable
                    | NUMBER"""
    p[0] = p[1]


def p_is_null(p):
    """expression : VARIABLE IS NULL"""
    p[0] = p[1] not in local.variables


def p_is_not_null(p):
    """expression : VARIABLE IS NOT NULL"""
    p[0] = p[1] in local.variables


def p_binary_operators(p):
    """expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression"""
    if (not isinstance(p[1], (int, long, float)) or
        not isinstance(p[3], (int, long, float))):
        raise IncompatibleTypeError(
            '%s requires numeric operands; got %s and %s' %
            (p[2], type(p[1]), type(p[3])))
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]


def p_expr_uminus(p):
    """expression : MINUS expression %prec UMINUS"""
    if not isinstance(p[2], (int, long, float)):
        raise IncompatibleTypeError(u'Only numbers can be negated')
    p[0] = -p[2]


def p_num_comparisons(p):
    """expression : expression GT expression
                  | expression GTE expression
                  | expression LT expression
                  | expression LTE expression"""
    if (not isinstance(p[1], (int, long, float)) or
        not isinstance(p[3], (int, long, float))):
        raise IncompatibleTypeError(
            '%s requires numeric operands; got %s and %s' %
            (p[2], type(p[1]), type(p[3])))
    if p[2] == '>':
        p[0] = p[1] > p[3]
    elif p[2] == '>=':
        p[0] = p[1] >= p[3]
    elif p[2] == '<':
        p[0] = p[1] < p[3]
    elif p[2] == '<=':
        p[0] = p[1] <= p[3]


def p_in(p):
    """expression : expression IN '(' expression_list ')'"""
    p[0] = p[1] in p[4]


def p_not_in(p):
    """expression : expression NOT IN '(' expression_list ')'"""
    p[0] = p[1] not in p[5]


def p_expression_list(p):
    """expression_list : expression_list ',' expression
                       | expression"""
    if len(p) == 4:
        p[0] = p[1]
        p[0].append(p[3])
    else:
        p[0] = [p[1]]


def p_like(p):
    """expression : expression LIKE expression escapechar"""
    if (not isinstance(p[1], basestring) or
        not isinstance(p[3], basestring)):
        raise IncompatibleTypeError(
            'LIKE requires string operands; got %s and %s' %
            (type(p[1]), type(p[3])))
    p[0] = Matcher(p[1], p[3], p[4]).matches()


def p_not_like(p):
    """expression : expression NOT LIKE expression escapechar"""
    if (not isinstance(p[1], basestring) or
        not isinstance(p[4], basestring)):
        raise IncompatibleTypeError(
            'LIKE requires string operands; got %s and %s' %
            (type(p[1]), type(p[4])))
    p[0] = not Matcher(p[1], p[4], p[5]).matches()


def p_escapechar(p):
    """escapechar : ESCAPE STRING
                  |"""
    p[0] = p[2] if len(p) == 3 else '\\'


def p_parentheses(p):
    """expression  : '(' expression ')'"""
    p[0] = p[2]


def p_variable(p):
    """variable : VARIABLE"""
    try:
        p[0] = local.variables[p[1]]
    except KeyError:
        raise UnknownVariableError('Undefined variable: %s' % p[1])


# Error rule for syntax errors
def p_error(p):
    raise ParseError(u'Syntax error in input')
