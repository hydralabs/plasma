# -*- coding: utf-8 -*-
#
# Copyright The Plasma Project.
# See LICENSE.txt for details.

"""
Flex Data Messaging compatibility tests.

.. versionadded:: 0.1
"""

import unittest

import pyamf

from plasma.flex.data import messages
from plasma.test import util


class DataMessageTestCase(unittest.TestCase):
    """
    Tests for :class:`messages.DataMessage`
    """

    def test_alias(self):
        alias = pyamf.get_class_alias(messages.DataMessage)

        alias.compile()

        self.assertTrue(alias.sealed)
        self.assertFalse(alias.dynamic)

        self.assertEquals(alias.static_attrs, [
            'body', 'clientId', 'correlationId', 'destination', 'headers',
            'identity', 'messageId', 'operation', 'timeToLive', 'timestamp'])

    def test_create(self):
        m = messages.DataMessage()

        self.assertEquals(m.body, None)
        self.assertEquals(m.timestamp, None)
        self.assertEquals(m.destination, None)
        self.assertEquals(m.clientId, None)
        self.assertEquals(m.headers, {})
        self.assertEquals(m.timeToLive, None)
        self.assertEquals(m.messageId, None)
        self.assertEquals(m.operation, None)
        self.assertEquals(m.identity, None)

        m = messages.DataMessage(operation='foo', identity='bar', spam='eggs')

        self.assertFalse(hasattr(m, 'spam'))
        self.assertEquals(m.body, None)
        self.assertEquals(m.timestamp, None)
        self.assertEquals(m.destination, None)
        self.assertEquals(m.clientId, None)
        self.assertEquals(m.headers, {})
        self.assertEquals(m.timeToLive, None)
        self.assertEquals(m.messageId, None)
        self.assertEquals(m.operation, 'foo')
        self.assertEquals(m.identity, 'bar')

    def test_amf(self):
        kwargs = {
            'body': ['foo'],
            'timestamp': 'bar',
            'destination': 'baz',
            'clientId': 'gak',
            'headers': {'blarg': 'nah'},
            'timeToLive': 103,
            'messageId': 'spam',
            'operation': 'eggs',
            'identity': 'blarg',
            'correlationId': '1234'
        }

        m = messages.DataMessage(**kwargs)

        bytes = pyamf.encode(m, encoding=pyamf.AMF3).getvalue()

        self.assertEquals(bytes, '\n\x81#=flex.data.messages.DataMessage'
            '\tbody\x11clientId\x1bcorrelationId\x17destination\x0fheaders'
            '\x11identity\x13messageId\x13operation\x15timeToLive\x13'
            'timestamp\t\x03\x01\x06\x07foo\x06\x07gak\x06\t1234\x06\x07baz'
            '\n\x0b\x01\x0bblarg\x06\x07nah\x01\x06\x1e\x06\tspam\x06\teggs'
            '\x04g\x06\x07bar')

        m = pyamf.decode(bytes, encoding=pyamf.AMF3).next()

        self.assertTrue(isinstance(m, messages.DataMessage))
        self.assertEquals(util.dict_for_slots(m), kwargs)


class SequencedMessageTestCase(unittest.TestCase):
    """
    Tests for :class:`messages.SequencedMessage`
    """

    def test_alias(self):
        alias = pyamf.get_class_alias(messages.SequencedMessage)

        alias.compile()

        self.assertTrue(alias.sealed)
        self.assertFalse(alias.dynamic)

        self.assertEquals(alias.static_attrs, ['body', 'clientId',
            'correlationId', 'destination', 'headers', 'messageId',
            'sequenceId', 'sequenceSize', 'timeToLive', 'timestamp'])

    def test_create(self):
        m = messages.SequencedMessage()

        self.assertEquals(m.body, None)
        self.assertEquals(m.timestamp, None)
        self.assertEquals(m.destination, None)
        self.assertEquals(m.clientId, None)
        self.assertEquals(m.headers, {})
        self.assertEquals(m.timeToLive, None)
        self.assertEquals(m.messageId, None)
        self.assertEquals(m.sequenceId, None)
        self.assertEquals(m.sequenceSize, None)

        m = messages.SequencedMessage(sequenceId='foo', sequenceSize='bar', spam='eggs')

        self.assertFalse(hasattr(m, 'spam'))
        self.assertEquals(m.body, None)
        self.assertEquals(m.timestamp, None)
        self.assertEquals(m.destination, None)
        self.assertEquals(m.clientId, None)
        self.assertEquals(m.headers, {})
        self.assertEquals(m.timeToLive, None)
        self.assertEquals(m.messageId, None)
        self.assertEquals(m.sequenceId, 'foo')
        self.assertEquals(m.sequenceSize, 'bar')

    def test_amf(self):
        kwargs = {
            'body': ['foo'],
            'timestamp': 'bar',
            'destination': 'baz',
            'clientId': 'gak',
            'headers': {'blarg': 'nah'},
            'timeToLive': 103,
            'messageId': 'spam',
            'sequenceId': 'eggs',
            'sequenceSize': 'blarg',
            'correlationId': '1234'
        }

        m = messages.SequencedMessage(**kwargs)

        bytes = pyamf.encode(m, encoding=pyamf.AMF3).getvalue()

        self.assertEquals(bytes, '\n\x81#Gflex.data.messages.SequencedMessage'
            '\tbody\x11clientId\x1bcorrelationId\x17destination\x0fheaders'
            '\x13messageId\x15sequenceId\x19sequenceSize\x15timeToLive\x13'
            'timestamp\t\x03\x01\x06\x07foo\x06\x07gak\x06\t1234\x06\x07baz'
            '\n\x0b\x01\x0bblarg\x06\x07nah\x01\x06\tspam\x06\teggs\x06\x1e'
            '\x04g\x06\x07bar')

        m = pyamf.decode(bytes, encoding=pyamf.AMF3).next()

        self.assertTrue(isinstance(m, messages.SequencedMessage))
        self.assertEquals(util.dict_for_slots(m), kwargs)


class PagedMessageTestCase(unittest.TestCase):
    """
    Tests for :class:`messages.PagedMessage`
    """

    def test_alias(self):
        alias = pyamf.get_class_alias(messages.PagedMessage)

        alias.compile()

        self.assertTrue(alias.sealed)
        self.assertFalse(alias.dynamic)

        self.assertEquals(alias.static_attrs, ['body', 'clientId',
            'correlationId', 'destination', 'headers', 'messageId',
            'pageCount', 'pageIndex', 'sequenceId', 'sequenceSize',
            'timeToLive', 'timestamp'])

    def test_create(self):
        m = messages.PagedMessage()

        self.assertEquals(m.body, None)
        self.assertEquals(m.timestamp, None)
        self.assertEquals(m.destination, None)
        self.assertEquals(m.clientId, None)
        self.assertEquals(m.headers, {})
        self.assertEquals(m.timeToLive, None)
        self.assertEquals(m.messageId, None)
        self.assertEquals(m.sequenceId, None)
        self.assertEquals(m.sequenceSize, None)
        self.assertEquals(m.pageCount, None)
        self.assertEquals(m.pageIndex, None)

        m = messages.PagedMessage(sequenceId='foo', sequenceSize='bar',
            pageCount=3, pageIndex=123, spam='eggs')

        self.assertFalse(hasattr(m, 'spam'))
        self.assertEquals(m.body, None)
        self.assertEquals(m.timestamp, None)
        self.assertEquals(m.destination, None)
        self.assertEquals(m.clientId, None)
        self.assertEquals(m.headers, {})
        self.assertEquals(m.timeToLive, None)
        self.assertEquals(m.messageId, None)
        self.assertEquals(m.sequenceId, 'foo')
        self.assertEquals(m.sequenceSize, 'bar')
        self.assertEquals(m.pageCount, 3)
        self.assertEquals(m.pageIndex, 123)

    def test_amf(self):
        kwargs = {
            'body': ['foo'],
            'timestamp': 'bar',
            'destination': 'baz',
            'clientId': 'gak',
            'headers': {'blarg': 'nah'},
            'timeToLive': 103,
            'messageId': 'spam',
            'sequenceId': 'eggs',
            'sequenceSize': 'blarg',
            'correlationId': '1234',
            'pageCount': 123,
            'pageIndex': 3,
        }

        m = messages.PagedMessage(**kwargs)

        bytes = pyamf.encode(m, encoding=pyamf.AMF3).getvalue()

        self.assertEquals(bytes, '\n\x81C?flex.data.messages.PagedMessage'
            '\tbody\x11clientId\x1bcorrelationId\x17destination\x0fheaders'
            '\x13messageId\x13pageCount\x13pageIndex\x15sequenceId\x19'
            'sequenceSize\x15timeToLive\x13timestamp\t\x03\x01\x06\x07foo'
            '\x06\x07gak\x06\t1234\x06\x07baz\n\x0b\x01\x0bblarg\x06\x07nah'
            '\x01\x06\tspam\x04{\x04\x03\x06\teggs\x06"\x04g\x06\x07bar')

        m = pyamf.decode(bytes, encoding=pyamf.AMF3).next()

        self.assertTrue(isinstance(m, messages.PagedMessage))
        self.assertEquals(util.dict_for_slots(m), kwargs)

        self.assertEquals(util.dict_for_slots(m), kwargs)
