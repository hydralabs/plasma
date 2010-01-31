# Copyright (c) The Plasma Project.
# See LICENSE.txt for details.

"""
This module is the entry point to the message selectors implementation.
It provides a (mostly) BlazeDS compatible subset of the SQL92 expression
language that is used for message filtering.

.. seealso:: http://livedocs.adobe.com/blazeds/1/blazeds_devguide/help.html?content=messaging_6.html
"""

from ply.yacc import yacc
from ply.lex import lex

from plasma.flex.messaging.selector import sql92grammar, sql92lexer


_lexer = lex(module=sql92lexer)
_parser = yacc(module=sql92grammar, debug=None, write_tables=False)

def evaluate(expression, variables=None, log=None):
    """
    Evaluates the given SQL92 boolean expression using the given variables.

    ..note:: `BETWEEN` expressions only accept variables and number literals.

    :param expression: A BlazeDS-compatible SQL92 boolean expression
    :type expression: `str`
    :param variables: a dictionary of variables and their values
    :type variables: `dict`
    :param log: logger that receives debugging information
    :type log: :class:`logging.Logger`
    :return: result of the expression evaluation
    :rtype: `bool`
    """
    sql92grammar.local.variables = variables or {}
    return _parser.parse(expression, lexer=_lexer, debug=log)
