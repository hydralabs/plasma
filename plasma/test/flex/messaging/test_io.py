# -*- coding: utf-8 -*-
#
# Copyright (c) 2009 The Plasma Project.
# See LICENSE.txt for details.

"""
Flex compatibility tests.

@since: 0.1
"""

import unittest

from plasma.flex.messaging import io
import pyamf
from pyamf import amf0, amf3


class ArrayCollectionTestCase(unittest.TestCase):
    """
    Tests for L{io.ArrayCollection}
    """

    def test_create(self):
        self.assertEquals(io.ArrayCollection(), [])
        self.assertEquals(io.ArrayCollection([1, 2, 3]), [1, 2, 3])
        self.assertEquals(io.ArrayCollection(('a', 'b', 'b')), ['a', 'b', 'b'])

        class X(object):
            def __iter__(self):
                return iter(['foo', 'bar', 'baz'])

        self.assertEquals(io.ArrayCollection(X()), ['foo', 'bar', 'baz'])

        self.assertRaises(TypeError, io.ArrayCollection,
            {'first': 'Matt', 'last': 'Matthews'})

    def test_encode_amf3(self):
        x = io.ArrayCollection()
        x.append('eggs')

        stream = amf3.encode(x)

        self.assertEquals(stream.getvalue(),
            '\n\x07Cflex.messaging.io.ArrayCollection\t\x03\x01\x06\teggs')

    def test_decode_amf3(self):
        bytes = '\n\x07Cflex.messaging.io.ArrayCollection\t\x03\x01\x06\teggs'
        x = amf3.decode(bytes).next()

        self.assertEquals(x.__class__, io.ArrayCollection)
        self.assertEquals(x, ['eggs'])

    def test_decode_amf0(self):
        bytes = '\x11\n\x07Cflex.messaging.io.ArrayCollection\t\x03\x01\x06\teggs'
        x = amf0.decode(bytes).next()

        self.assertEquals(x.__class__, io.ArrayCollection)
        self.assertEquals(x, ['eggs'])

    def test_source_attr(self):
        s = ('\n\x07Cflex.messaging.io.ArrayCollection\n\x0b\x01\rsource'
            '\t\x05\x01\x06\x07foo\x06\x07bar\x01')

        x = amf3.decode(s).next()

        self.assertTrue(isinstance(x, io.ArrayCollection))
        self.assertEquals(x, ['foo', 'bar'])

    def test_repr(self):
        a = io.ArrayCollection()
        b = io.ArrayCollection([1, 2, 3])
        c = io.ArrayCollection([u'∑œ', 'd'])

        class X(object):
            def __iter__(self):
                return iter(['foo', 'bar', 'baz'])

        d = io.ArrayCollection(X())

        self.assertEquals(repr(a), '<flex.messaging.io.ArrayCollection []>')
        self.assertEquals(repr(b),
            '<flex.messaging.io.ArrayCollection [1, 2, 3]>')
        self.assertEquals(repr(c),
            '<flex.messaging.io.ArrayCollection [u\'\\u2211\\u0153\', \'d\']>')
        self.assertEquals(repr(d),
            '<flex.messaging.io.ArrayCollection [\'foo\', \'bar\', \'baz\']>')

    def test_read_external_no_iterate(self):
        """
        Test to ensure an error is thrown if an object that cannot be iterated
        over is read from the stream.
        """
        class MockDataInput:
            def readObject(self):
                return object()

        a = io.ArrayCollection()
        self.assertRaises(pyamf.DecodeError, a.__readamf__, MockDataInput())

    def test_readonly_length(self):
        """
        Trying to set the length should cause an error
        """
        a = io.ArrayCollection()

        self.assertRaises(AttributeError, setattr, a, 'length', 2)


class ArrayCollectionAPITestCase(unittest.TestCase):
    def test_addItem(self):
        a = io.ArrayCollection()
        self.assertEquals(a, [])
        self.assertEquals(a.length, 0)

        a.addItem('hi')
        self.assertEquals(a, ['hi'])
        self.assertEquals(a.length, 1)

    def test_addItemAt(self):
        a = io.ArrayCollection()
        self.assertEquals(a, [])

        self.assertRaises(IndexError, a.addItemAt, 'foo', -1)
        self.assertRaises(IndexError, a.addItemAt, 'foo', 1)

        a.addItemAt('foo', 0)
        self.assertEquals(a, ['foo'])
        a.addItemAt('bar', 0)
        self.assertEquals(a, ['bar', 'foo'])
        self.assertEquals(a.length, 2)

    def test_getItemAt(self):
        a = io.ArrayCollection(['a', 'b', 'c'])

        self.assertEquals(a.getItemAt(0), 'a')
        self.assertEquals(a.getItemAt(1), 'b')
        self.assertEquals(a.getItemAt(2), 'c')

        self.assertRaises(IndexError, a.getItemAt, -1)
        self.assertRaises(IndexError, a.getItemAt, 3)
        self.assertRaises(IndexError, a.getItemAt, 4)

    def test_getItemIndex(self):
        a = io.ArrayCollection(['a', 'b', 'c'])

        self.assertEquals(a.getItemIndex('a'), 0)
        self.assertEquals(a.getItemIndex('b'), 1)
        self.assertEquals(a.getItemIndex('c'), 2)
        self.assertEquals(a.getItemIndex('d'), -1)

    def test_removeAll(self):
        a = io.ArrayCollection(['a', 'b', 'c'])
        self.assertEquals(a.length, 3)

        a.removeAll()

        self.assertEquals(a, [])
        self.assertEquals(a.length, 0)

    def test_removeItemAt(self):
        a = io.ArrayCollection(['a', 'b', 'c'])

        self.assertRaises(IndexError, a.removeItemAt, -1)
        self.assertRaises(IndexError, a.removeItemAt, 3)
        self.assertRaises(IndexError, a.removeItemAt, 4)

        self.assertEquals(a.removeItemAt(1), 'b')
        self.assertEquals(a, ['a', 'c'])
        self.assertEquals(a.length, 2)
        self.assertEquals(a.removeItemAt(1), 'c')
        self.assertEquals(a, ['a'])
        self.assertEquals(a.length, 1)
        self.assertEquals(a.removeItemAt(0), 'a')
        self.assertEquals(a, [])
        self.assertEquals(a.length, 0)

    def test_setItemAt(self):
        a = io.ArrayCollection(['a', 'b', 'c'])

        self.assertRaises(IndexError, a.setItemAt, -1, -1)
        self.assertRaises(IndexError, a.setItemAt, -1, 4)

        self.assertEquals(a.setItemAt('d', 1), 'b')
        self.assertEquals(a, ['a', 'd', 'c'])
        self.assertEquals(a.length, 3)

    def test_toArray(self):
        a = io.ArrayCollection(['a', 'b', 'c'])

        self.assertEquals(a.toArray(), a)


class ObjectProxyTestCase(unittest.TestCase):
    """
    Tests for L{io.ObjectProxy}
    """

    def test_encode(self):
        x = io.ObjectProxy(dict(a='spam', b=5))

        stream = amf3.encode(x)

        self.assertEquals(stream.getvalue(), '\n\x07;flex.messaging.io.'
            'ObjectProxy\n\x0b\x01\x03a\x06\tspam\x03b\x04\x05\x01')

    def test_decode(self):
        x = amf3.decode('\x0a\x07;flex.messaging.io.ObjectProxy\x09\x01\x03a'
            '\x06\x09spam\x03b\x04\x05\x01').next()

        self.assertEquals(x.__class__, io.ObjectProxy)
        self.assertEquals(x._amf_object, {'a': 'spam', 'b': 5})

    def test_get_attrs(self):
        x = io.ObjectProxy()

        self.assertEquals(x._amf_object, {})

        x._amf_object = None
        self.assertEquals(x._amf_object, None)

        y = pyamf.ASObject()
        y.foo = 'foo'
        y.bar = 'bar'

        x._amf_object = y

        self.assertEquals(getattr(x, 'foo'), 'foo')
        self.assertEquals(getattr(x, 'bar'), 'bar')
        self.assertEquals(getattr(x, '_amf_object'), y)

    def test_repr(self):
        a = io.ObjectProxy(u'∆∑')

        self.assertEquals(repr(a), "<flex.messaging.io.ObjectProxy u'\u2206\u2211'>")


class ArrayListTestCase(unittest.TestCase):
    """
    Tests for L{io.ArrayList}
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
        """
        Trying to set the length should cause an error
        """
        a = io.ArrayList()

        self.assertRaises(AttributeError, setattr, a, 'length', 2)


class UnproxyTestCase(unittest.TestCase):
    """
    Tests for L{io.unproxy_object}
    """

    def test_objectproxy(self):
        x = {'foo': 'foo', 'bar': 'bar'}

        a = io.ObjectProxy(x)

        self.assertEquals(io.unproxy_object(a), x)

    def test_arraycollection(self):
        x = [1, 2, 3]

        a = io.ArrayCollection(x)

        self.assertEquals(io.unproxy_object(a), x)

    def test_other(self):
        x = [1, 2, 3]

        self.assertEquals(io.unproxy_object(x), x)
