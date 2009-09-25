# -*- coding: utf-8 -*-
#
# Copyright (c) 2009 The Plasma Project.
# See LICENSE.txt for details.

"""
Flex Messaging compatibility tests.

@since: 0.1
"""

import unittest
import datetime
import uuid

import pyamf

from plasma.flex.messaging import messages


class AbstractMessageTestCase(unittest.TestCase):
    """
    Tests for L{messages.AbstractMessage}
    """

    def test_create(self):
        a = messages.AbstractMessage()

        self.assertEquals(a.__dict__, {
            'body': None,
            'timestamp': None,
            'destination': None,
            'clientId': None,
            'headers': {},
            'timeToLive': None,
            'messageId': None
        })

    def test_kwargs(self):
        a = messages.AbstractMessage(body=[], timestamp='foo', clientId='baz',
            destination='bar', headers='gak', timeToLive='spam',
            messageId='eggs', python='cool')

        self.assertEquals(a.__dict__, {
            'body': [],
            'timestamp': 'foo',
            'destination': 'bar',
            'clientId': 'baz',
            'headers': 'gak',
            'timeToLive': 'spam',
            'messageId': 'eggs'
        })

    def test_repr(self):
        a = messages.AbstractMessage()

        a.body = u'é,è'

        repr(a)

    def test_too_many_flags(self):
        """
        Test to check that if more than 2 flags are received in __readamf__
        an error will be thrown.
        """
        class Mock:
            b = [0x80, 0x80, 0x02]

            def __init__(self):
                self.i = iter(self.b)

            def readUnsignedByte(self):
                return self.i.next()

            def readObject(self):
                return {}

        a = messages.AbstractMessage()

        self.assertRaises(pyamf.DecodeError, a.__readamf__, Mock())


class AsyncMessageTestCase(unittest.TestCase):
    """
    Tests for L{messages.AsyncMessage}
    """

    def test_too_many_flags(self):
        """
        Test to check that if more than 2 flags are received in __readamf__
        an error will be thrown.
        """
        class Mock:
            b = [0x80, 0x00, 0x80, 0x00]

            def __init__(self):
                self.i = iter(self.b)

            def readUnsignedByte(self):
                return self.i.next()

            def readObject(self):
                return {}

        a = messages.AsyncMessage()

        self.assertRaises(pyamf.DecodeError, a.__readamf__, Mock())


class AcknowledgeMessageTestCase(unittest.TestCase):
    """
    Tests for L{messages.AcknowledgeMessage}
    """

    def test_too_many_flags(self):
        """
        Test to check that if more than 2 flags are received in __readamf__
        an error will be thrown.
        """
        class Mock:
            b = [0x80, 0x00, 0x00, 0x80, 0x00]

            def __init__(self):
                self.i = iter(self.b)

            def readUnsignedByte(self):
                return self.i.next()

            def readObject(self):
                return {}

        a = messages.AcknowledgeMessage()

        self.assertRaises(pyamf.DecodeError, a.__readamf__, Mock())


class CommandMessageTestCase(unittest.TestCase):
    """
    Tests for L{messages.CommandMessage}
    """

    def test_too_many_flags(self):
        """
        Test to check that if more than 2 flags are received in __readamf__
        an error will be thrown.
        """
        class Mock:
            b = [0x80, 0x00, 0x00, 0x80, 0x00]

            def __init__(self):
                self.i = iter(self.b)

            def readUnsignedByte(self):
                return self.i.next()

            def readObject(self):
                return {}

        a = messages.CommandMessage()

        self.assertRaises(pyamf.DecodeError, a.__readamf__, Mock())

    def test_flags_no_operation(self):
        """
        Test to ensure that 0 is written for the command flag when operation
        is C{None}
        """
        class MockDataOutput:
            written = []

            def writeUnsignedByte(self, byte):
                self.written.append(byte)

            def writeObject(self, object):
                self.written.append(object)

        a = messages.CommandMessage()
        b = MockDataOutput()

        self.assertEquals(a.operation, None)

        a.__writeamf__(b)

        self.assertEquals(b.written, [0, 1, None, 0])


class EncodingTestCase(unittest.TestCase):
    """
    Encoding tests for L{messages}
    """

    def test_AcknowledgeMessage(self):
        m = messages.AcknowledgeMessage()
        m.correlationId = '1234'

        self.assertEquals(pyamf.encode(m).getvalue(),
            '\x11\n\x81\x03Uflex.messaging.messages.AcknowledgeMessage\tbody'
            '\x11clientId\x1bcorrelationId\x17destination\x0fheaders\x13'
            'messageId\x15timeToLive\x13timestamp\x01\x01\x06\t1234\x01\n\x0b'
            '\x01\x01\x01\x01\x01')

    def test_CommandMessage(self):
        m = messages.CommandMessage(operation='foo.bar')

        self.assertEquals(pyamf.encode(m).getvalue(),
            '\x11\n\x81\x13Mflex.messaging.messages.CommandMessage\tbody\x11'
            'clientId\x1bcorrelationId\x17destination\x0fheaders\x13messageId'
            '\x13operation\x15timeToLive\x13timestamp\x01\x01\x01\x01\n\x0b'
            '\x01\x01\x01\x06\x0ffoo.bar\x01\x01')

    def test_ErrorMessage(self):
        m = messages.ErrorMessage(faultString='ValueError')

        self.assertEquals(pyamf.encode(m).getvalue(),
            '\x11\n\x81SIflex.messaging.messages.ErrorMessage\tbody\x11'
            'clientId\x1bcorrelationId\x17destination\x19extendedData\x13'
            'faultCode\x17faultDetail\x17faultString\x0fheaders\x13messageId'
            '\x13rootCause\x15timeToLive\x13timestamp\x01\x01\x01\x01\n\x0b'
            '\x01\x01\x01\x01\x06\x15ValueError\n\x05\x01\x01\n\x05\x01\x01'
            '\x01')

    def test_RemotingMessage(self):
        m = messages.RemotingMessage(source='foo.bar')

        self.assertEquals(pyamf.encode(m).getvalue(),
            '\x11\n\x81\x13Oflex.messaging.messages.RemotingMessage'
            '\tbody\x11clientId\x17destination\x0fheaders\x13messageId\x13'
            'operation\rsource\x15timeToLive\x13timestamp\x01\x01\x01\n\x0b'
            '\x01\x01\x01\x01\x06\x0ffoo.bar\x01\x01')


class SmallMessageTestCase(unittest.TestCase):
    """
    Tests for L{messages.SmallMessageMixIn}
    """

    def setUp(self):
        self.decoder = pyamf.get_decoder(pyamf.AMF3)
        self.buffer = self.decoder.stream

    def test_acknowledge(self):
        bytes = ('\n\x07\x07DSK\xa8\x03\n\x0b\x01%DSMessagingVersion\x05?\xf0'
            '\x00\x00\x00\x00\x00\x00\tDSId\x06IEE0D161D-C11D-25CB-8DBE-3B77B'
            '54B55D9\x01\x05Br3&m\x85\x10\x00\x0c!\xee\r\x16\x1d\xc1(&[\xc9'
            '\x80RK\x9bE\xc6\xc4\x0c!\xee\r\x16\x1d\xc1=\x8e\xa3\xe0\x10\xef'
            '\xad;\xe5\xc5j\x02\x0c!S\x84\x83\xdb\xa9\xc8\xcaM`\x952f\xdbQ'
            '\xc9<\x00')
        self.buffer.write(bytes)
        self.buffer.seek(0)

        msg = self.decoder.readElement()

        self.assertTrue(isinstance(msg, messages.AcknowledgeMessageExt))
        self.assertEquals(msg.body, None)
        self.assertEquals(msg.destination, None)
        self.assertEquals(msg.timeToLive, None)

        self.assertEquals(msg.timestamp,
            datetime.datetime(2009, 8, 19, 11, 24, 43, 985000))
        self.assertEquals(msg.headers, {
            'DSMessagingVersion': 1.0,
            'DSId': u'EE0D161D-C11D-25CB-8DBE-3B77B54B55D9'
        })
        self.assertEquals(msg.clientId,
            uuid.UUID('ee0d161d-c128-265b-c980-524b9b45c6c4'))
        self.assertEquals(msg.messageId,
            uuid.UUID('ee0d161d-c13d-8ea3-e010-efad3be5c56a'))
        self.assertEquals(msg.correlationId,
            uuid.UUID('538483db-a9c8-ca4d-6095-3266db51c93c'))
        self.assertEquals(self.buffer.remaining(), 0)

        # now encode the msg to check that encoding is byte for byte the same
        buffer = pyamf.encode(msg, encoding=pyamf.AMF3).getvalue()

        self.assertEquals(buffer, bytes)

    def test_command(self):
        bytes = ('\n\x07\x07DSC\x88\x02\n\x0b\x01\tDSId\x06IEE0D161D-C11D-'
            '25CB-8DBE-3B77B54B55D9\x01\x0c!\xc0\xdf\xb7|\xd6\xee$1s\x152f'
            '\xe11\xa8f\x01\x06\x01\x01\x04\x02')

        self.buffer.write(bytes)
        self.buffer.seek(0)

        msg = self.decoder.readElement()

        self.assertTrue(isinstance(msg, messages.CommandMessageExt))
        self.assertEquals(msg.body, None)
        self.assertEquals(msg.destination, None)
        self.assertEquals(msg.timeToLive, None)

        self.assertEquals(msg.timestamp, None)
        self.assertEquals(msg.headers, {
            'DSId': u'EE0D161D-C11D-25CB-8DBE-3B77B54B55D9'
        })
        self.assertEquals(msg.clientId, None)
        self.assertEquals(msg.messageId,
            uuid.UUID('c0dfb77c-d6ee-2431-7315-3266e131a866'))
        self.assertEquals(msg.correlationId, u'')
        self.assertEquals(self.buffer.remaining(), 0)

        # now encode the msg to check that encoding is byte for byte the same
        buffer = pyamf.encode(msg, encoding=pyamf.AMF3).getvalue()

        self.assertEquals(buffer, bytes)

    def test_getmessage(self):
        """
        Tests for `getSmallMessage`
        """
        for cls in ['AbstractMessage', 'ErrorMessage', 'RemotingMessage']:
            cls = getattr(messages, cls)
            self.assertRaises(NotImplementedError, cls().getSmallMessage)

        kwargs = {
            'body': {'foo': 'bar'},
            'clientId': 'spam',
            'destination': 'eggs',
            'headers': {'blarg': 'whoop'},
            'messageId': 'baz',
            'timestamp': 1234,
            'timeToLive': 99
        }

        # test async
        a = messages.AsyncMessage(correlationId='yay', **kwargs)
        m = a.getSmallMessage()

        k = kwargs.copy()
        k.update({'correlationId': 'yay'})

        self.assertTrue(isinstance(m, messages.AsyncMessageExt))
        self.assertEquals(m.__dict__, k)

        # test command
        a = messages.CommandMessage(operation='yay', **kwargs)
        m = a.getSmallMessage()

        k = kwargs.copy()
        k.update({
            'operation': 'yay',
            'correlationId': None,
            'messageRefType': None
        })

        self.assertTrue(isinstance(m, messages.CommandMessageExt))
        self.assertEquals(m.__dict__, k)

        # test ack
        a = messages.AcknowledgeMessage(**kwargs)
        m = a.getSmallMessage()

        k = kwargs.copy()
        k.update({'correlationId': None})

        self.assertTrue(isinstance(m, messages.AcknowledgeMessageExt))
        self.assertEquals(m.__dict__, k)


class RegisteredClassesTest(unittest.TestCase):
    """
    Test to ensure that the correct classes have been registered in pyamf.
    """

