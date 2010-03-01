# -*- coding: utf-8 -*-
#
# Copyright The Plasma Project.
# See LICENSE.txt for details.

"""
Uses PyAmf package to encode and decode Flex messages.

.. versionadded:: 0.1
"""

import pyamf.remoting

from plasma.flex.messaging import messages
import errors
import message_context

class PyAmfEncoder(object):
    """
    Uses PyAmf to encode Flex messages.
    """ 

    def encodePacket(self, r_msg, msgs):
        """
        Returns encoded AMF packet.

        :param r_msg: request Flex message
        :type  r_msg: :class:`AbstractMessage`
        :param msgs: list of Flex messages to encode in the packet payload
        :type  msgs: iterable
        :rtype: str
        """
        amf_packet = self.buildPacket(r_msg, msgs)
        context = pyamf.get_context(pyamf.AMF0)
        stream = pyamf.remoting.encode(amf_packet, context)
        return stream.getvalue()

    def buildPacket(self, r_msg, msgs):
        """
        Returns an AMF packet.

        :param r_msg: request Flex message
        :type  r_msg: :class:`AbstractMessage`
        :param msgs: list of Flex messages to encode in the packet payload
        :type  msgs: iterable
        :rtype: :class:`Envelope`
        """

        # Create response packet
        amf_packet = pyamf.remoting.Envelope()
        amf_packet.clientType = r_msg.context.amf_packet.clientType
        amf_packet.amfVersion = pyamf.AMF0

        # Create response messages
        amf_response = pyamf.remoting.Response(msgs)
        # There should never be a failed status code,
        # because a failure should be encoded in the
        # Flex messages instead of the AMF message.
        amf_response.status = pyamf.remoting.STATUS_OK
        amf_response.envelope = amf_packet
        amf_packet[r_msg.context.amf_msg.response] = amf_response

        return amf_packet

class PyAmfDecoder(object):
    """
    Uses PyAmf to decode Flex messages.
    """
    
    def decodePacket(self, raw_packet):
        """
        Decodes an AMF packet and returns a Flex message.

        :param raw_packet: AMF packet to decode
        :type  raw_packet: str
        :rtype: :class:`AbstractMessage`
        """
        context = pyamf.get_context(pyamf.AMF0)
        amf_packet = pyamf.remoting.decode(raw_packet, context)
        return self.extractMsgs(amf_packet)

    def extractMsgs(self, amf_packet):
        """
        Returns a Flex message from a packet object.

        :param packet: AMF packet to get Flex message from.
        :type  packet: :class:`Envelope`
        :rtype: :class:`AbstractMessage`
        :raises: :class:`DecodeError`
        """

        if len(amf_packet.bodies) < 1:
            raise errors.DecodeError("No message bodies in AMF packet.")

        # Flex messaging packets can
        # only contain a single AMF message.
        if len(amf_packet.bodies) > 1:
            raise errors.DecodeError("Multiple message bodies in AMF packet.")

        amf_msg_data = amf_packet.bodies[0]
        amf_msg = amf_msg_data[1]
        amf_msg.response = amf_msg_data[0]

        # Validate message payload
        for flex_msg in amf_msg.body:
            if not isinstance(flex_msg, messages.AbstractMessage):
                raise errors.DecodeError("Message body is not a Flex message.")

            # Assign message context so we can access
            # amf_packet and amf_msg later on.
            flex_msg.context = message_context.AmfMessageContext(
                amf_packet=amf_packet, amf_msg=amf_msg)

        return amf_msg.body
