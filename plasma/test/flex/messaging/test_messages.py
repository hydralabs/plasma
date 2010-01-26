# -*- coding: utf-8 -*-
#
# Copyright The Plasma Project.
# See LICENSE.txt for details.

"""
Flex Messaging compatibility tests.

.. versionadded:: 0.1

"""

import unittest
import datetime
import uuid

import pyamf

from plasma.flex.messaging import messages


class AbstractMessageTestCase(unittest.TestCase):
    """
    Tests for :class:`messages.AbstractMessage`
    """

    def test_create(self):
        a = messages.AbstractMessage()

        self.assertEquals(a.body, None)
        self.assertEquals(a.timestamp, None)
        self.assertEquals(a.destination, None)
        self.assertEquals(a.clientId, None)
        self.assertEquals(a.headers, {})
        self.assertEquals(a.timeToLive, None)
        self.assertEquals(a.messageId, None)

    def test_kwargs(self):
        a = messages.AbstractMessage(body=[], timestamp='foo', clientId='baz',
            destination='bar', headers='gak', timeToLive='spam',
            messageId='eggs', python='cool')

        self.assertEquals(a.body, [])
        self.assertEquals(a.timestamp, 'foo')
        self.assertEquals(a.destination, 'bar')
        self.assertEquals(a.clientId, 'baz')
        self.assertEquals(a.headers, 'gak')
        self.assertEquals(a.timeToLive, 'spam')
        self.assertEquals(a.messageId, 'eggs')

        self.assertFalse(hasattr(a, 'python'))

    def test_repr(self):
        a = messages.AbstractMessage()

        a.body = u'é,è'

        self.assertEquals(repr(a), "<AbstractMessage body=u'\\xe9,\\xe8' "
            "clientId=None destination=None headers={} messageId=None "
            "timestamp=None timeToLive=None />")


class AsyncMessageTestCase(unittest.TestCase):
    """
    Tests for :class:`messages.AsyncMessage`
    """

    def test_init(self):
        a = messages.AsyncMessage()

        self.assertEquals(a.body, None)
        self.assertEquals(a.timestamp, None)
        self.assertEquals(a.destination, None)
        self.assertEquals(a.clientId, None)
        self.assertEquals(a.headers, {})
        self.assertEquals(a.timeToLive, None)
        self.assertEquals(a.messageId, None)
        self.assertEquals(a.correlationId, None)

    def test_alias(self):
        alias = pyamf.get_class_alias(messages.AsyncMessage)

        alias.compile()

        self.assertTrue(alias.sealed)
        self.assertFalse(alias.dynamic)
        self.assertFalse(alias.external)

        self.assertEquals(alias.static_attrs, ['body', 'clientId',
            'correlationId', 'destination', 'headers', 'messageId',
            'timeToLive', 'timestamp'])


class AcknowledgeMessageTestCase(unittest.TestCase):
    """
    Tests for :class:`messages.AcknowledgeMessage`
    """

    def test_init(self):
        a = messages.AcknowledgeMessage()

        self.assertEquals(a.body, None)
        self.assertEquals(a.timestamp, None)
        self.assertEquals(a.destination, None)
        self.assertEquals(a.clientId, None)
        self.assertEquals(a.headers, {})
        self.assertEquals(a.timeToLive, None)
        self.assertEquals(a.messageId, None)
        self.assertEquals(a.correlationId, None)

    def test_kwargs(self):
        a = messages.AcknowledgeMessage(foo='bar')

        self.assertFalse(hasattr(a, 'foo'))

    def test_alias(self):
        alias = pyamf.get_class_alias(messages.AcknowledgeMessage)

        alias.compile()

        self.assertTrue(alias.sealed)
        self.assertFalse(alias.dynamic)
        self.assertFalse(alias.external)

        self.assertEquals(alias.static_attrs, ['body', 'clientId',
            'correlationId', 'destination', 'headers', 'messageId',
            'timeToLive', 'timestamp'])


class CommandMessageTestCase(unittest.TestCase):
    """
    Tests for :class:`messages.CommandMessage`
    """

    def test_init(self):
        a = messages.CommandMessage()

        self.assertEquals(a.body, None)
        self.assertEquals(a.timestamp, None)
        self.assertEquals(a.destination, None)
        self.assertEquals(a.clientId, None)
        self.assertEquals(a.headers, {})
        self.assertEquals(a.timeToLive, None)
        self.assertEquals(a.messageId, None)
        self.assertEquals(a.correlationId, None)
        self.assertEquals(a.operation, 10000)

    def test_kwargs(self):
        a = messages.CommandMessage(operation='yippee', foo='bar')

        self.assertEquals(a.operation, 'yippee')
        self.assertFalse(hasattr(a, 'foo'))

    def test_alias(self):
        alias = pyamf.get_class_alias(messages.CommandMessage)

        alias.compile()

        self.assertTrue(alias.sealed)
        self.assertFalse(alias.dynamic)
        self.assertFalse(alias.external)

        self.assertEquals(alias.static_attrs, ['body', 'clientId',
            'correlationId', 'destination', 'headers', 'messageId',
            'operation', 'timeToLive', 'timestamp'])


class ErrorMessageTestCase(unittest.TestCase):
    """
    Tests for :class:`messages.ErrorMessage`
    """

    def test_init(self):
        a = messages.ErrorMessage()

        self.assertEquals(a.body, None)
        self.assertEquals(a.timestamp, None)
        self.assertEquals(a.destination, None)
        self.assertEquals(a.clientId, None)
        self.assertEquals(a.headers, {})
        self.assertEquals(a.timeToLive, None)
        self.assertEquals(a.messageId, None)
        self.assertEquals(a.correlationId, None)

        self.assertEquals(a.extendedData, {})
        self.assertEquals(a.faultCode, None)
        self.assertEquals(a.faultDetail, None)
        self.assertEquals(a.faultString, None)
        self.assertEquals(a.rootCause, {})

    def test_kwargs(self):
        a = messages.ErrorMessage(extendedData='foo', faultCode='bar',
            faultDetail='baz', faultString='gak', rootCause='spam', foo='bar')

        self.assertEquals(a.extendedData, 'foo')
        self.assertEquals(a.faultCode, 'bar')
        self.assertEquals(a.faultDetail, 'baz')
        self.assertEquals(a.faultString, 'gak')
        self.assertEquals(a.rootCause, 'spam')
        self.assertFalse(hasattr(a, 'foo'))

    def test_alias(self):
        alias = pyamf.get_class_alias(messages.ErrorMessage)

        alias.compile()

        self.assertTrue(alias.sealed)
        self.assertFalse(alias.dynamic)
        self.assertFalse(alias.external)

        self.assertEquals(alias.static_attrs, ['body', 'clientId',
            'correlationId', 'destination', 'extendedData', 'faultCode',
            'faultDetail', 'faultString', 'headers', 'messageId', 'rootCause',
            'timeToLive', 'timestamp'])


class RemotingMessageTestCase(unittest.TestCase):
    """
    Tests for :class:`messages.RemotingMessage`
    """

    def test_init(self):
        a = messages.RemotingMessage()

        self.assertEquals(a.body, None)
        self.assertEquals(a.timestamp, None)
        self.assertEquals(a.destination, None)
        self.assertEquals(a.clientId, None)
        self.assertEquals(a.headers, {})
        self.assertEquals(a.timeToLive, None)
        self.assertEquals(a.messageId, None)

        self.assertEquals(a.operation, None)
        self.assertEquals(a.source, None)

    def test_kwargs(self):
        a = messages.RemotingMessage(operation='foo', source='bar', foo='bar')

        self.assertEquals(a.operation, 'foo')
        self.assertEquals(a.source, 'bar')
        self.assertFalse(hasattr(a, 'foo'))

    def test_alias(self):
        alias = pyamf.get_class_alias(messages.RemotingMessage)

        alias.compile()

        self.assertTrue(alias.sealed)
        self.assertFalse(alias.dynamic)
        self.assertFalse(alias.external)

        self.assertEquals(alias.static_attrs, ['body', 'clientId',
            'destination', 'headers', 'messageId', 'operation', 'source',
            'timeToLive', 'timestamp'])


class EncodingTestCase(unittest.TestCase):
    """
    Encoding tests for :mod:`messages`
    """

    def test_AsyncMessage(self):
        m = messages.AsyncMessage()
        m.correlationId = '1234'

        self.assertEquals(pyamf.encode(m, encoding=pyamf.AMF3).getvalue(),
            '\n\x81\x03Iflex.messaging.messages.AsyncMessage\tbody'
            '\x11clientId\x1bcorrelationId\x17destination\x0fheaders\x13'
            'messageId\x15timeToLive\x13timestamp\x01\x01\x06\t1234\x01\n\x0b'
            '\x01\x01\x01\x01\x01')

    def test_AcknowledgeMessage(self):
        m = messages.AcknowledgeMessage()
        m.correlationId = '1234'

        self.assertEquals(pyamf.encode(m, encoding=pyamf.AMF3).getvalue(),
            '\n\x81\x03Uflex.messaging.messages.AcknowledgeMessage\tbody'
            '\x11clientId\x1bcorrelationId\x17destination\x0fheaders\x13'
            'messageId\x15timeToLive\x13timestamp\x01\x01\x06\t1234\x01\n\x0b'
            '\x01\x01\x01\x01\x01')

    def test_CommandMessage(self):
        m = messages.CommandMessage(operation='foo.bar')

        self.assertEquals(pyamf.encode(m, encoding=pyamf.AMF3).getvalue(),
            '\n\x81\x13Mflex.messaging.messages.CommandMessage\tbody\x11'
            'clientId\x1bcorrelationId\x17destination\x0fheaders\x13messageId'
            '\x13operation\x15timeToLive\x13timestamp\x01\x01\x01\x01\n\x0b'
            '\x01\x01\x01\x06\x0ffoo.bar\x01\x01')

    def test_ErrorMessage(self):
        m = messages.ErrorMessage(faultString='ValueError')

        self.assertEquals(pyamf.encode(m, encoding=pyamf.AMF3).getvalue(),
            '\n\x81SIflex.messaging.messages.ErrorMessage\tbody\x11'
            'clientId\x1bcorrelationId\x17destination\x19extendedData\x13'
            'faultCode\x17faultDetail\x17faultString\x0fheaders\x13messageId'
            '\x13rootCause\x15timeToLive\x13timestamp\x01\x01\x01\x01\n\x0b'
            '\x01\x01\x01\x01\x06\x15ValueError\n\x05\x01\x01\n\x05\x01\x01'
            '\x01')

    def test_RemotingMessage(self):
        m = messages.RemotingMessage(source='foo.bar')

        self.assertEquals(pyamf.encode(m).getvalue(),
            '\n\x81\x13Oflex.messaging.messages.RemotingMessage'
            '\tbody\x11clientId\x17destination\x0fheaders\x13messageId\x13'
            'operation\rsource\x15timeToLive\x13timestamp\x01\x01\x01\n\x0b'
            '\x01\x01\x01\x01\x06\x0ffoo.bar\x01\x01')
