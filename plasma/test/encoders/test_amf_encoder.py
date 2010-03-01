# -*- coding: utf-8 -*-
#
# Copyright The Plasma Project.
# See LICENSE.txt for details.

"""
Flex Encoder/Decoder compatibility tests.

.. versionadded:: 0.1

"""
from twisted.trial import unittest

from plasma.encoders import message_context
from plasma.flex.messaging import messages

class AmfEncoderTestCase(unittest.TestCase):
    """
    Base class for AMF encoder tests.
    """

    def setUp(self):

        # Bytes are from AmFast messaging server
        self.async_response_bytes = '' \
'\x00\x03\x00\x00\x00\x01\x00\x0b/6/onResult\x00\x00\x00\x00\x00\xb2\x11\t\x03\x01\n\x81\x03Uflex.messaging.messages.AcknowledgeMessage\tbody\x11clientId\x17destination\x0fheaders\x13messageId\x13timestamp\x15timeToLive\x1bcorrelationId\x01\x01\x01\n\x0b\x01\x01\x01\x01\x01\x06KId297cc0a-7798-4ffd-a677-09708eeb733c'

        # Bytes are straight from a Flash client.
        self.async_request_bytes = '' \
'\x00\x03\x00\x00\x00\x01\x00\x04null\x00\x02/5\x00\x00\x01\x0f\n\x00\x00\x00\x01\x11\n\x81\x03Iflex.messaging.messages.AsyncMessage\x1bcorrelationId\x17destination\x11clientId\tbody\x13messageId\x0fheaders\x13timestamp\x15timeToLive\x06\x01\x06\x11messages\x01\x06\x19Hello World!\x06I0FECDD94-5FFD-B29A-5BAB-0BB907CED18B\n\x0b\x01\x15DSEndpoint\x06#streaming-channel\tDSId\x06I3a10fed0-0011-4345-b591-165c8541a042\x01\x04\x00\x04\x00'
 
        self.correlationId = "1234"
        self.clientId = "4321"

    def getRequestFlexMessage(self):
        flex_msg = messages.AsyncMessage()
        flex_msg.correlationId = self.correlationId
        flex_msg.clientId = self.clientId
        return flex_msg

    def test_encodeAcknowledgeMessage(self):
        m = messages.AcknowledgeMessage()
        m.correlationId = "Id297cc0a-7798-4ffd-a677-09708eeb733c"
        r_msg = self.getRequestMessage("/6")
        encoded = self.getEncoder().encodePacket(r_msg, (m,))
        self.assertEquals(encoded, self.async_response_bytes)

    def test_decodeAsyncMessage(self):
        m = self.getDecoder().decodePacket(self.async_request_bytes)[0]
        self.assertEquals("Hello World!", m.body)
        self.assertTrue(isinstance(m.context, message_context.AmfMessageContext))
