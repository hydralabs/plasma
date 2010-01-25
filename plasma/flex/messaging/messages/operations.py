# Copyright The Plasma Project.
# See LICENSE.txt for details.

"""
A list of all command operations available.
"""

from plasma.util import Constant


subscribe = Constant(0, 'Used to subscribe to a remote destination.')

unsubscribe = Constant(1, 'Used to unsubscribe from a remote destination')

poll = Constant(2, 'Used to poll a remote destination for pending, '
    'undelivered messages.')

unused3 = Constant(3, 'This operation is not used.')

client_sync = Constant(4, 'Used by a remote destination to sync missed or '
    'cached messages as a results of an issued poll command')

ping = Constant(5, 'Used to test the connectivity over the current channel '
    'to the remote endpoint')

unused6 = Constant(6, 'This operation is not used.')

cluster_request = Constant(7, 'This is used to request a list of failover '
    'endpoint URIs for the remote destination based on cluster membership.')

login = Constant(8, 'Used to send credentials to the endpoint so that the '
    'user can be logged in over the current channel. The credentials need to '
    'be base64 encoded and stored in the body of the message.')

logout = Constant(9, 'used to log the user out of the current channel, and '
    'will invalidate the server session if the channel is HTTP based.')

subscription_invalidate = Constant(10, 'Used to indicate that the client '
    'subscription to a remote destination has been invalidated.')

multi_subscribe = Constant(11, 'Used to un/subscribe to multiple subtopics '
    'in the same message.')

disconnect = Constant(12, 'Used to indicate that a channel has been '
    'disconnected')

trigger_connect = Constant(13, 'Used to trigger a client connect attempt.')

unknown = Constant(10000, 'Default operation for new CommandMessage instances')
