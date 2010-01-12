# Copyright (c) 2007-2009 The Plasma Project.
# See LICENSE.txt for details.

"""Plasma utility classes and helper functions."""

import unittest

from plasma import util


class ConstantTestCase(unittest.TestCase):
    """Tests for :class:`util.Constant`"""

    def test_create(self):
        x = util.Constant('foo')

        self.assertEquals(x.value, 'foo')
        self.assertEquals(x.__doc__, None)

        x = util.Constant('foo', 'bar')

        self.assertEquals(x.value, 'foo')
        self.assertEquals(x.__doc__, 'bar')

    def test_cmp(self):
        x = util.Constant('foo')

        self.assertEquals(cmp(x, 'foo'), cmp('foo', 'foo'))
        self.assertEquals(cmp(x, 'fop'), cmp('foo', 'fop'))
        self.assertEquals(cmp(x, 'fon'), cmp('foo', 'fon'))

        self.assertFalse(x > 'foo')
        self.assertFalse(x < 'foo')

        self.assertFalse(x > 'fop')
        self.assertTrue(x < 'fop')

        self.assertTrue(x > 'fon')
        self.assertFalse(x < 'fon')

    def test_eq(self):
        x = util.Constant(23)

        self.assertTrue(x == 23)
        self.assertFalse(x != 23)

    def test_str(self):
        x = util.Constant('foo bar')
        self.assertEquals(str(x), 'foo bar')

        x = util.Constant(1234)
        self.assertEquals(str(x), '1234')

    def test_repr(self):
        x = util.Constant('foo bar')
        self.assertEquals(repr(x), "'foo bar'")

        x = util.Constant(1234)
        self.assertEquals(repr(x), '1234')
