# -*- coding: utf-8 -*-
#
# Copyright The Plasma Project.
# See LICENSE.txt for details.

"""
Flex Encoder/Decoder compatibility tests.

.. versionadded:: 0.1

"""

import amfast.remoting

from plasma.encoders.amfast_encoder import AmFastEncoder, AmFastDecoder
from plasma.flex.messaging import messages
from plasma.test.encoders.test_amf_encoder import AmfEncoderTestCase

class AmFastEncoderTestCase(AmfEncoderTestCase):
    """
    Encoding tests for AmFastEncoder and AmFastDecoder.
    """

    def getEncoder(self):
       return AmFastEncoder()

    def getDecoder(self):
       return AmFastDecoder()

    def getRequestPacket(self, response):
        """
        Creates a packet ready to be used as a request packet.
        """
        amf_msg = amfast.remoting.Message(target='null', response=response,
            body=(self.getRequestFlexMessage(),))
        amf_packet = amfast.remoting.Packet(messages=(amf_msg,))
        amf_packet.client_type = amfast.remoting.Packet.FLASH_9
        return amf_packet

    def getRequestMessage(self, response):
       """
       Creates a message ready to be used as a request message.
       """
       return self.getDecoder().extractMsgs(self.getRequestPacket(response))[0]
