# Copyright The Plasma Project.
# See LICENSE.txt for details.

"""
Plasma utility classes and helper functions.
"""

import pyamf


class Constant(object):
    """
    Represents a combination of a value and a docstring for use in defining
    constants in classes. E.g.::

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

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return repr(self.value)


def to_amf(obj, encoder):
    return obj.value


pyamf.add_type(Constant, to_amf)
