# Copyright (c) 2007-2009 The Plasma Project.
# See LICENSE.txt for details.

"""
Plasma utility classes and helper functions.
"""


class Constant(object):
    """
    Represents a combination of a value and a docstring for use in defining
    constants in classes. E.g.:

    class Foo(object):
        ENDPOINT_HEADER = Constant('DSEndpoint', 'The name for the endpoint header.')
    """

    def __init__(self, value, doc=None):
        self.value = value
        self.__doc__ = doc

    def __cmp__(self, other):
        return cmp(self.value, other)

    def __eq__(self, other):
        return self.value == other
