# -*- coding: utf-8 -*-
#
# Copyright The Plasma Project.
# See LICENSE.txt for details.

"""
Classes that store metadata about messages.

.. versionadded:: 0.1
"""

class MessageContext(object):
    """
    Stores metadata about a message.

    :ivar channel: the Channel a message was sent over
    :type channel: :class:`Channel`
    :ivar channel: the connection the message belongs to
    :type channel: :class:`Connection`
    """
    def __init__(self, channel=None, connection=None):
        self.channel = channel
        self.connection = connection

class AmfMessageContext(MessageContext):
    """
    Metadata for a message that was sent over an AMF channel.

    :ivar amf_packet: the AMF packet the message arrived in
    :ivar amf_msg: the AMF message the message arrived in
    """

    def __init__(self, amf_packet=None, amf_msg=None, *args, **kwargs):
        MessageContext.__init__(self, *args, **kwargs)
        self.amf_packet = amf_packet
        self.amf_msg = amf_msg
