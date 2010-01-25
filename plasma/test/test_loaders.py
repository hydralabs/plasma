# Copyright The Plasma Project.
# See LICENSE.txt for details.

"""
Plasma utility classes and helper functions.
"""

import unittest

import plasma
import pyamf


class ClassCacheTestCase(unittest.TestCase):
    """
    Clears out (and restores) all aliased classes
    """

    def setUp(self):
        self.old_class_cache = pyamf.CLASS_CACHE.copy()
        pyamf.CLASS_CACHE = {}

    def tearDown(self):
        pyamf.CLASS_CACHE = self.old_class_cache


class FlexLoaderTestCase(ClassCacheTestCase):
    """
    Tests for `plasma.flex_loader`
    """

    def test_not_aliased(self):
        for x in ['foo', 'flex.foo.bar', 'flex.messaging.foo']:
            self.assertRaises(pyamf.UnknownClassAlias, pyamf.get_class_alias, x)

    def test_aliased(self):
        alias = pyamf.get_class_alias('flex.messaging.messages.RemotingMessage')

        self.assertTrue(alias.klass.__module__.startswith(plasma.__name__))


class BlazeLoaderTestCase(ClassCacheTestCase):
    """
    Tests for `plasma.blaze_loader`
    """

    def test_not_aliased(self):
        for x in ['foo']:
            self.assertRaises(pyamf.UnknownClassAlias, pyamf.get_class_alias, x)

    def test_aliased(self):
        for x in ['DSC', 'DSK', 'DSC']:
            alias = pyamf.get_class_alias(x)

            self.assertTrue(alias.klass.__module__.startswith(plasma.__name__))
