# -*- coding: utf-8 -*-
#
# Copyright (c) 2009 The Plasma Project.
# See LICENSE.txt for details.

"""
Flex compatibility tests.

.. versionadded:: 0.1

"""

import unittest

from plasma.flex.messaging import io
import pyamf
from pyamf import amf0, amf3


class ArrayListTestCase(unittest.TestCase):
    """
    Tests for :class:`io.ArrayList`
    """

    def test_create(self):
        self.assertEquals(io.ArrayList(), [])
        self.assertEquals(io.ArrayList([1, 2, 3]), [1, 2, 3])
        self.assertEquals(io.ArrayList(('a', 'b', 'b')), ['a', 'b', 'b'])

        class X(object):
            def __iter__(self):
                return iter(['foo', 'bar', 'baz'])

        self.assertEquals(io.ArrayList(X()), ['foo', 'bar', 'baz'])

        self.assertRaises(TypeError, io.ArrayList,
            {'first': 'Matt', 'last': 'Matthews'})

    def test_encode_amf3(self):
        x = io.ArrayList()
        x.append('eggs')

        stream = amf3.encode(x)

        self.assertEquals(stream.getvalue(),
            '\n\x077flex.messaging.io.ArrayList\t\x03\x01\x06\teggs')

    def test_decode_amf3(self):
        bytes = '\n\x077flex.messaging.io.ArrayList\t\x03\x01\x06\teggs'
        x = amf3.decode(bytes).next()

        self.assertEquals(x.__class__, io.ArrayList)
        self.assertEquals(x, ['eggs'])

    def test_decode_amf0(self):
        bytes = '\x11\n\x077flex.messaging.io.ArrayList\t\x03\x01\x06\teggs'
        x = amf0.decode(bytes).next()

        self.assertEquals(x.__class__, io.ArrayList)
        self.assertEquals(x, ['eggs'])

    def test_source_attr(self):
        s = ('\n\x077flex.messaging.io.ArrayList\n\x0b\x01\rsource'
            '\t\x05\x01\x06\x07foo\x06\x07bar\x01')

        x = amf3.decode(s).next()

        self.assertTrue(isinstance(x, io.ArrayList))
        self.assertEquals(x, ['foo', 'bar'])

    def test_repr(self):
        a = io.ArrayList()
        b = io.ArrayList([1, 2, 3])
        c = io.ArrayList([u'∑œ', 'd'])

        class X(object):
            def __iter__(self):
                return iter(['foo', 'bar', 'baz'])

        d = io.ArrayList(X())

        self.assertEquals(repr(a), '<flex.messaging.io.ArrayList []>')
        self.assertEquals(repr(b),
            '<flex.messaging.io.ArrayList [1, 2, 3]>')
        self.assertEquals(repr(c),
            '<flex.messaging.io.ArrayList [u\'\\u2211\\u0153\', \'d\']>')
        self.assertEquals(repr(d),
            '<flex.messaging.io.ArrayList [\'foo\', \'bar\', \'baz\']>')

    def test_read_external_no_iterate(self):
        """
        Test to ensure an error is thrown if an object that cannot be iterated
        over is read from the stream.

        """
        class MockDataInput:
            def readObject(self):
                return object()

        a = io.ArrayList()
        self.assertRaises(pyamf.DecodeError, a.__readamf__, MockDataInput())

    def test_readonly_length(self):
        """Trying to set the length should cause an error."""
        a = io.ArrayList()

        self.assertRaises(AttributeError, setattr, a, 'length', 2)
