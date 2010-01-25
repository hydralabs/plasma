# Copyright The Plasma Project.
# See LICENSE.txt for details.

"""
"""

import inspect
import uuid

import pyamf.util
from pyamf.amf3 import ByteArray

from plasma.flex.messaging import messages


__all__ = ['AcknowledgeMessageExt', 'CommandMessageExt', 'AsyncMessageExt']


HAS_NEXT = 0x80


class SmallMessageMixIn(object):
    """
    """

    flags = (
        messages.AbstractMessage.__slots__,
        (0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40)
    )

    bytes = (
        ('clientId', 'messageId'),
        (0x01, 0x02)
    )

    __slots__ = ()

    def __init__(self, msg):
        for cls in inspect.getmro(msg.__class__):
            if hasattr(cls, '__slots__'):
                for attr in cls.__slots__:
                    setattr(self, attr, getattr(msg, attr))

    def decodeSmallAttribute(self, attr, input):
        obj = input.readObject()

        if attr in ['timestamp', 'timeToLive']:
            return pyamf.util.get_datetime(obj / 1000.0)

        return obj

    def encodeSmallAttribute(self, attr):
        obj = getattr(self, attr)

        if not obj:
            return obj

        if attr in ['timestamp', 'timeToLive']:
            return pyamf.util.get_timestamp(obj) * 1000.0
        elif attr in ['clientId', 'messageId']:
            if isinstance(obj, uuid.UUID):
                return None

        return obj

    # IExternalizable

    def __readamf__(self, input):
        flags = read_flag_mask(input)

        if len(flags) > 2:
            raise pyamf.DecodeError('Expected <=2 (got %d) flags for the '
                'AbstractMessage portion of the small message for %r' % (
                    len(flags), self.__class__))

        self.__class__.__init__(self)

        for index, byte in enumerate(flags):
            if index == 0:
                self._read_attrs(SmallMessageMixIn.flags, byte, input)
            elif index == 1:
                self._read_uuid(SmallMessageMixIn.bytes, byte, input)

    def __writeamf__(self, output):
        flag_attrs = []
        uuid_attrs = []
        byte = 0

        attrs, flags = SmallMessageMixIn.flags

        for i, flag in enumerate(flags):
            attr = attrs[i]
            value = self.encodeSmallAttribute(attr)

            if value:
                byte |= flag
                flag_attrs.append(value)

        flags = byte
        byte = 0
        attrs, bytes = SmallMessageMixIn.bytes

        for i, flag in enumerate(bytes):
            attr = attrs[i]
            value = getattr(self, attr)

            if not value:
                continue

            byte |= flag
            uuid_attrs.append(ByteArray(value.bytes))

        if not byte:
            output.writeUnsignedByte(flags)
        else:
            output.writeUnsignedByte(flags | HAS_NEXT)
            output.writeUnsignedByte(byte)

        [output.writeObject(attr) for attr in flag_attrs]
        [output.writeObject(attr) for attr in uuid_attrs]

    def _read_attrs(self, flags, byte, input):
        """
        Reads a set of attrs as defined by flags. `flags` is a tuple of
        tuples, the first being a list of attributes and the second being a
        list of bitmasks to determine if that attribute is set.

        `byte` is the `int` to be masked against.
        `input` used to read the attribute from the amf stream.

        .. seealso: `IDataOutput on Livedocs (external)
            <http://livedocs.adobe.com/flex/201/langref/flash/utils/IDataOutput.html>`_
        """
        attrs, bytes = flags

        for i, flag in enumerate(bytes):
            if flag & byte:
                attr = attrs[i]

                setattr(self, attr, self.decodeSmallAttribute(attr, input))

    def _read_uuid(self, flags, byte, input):
        """
        Similar in scope to `_read_attrs` but will specifically read a UUID
        (which is wrapped up as a :class:`pyamf.amf3.ByteArray`)
        """
        attrs, bytes = flags

        for i, flag in enumerate(bytes):
            if flag & byte:
                setattr(self, attrs[i], decode_uuid(input.readObject()))


class AsyncMessageExt(messages.AsyncMessage, SmallMessageMixIn):
    """
    An L{messages.AsyncMessage}, but implementing C{ISmallMessage}.
    """

    flags = (
        ('correlationId',),
        (0x01,),
    )

    bytes = (
        ('correlationId',),
        (0x02,),
    )

    __slots__ = ()

    class __amf__:
        external = True

    def __init__(self, msg=None):
        messages.AsyncMessage.__init__(self)

        if msg:
            SmallMessageMixIn.__init__(self, msg)

    def __readamf__(self, input):
        SmallMessageMixIn.__readamf__(self, input)

        flags = read_flag_mask(input)

        if len(flags) > 1:
            raise pyamf.DecodeError('Expected <=1 (got %d) flags for the '
                'AsyncMessage portion of the small message for %r' % (
                    len(flags), self.__class__))

        byte = flags[0]

        self._read_attrs(AsyncMessageExt.flags, byte, input)
        self._read_uuid(AsyncMessageExt.bytes, byte, input)

    def __writeamf__(self, output):
        SmallMessageMixIn.__writeamf__(self, output)

        if not isinstance(self.correlationId, uuid.UUID):
            output.writeUnsignedByte(0x01)
            output.writeObject(self.correlationId)
        else:
            output.writeUnsignedByte(0x02)
            output.writeObject(ByteArray(self.correlationId.bytes))


class AcknowledgeMessageExt(messages.AcknowledgeMessage, AsyncMessageExt):
    """
    An :class:`messages.AcknowledgeMessage`, but implementing ISmallMessage.
    """

    __slots__ = ()

    class __amf__:
        external = True

    def __init__(self, msg=None):
        messages.AcknowledgeMessage.__init__(self)

        if msg:
            SmallMessageMixIn.__init__(self, msg)


class CommandMessageExt(messages.CommandMessage, AsyncMessageExt):
    """
    A :class:`messages.CommandMessage`, but implementing ISmallMessage.
    """

    flags = (
        ('operation',),
        (0x01,),
    )

    __slots__ = ()

    class __amf__:
        external = True

    def __init__(self, msg=None):
        messages.CommandMessage.__init__(self)
        AsyncMessageExt.__init__(self, msg=msg)

    def __readamf__(self, input):
        AsyncMessageExt.__readamf__(self, input)

        flags = read_flag_mask(input)

        if len(flags) > 1:
            raise pyamf.DecodeError('Expected <=1 (got %d) flags for the '
                'CommandMessage portion of the small message for %r' % (
                    len(flags), self.__class__))

        byte = flags[0]

        self._read_attrs(CommandMessageExt.flags, byte, input)

    def __writeamf__(self, output):
        AsyncMessageExt.__writeamf__(self, output)

        if self.operation:
            output.writeUnsignedByte(0x01)
            output.writeObject(self.operation)
        else:
            output.writeUnsignedByte(0)


def read_flag_mask(input):
    flags = []

    while True:
        byte = input.readUnsignedByte()

        flags.append(byte)

        if byte & HAS_NEXT == 0:
            return flags


def decode_uuid(obj):
    """
    Decode a :class:`ByteArray` contents to a :class:`uuid.UUID` instance.
    """
    return uuid.UUID(bytes=str(obj))


pyamf.register_class(AcknowledgeMessageExt, 'DSK')
pyamf.register_class(CommandMessageExt, 'DSC')
pyamf.register_class(AsyncMessageExt, 'DSA')
