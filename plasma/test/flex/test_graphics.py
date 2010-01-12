# -*- coding: utf-8 -*-
#
# Copyright (c) 2009 The Plasma Project.
# See LICENSE.txt for details.

"""
Tests for :mod:`plasma.flex.graphics`.

.. versionadded:: 0.1

"""

import unittest

import pyamf

from plasma.flex import graphics


class ImageSnapshotTestCase(unittest.TestCase):
    """Tests for :class:`graphics.ImageSnapshot`"""

    alias = 'flex.graphics.ImageSnapshot'

    def test_alias(self):
        alias = pyamf.get_class_alias(self.alias)

        self.assertIdentical(alias.klass, graphics.ImageSnapshot)

    def test_create(self):
        i = graphics.ImageSnapshot()

        self.assertEquals(i.__dict__, {
            'width': 0,
            'height': 0,
            'contentType': None,
            'properties': {},
            'data': None,
        })

    def test_kwargs(self):
        kwargs = {
            'width': 123,
            'height': 456,
            'contentType': 'image/png',
            'properties': {'foo': 'bar'},
            'data': 'a;osiejfawef',
        }

        i = graphics.ImageSnapshot(**kwargs)

        self.assertEquals(i.__dict__, kwargs)

        n = kwargs.copy()
        n.update({'foo': 'bar', 'baz': 'gak'})

        i = graphics.ImageSnapshot(**n)

        self.assertEquals(i.__dict__, kwargs)
