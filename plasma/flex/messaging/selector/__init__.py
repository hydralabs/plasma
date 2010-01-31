# Copyright (c) The Plasma Project.
# See LICENSE.txt for details.

class ParseError(Exception):
    """
    Raised when there is a problem parsing or evaluating a selector expression.
    """


class LexerError(ParseError):
    """
    Raised when the lexer receives invalid input.
    """


class IncompatibleTypeError(ParseError):
    """
    Raised when the parser receives operand(s) of wrong type for the current
    operation.
    """


class UnknownVariableError(ParseError):
    """
    Raised when the parser attempts to lookup a variable that does not
    exist in the symbol table.
    """
