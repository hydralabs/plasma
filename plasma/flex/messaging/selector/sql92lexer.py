# Copyright (c) The Plasma Project.
# See LICENSE.txt for details.

"""
Lexer for the SQL92 expressions grammar.
"""

from plasma.flex.messaging.selector import LexerError


literals = ('(', ')', ',')

reserved = ('AND', 'BETWEEN', 'IN', 'IS', 'LIKE', 'NOT', 'NULL', 'OR',
            'ESCAPE')

# List of token names.   This is always required
tokens = (
   'NUMBER',
   'STRING',
   'BOOLEAN',
   'VARIABLE',
   'PLUS',
   'MINUS',
   'TIMES',
   'DIVIDE',
   'GT',
   'GTE',
   'LT',
   'LTE',
   'EQ',
   'NEQ') + reserved

# Regular expression rules for simple tokens
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_GT      = r'>'
t_GTE     = r'>='
t_LT      = r'<'
t_LTE     = r'<='
t_EQ      = r'='
t_NEQ     = r'<>'

def t_HEXNUMBER(t):
    r'0x[0-9a-fA-F]+'
    t.type = 'NUMBER'
    t.value = long(t.value[2:], 16)
    return t


def t_NUMBER(t):
    r'(?P<main>\d*\.?\d+)([eE](?P<exponent>(\+|-)?\d+))?'
    main = t.lexer.lexmatch.group('main')
    exponent = t.lexer.lexmatch.group('exponent')
    t.value = float(main) if '.' in main else long(main)
    if exponent:
        t.value *= 10 ** int(exponent)
    return t


def t_STRING(t):
    r"'([^'\\]|\\.)*'"
    t.value = t.value[1:-1]
    return t


def t_BOOLEAN(t):
    r"(true|false)"
    t.value = (t.value == 'true')
    return t


def t_VAR(t):
    r"[a-zA-Z_][a-zA-Z0-9_]*"
    uval = t.value.upper()
    if uval in reserved:
        t.type = t.value = uval
    else:
        t.type = 'VARIABLE'
    return t

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t\r\n\f'

# Error handling rule
def t_error(t):
    raise LexerError(u"Illegal character '%s'" % t.value[0])
