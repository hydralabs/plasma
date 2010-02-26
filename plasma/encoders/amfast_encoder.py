# -*- coding: utf-8 -*-
#
# Copyright The Plasma Project.
# See LICENSE.txt for details.

"""
Uses AmFast package to encode and decode Flex messages.

.. versionadded:: 0.1
"""

from amfast.decode import decode_packet
from amfast.encode import encode_packet
from amfast.context import DecoderContext, EncoderContext
from amfast.class_def import ClassDef, ClassDefMapper
import amfast.remoting

import errors

from plasma.flex.messaging import messages
import message_context

def _map_flex_messages(mapper):
    """
    Maps Flex messages to ClassDefs.

    :param mapper: the object that retrieves ClassDef objects
    :type  mapper: :class:`amfast.class_def.ClassDefMapper`
    """

    mapper.mapClass(ClassDef(messages.AsyncMessage, amf3=True,
        alias="flex.messaging.messages.AsyncMessage",
        static_attrs=("body", "clientId", "destination", "headers",
            "messageId", "timestamp", "timeToLive", "correlationId")
    ))

    mapper.mapClass(ClassDef(messages.AcknowledgeMessage, amf3=True,
        alias="flex.messaging.messages.AcknowledgeMessage",
        static_attrs=("body", "clientId", "destination", "headers",
            "messageId", "timestamp", "timeToLive", "correlationId")
    ))

    mapper.mapClass(ClassDef(messages.ErrorMessage, amf3=True,
        alias="flex.messaging.messages.ErrorMessage",
        static_attrs=("body", "clientId", "destination", "headers",
            "messageId", "timestamp", "timeToLive", "correlationId",
            "extendedData", "faultCode", "faultDetail", "faultString",
            "rootcause")
    ))

    mapper.mapClass(ClassDef(messages.CommandMessage, amf3=True,
        alias="flex.messaging.messages.CommandMessage",
        static_attrs=("body", "clientId", "destination", "headers",
            "messageId", "timestamp", "timeToLive", "correlationId",
            "operation")
    ))

    mapper.mapClass(ClassDef(messages.RemotingMessage, amf3=True,
        alias="flex.messaging.messages.RemotingMessage",
        static_attrs=("body", "clientId", "destination", "headers",
            "messageId", "timestamp", "timeToLive", "correlationId",
            "operation", "source")
    ))

class AmFastEncoder(object):
    """
    Uses AmFast package to encode messages.

    :ivar use_collections: if True, encode lists and tuples as ArrayCollections
    :type use_collections: bool
    :ivar use_proxies: if True, encode dicts as ObjectProxies
    :type use_proxies: bool
    :ivar use_references: if True, use references to encode objects
    :type use_references: bool
    :ivar use_legacy_xml: if True, encode XML to XMLDocument instead of e4x
    :type use_legacy_xml: bool
    :ivar include_private: if True, encode attributes starting with '_'
    :type include_private: bool
    :ivar class_def_mapper: the object that retrieves ClassDef objects
    :type class_def_mapper: :class:`amfast.class_def.ClassDefMapper`
    """

    def __init__(self, use_collections=False, use_proxies=False,
        use_references=True, use_legacy_xml=False, include_private=False,
        class_def_mapper=None, buffer=None):

        self.use_collections = use_collections
        self.use_proxies = use_proxies
        self.use_references = use_references
        self.use_legacy_xml = use_legacy_xml
        self.include_private = include_private

        if class_def_mapper is None:
            class_def_mapper = ClassDefMapper()
        self.class_def_mapper = class_def_mapper
        _map_flex_messages(self.class_def_mapper)

    def _getContext(self):
        kwargs = {
            'amf3': True,
            'use_collections': self.use_collections,
            'use_proxies': self.use_proxies,
            'use_references': self.use_references,
            'use_legacy_xml': self.use_legacy_xml,
            'include_private': self.include_private,
            'class_def_mapper': self.class_def_mapper
        }

        return EncoderContext(**kwargs);

    def encode(self, r_msg, msgs):
        """
        Returns encoded AMF packet.

        :param r_msg: request Flex message
        :type  r_msg: :class:`AbstractMessage`
        :param msgs: list of Flex messages to encode in the packet payload
        :type  msgs: iterable
        :rtype: str
        """
        amf_packet = self.buildPacket(r_msg, msgs)
        return encode_packet(amf_packet, self._getContext())

    def buildPacket(self, r_msg, msgs):
        """
        Returns an AMF packet.

        :param r_msg: request Flex message
        :type  r_msg: :class:`AbstractMessage`
        :param msgs: list of Flex messages to encode in the packet payload
        :type  msgs: iterable
        :rtype: :class:`amfast.remoting.Packet`
        """
        amf_response = amfast.remoting.Message(
            target=r_msg.context.amf_msg.response + \
                amfast.remoting.Message.SUCCESS_TARGET,
            body=msgs, response=''
        )

        return amfast.remoting.Packet(
            client_type=r_msg.context.amf_packet.client_type,
            messages=(amf_response,))

class AmFastDecoder(object):
    """
    Uses AmFast package to decode messages.

    :ivar class_def_mapper: the object that retrieves ClassDef objects
    :type class_def_mapper: :class:`amfast.class_def.ClassDefMapper`
    """

    def __init__(self, class_def_mapper=None):
        if class_def_mapper is None:
            class_def_mapper = ClassDefMapper()
        self.class_def_mapper = class_def_mapper
        _map_flex_messages(self.class_def_mapper)

    def _getContext(self, input):
        return DecoderContext(input, amf3=True, class_def_mapper=self.class_def_mapper)

    def decode(self, raw_packet):
        """
        Decodes an AMF packet and returns a Flex message.

        :param raw_packet: AMF packet to decode
        :type  raw_packet: str
        :rtype: :class:`AbstractMessage`
        """
        amf_packet = decode_packet(self._getContext(raw_packet))
        return self.extractMsgs(amf_packet)

    def extractMsgs(self, amf_packet):
        """
        Returns a Flex message from a packet object.

        :param packet: AMF packet to get Flex message from.
        :type  packet: :class:`Envelope`
        :rtype: :class:`AbstractMessage`
        :raises: :class:`DecodeError`
        """
        if len(amf_packet.messages) < 1:
            raise errors.DecodeError("No message bodies in AMF packet.")

        # Flex messaging packets can
        # only contain a single AMF message.
        if len(amf_packet.messages) > 1:
            raise errors.DecodeError("Multiple message bodies in AMF packet.")

        amf_msg = amf_packet.messages[0]

        for flex_msg in amf_msg.body:
            # Validate message payload
            if not isinstance(flex_msg, messages.AbstractMessage):
                raise errors.DecodeError("Message body is not a Flex message.")

            # Assign message context so we can access
            # amf_packet and amf_msg later on.
            flex_msg.context = message_context.AmfMessageContext(
                amf_packet=amf_packet, amf_msg=amf_msg)

        return amf_msg.body
