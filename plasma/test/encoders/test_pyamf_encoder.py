# -*- coding: utf-8 -*-
#
# Copyright The Plasma Project.
# See LICENSE.txt for details.

"""
Flex Encoder/Decoder compatibility tests.

.. versionadded:: 0.1

"""
import pyamf
import pyamf.remoting

from plasma.encoders.pyamf_encoder import PyAmfEncoder, PyAmfDecoder
from plasma.flex.messaging import messages
from plasma.test.encoders.test_amf_encoder import AmfEncoderTestCase

class PyAmfEncoderTestCase(AmfEncoderTestCase):
    """
    Encoding tests for PyAmfEncoder.
    """

    def getEncoder(self):
       return PyAmfEncoder()

    def getDecoder(self):
       return PyAmfDecoder()

    def getRequestPacket(self, response):
       """
       Creates a packet ready to be used as a request packet.
       """
       amf_packet = pyamf.remoting.Envelope()
       amf_packet.clientType = pyamf.ClientTypes.Flash9
       amf_packet.amfVersion = pyamf.AMF0
       amf_msg = pyamf.remoting.Request('null',
           body=(self.getRequestFlexMessage(),),
           envelope=amf_packet)
       amf_packet.bodies.append((response, amf_msg))
       return amf_packet

    def getRequestMessage(self, response):
       """
       Creates a message ready to be used as a request message.
       """
       return self.getDecoder().extractMsgs(self.getRequestPacket(response))[0]
