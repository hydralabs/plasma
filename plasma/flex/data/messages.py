# Copyright (c) 2009 The Plasma Project.
# See LICENSE.txt for details.

"""
Flex Data Management Service implementation.

This module contains the message classes used with Flex Data Management
Service.

@since: 0.1
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
    I am used to transport an operation that occured on a managed object
    or collection.

    This class of message is transmitted between clients subscribed to a
    remote destination as well as between server nodes within a cluster.
    The payload of this message describes all of the relevant details of
    the operation. This information is used to replicate updates and detect
    conflicts.

    @ivar identity: Provides access to the identity map which defines the
        unique identity of the item affected by this DataMessage (relevant for
        create/update/delete but not fill operations).
    @ivar operation: Provides access to the operation/command of this
        DataMessage. Operations indicate how the remote destination should
        process this message.
    @see: U{DataMessage on Livedocs
    <http://livedocs.adobe.com/flex/201/langref/mx/data/messages/DataMessage.html>}
    """

    def __init__(self, **kwargs):
        messages.AsyncMessage.__init__(self, **kwargs)

        self.identity = kwargs.pop('identity', None)
        self.operation = kwargs.pop('operation', None)


class SequencedMessage(messages.AcknowledgeMessage):
    """
    Response to L{DataMessage} requests.

    @ivar sequenceId: Unique identifier for a sequence within a remote
        destination. This value is only unique for the endpoint and
        destination contacted.
    @ivar sequenceProxies: ???
    @ivar sequenceSize: How many items reside in the remote sequence.

    @see: U{SequencedMessage on Livedocs
    <http://livedocs.adobe.com/flex/201/langref/mx/data/messages/SequencedMessage.html>}
    """

    def __init__(self, **kwargs):
        messages.AcknowledgeMessage.__init__(self, **kwargs)

        self.sequenceId = kwargs.pop('sequenceId', None)
        self.sequenceProxies = kwargs.pop('sequenceProxies', None)
        self.sequenceSize = kwargs.pop('sequenceSize', None)

        # XXX: do we encode this?!
        self.dataMessage = kwargs.pop('dataMessage', None)


class PagedMessage(SequencedMessage):
    """
    This messsage provides information about a partial sequence result.

    @ivar pageCount: Provides access to the number of total pages in a
        sequence based on the current page size.
    @ivar pageIndex: Provides access to the index of the current page in a
        sequence.
    @see: U{PagedMessage on Livedocs
    <http://livedocs.adobe.com/flex/201/langref/mx/data/messages/PagedMessage.html>}
    """

    def __init__(self, **kwargs):
        SequencedMessage.__init__(self, **kwargs)

        self.pageCount = kwargs.pop('pageCount', None)
        self.pageIndex = kwargs.pop('pageIndex', None)


class DataErrorMessage(messages.ErrorMessage):
    """
    Special cases of ErrorMessage will be sent when a data conflict
    occurs.

    This message provides the conflict information in addition to
    the L{ErrorMessage<plasma.flex.messaging.ErrorMessage>} information.

    @ivar cause: The client originated message which caused the conflict.
    @ivar propertyNames: A list of properties that were found to be
        conflicting between the client and server objects.
    @ivar serverObject: The value that the server had for the object with the
        conflicting properties.

    @see: U{DataErrorMessage on Livedocs
    <http://livedocs.adobe.com/flex/201/langref/mx/data/messages/DataErrorMessage.html>}
    """

    def __init__(self, **kwargs):
        messages.ErrorMessage.__init__(self, **kwargs)

        self.cause = kwargs.pop('cause', None)
        self.propertyNames = kwargs.pop('propertyNames', None)
        self.serverObject = kwargs.pop('serverObject', None)


pyamf.register_package(globals(), package='flex.data.messages')
