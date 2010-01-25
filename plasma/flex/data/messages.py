# Copyright (c) 2009 The Plasma Project.
# See LICENSE.txt for details.

"""
Flex Data Management Service implementation.

This module contains the message classes used with Flex Data Management
Service.

.. versionadded:: 0.1

"""


import pyamf

from plasma.flex.messaging import messages

__all__ = [
    'DataMessage',
    'SequencedMessage',
    'PagedMessage',
    'DataErrorMessage'
]


class DataMessage(messages.AsyncMessage):
    """
    This message is used to transport an operation that occured on a managed
    object or collection.

    This class of message is transmitted between clients subscribed to a
    remote destination as well as between server nodes within a cluster.
    The payload of this message describes all of the relevant details of
    the operation. This information is used to replicate updates and detect
    conflicts.

    :ivar identity: Provides access to the identity map which defines the
        unique identity of the item affected by this `DataMessage`
        (relevant for create/update/delete but not fill operations).
    :ivar operation: Provides access to the operation/command of this
        `DataMessage`. Operations indicate how the remote destination should
        process this message.
    
    .. seealso:: `DataMessage on Livedocs
        <http://livedocs.adobe.com/flex/201/langref/mx/data/messages/DataMessage.html>`_
    """

    class __amf__:
        static = ('identity', 'operation',)

    __slots__ = __amf__.static

    def __init__(self, **kwargs):
        messages.AsyncMessage.__init__(self, **kwargs)

        self.identity = kwargs.pop('identity', None)
        self.operation = kwargs.pop('operation', None)


class SequencedMessage(messages.AcknowledgeMessage):
    """
    Response to :class:`DataMessage` requests.

    :ivar sequenceId: Unique identifier for a sequence within a remote
        destination. This value is only unique for the endpoint and
        destination contacted.
    :ivar sequenceSize: How many items reside in the remote sequence.

    .. seealso:: `SequencedMessage on Livedocs
        <http://livedocs.adobe.com/flex/201/langref/mx/data/messages/SequencedMessage.html>`_
    """

    class __amf__:
        static = ('sequenceId', 'sequenceSize',)

    __slots__ = __amf__.static

    def __init__(self, **kwargs):
        messages.AcknowledgeMessage.__init__(self, **kwargs)

        self.sequenceId = kwargs.pop('sequenceId', None)
        self.sequenceSize = kwargs.pop('sequenceSize', None)


class PagedMessage(SequencedMessage):
    """
    This message provides information about a partial sequence result.

    :ivar pageCount: Provides access to the number of total pages in a
        sequence based on the current page size.
    :ivar pageIndex: Provides access to the index of the current page in a
        sequence.

    .. seealso:: `PagedMessage on Livedocs
        <http://livedocs.adobe.com/flex/201/langref/mx/data/messages/PagedMessage.html>`_
    """

    class __amf__:
        static = ('pageCount', 'pageIndex',)

    __slots__ = __amf__.static

    def __init__(self, **kwargs):
        SequencedMessage.__init__(self, **kwargs)

        self.pageCount = kwargs.pop('pageCount', None)
        self.pageIndex = kwargs.pop('pageIndex', None)


class DataErrorMessage(messages.ErrorMessage):
    """
    Special cases of ErrorMessage will be sent when a data conflict
    occurs.

    This message provides the conflict information in addition to
    the :class:`~plasma.flex.messaging.ErrorMessage` information.

    :ivar cause: The client originated message which caused the conflict.
    :ivar propertyNames: A list of properties that were found to be
        conflicting between the client and server objects.
    :ivar serverObject: The value that the server had for the object with the
        conflicting properties.

    .. seealso:: `DataErrorMessage on Livedocs
        http://livedocs.adobe.com/flex/201/langref/mx/data/messages/DataErrorMessage.html>`_

    """

    class __amf__:
        static = ('cause', 'propertyNames', 'serverObject')

    __slots__ = __amf__.static

    def __init__(self, **kwargs):
        messages.ErrorMessage.__init__(self, **kwargs)

        self.cause = kwargs.pop('cause', None)
        self.propertyNames = kwargs.pop('propertyNames', None)
        self.serverObject = kwargs.pop('serverObject', None)


pyamf.register_package(globals(), package='flex.data.messages')
