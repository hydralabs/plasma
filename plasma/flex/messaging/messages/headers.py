# Copyright The Plasma Project.
# See LICENSE.txt for details.

"""
"""

from plasma.util import Constant


DESTINATION_CLIENT_ID = Constant('DSDstClientId',
    'Each message pushed from the server will contain this header '
    'identifying the client that will receive the message.')

ENDPOINT = Constant('DSEndpoint',
    'Messages are tagged with the endpoint id for the channel they are sent '
    'over.')

FLEX_CLIENT_ID = Constant('DSId',
    'Contains the global FlexClient Id value in outbound messages once it '
    'has been assigned by the server.')

PRIORTY = Constant('DSPriority'
    'Offers a priority setting that the server may choose to use in '
    'determining message priority')

REMOTE_CREDENTIALS = Constant('DSRemoteCredentials',
    'Messages that need to set remote credentials for a destination carry '
    'the base64 encoded credentials in this header.')

REMOTE_CREDENTIALS_CHARSET = Constant('DSRemoteCredentialsCharset',
    'The charset used to encode the remote credentials')

REQUEST_TIMEOUT = Constant('DSRequestTimeout',
    'The request timeout value is set on outbound messages by services or '
    'channels and the value controls how long the responder will wait for an '
    'acknowledgement, result or fault response for the message before timing '
    'out the request.')

STATUS = Constant('DSStatusCode',
    'Provide some status context for nature of the response message. E.g. an '
    'HTTP status code')

VALIDATE_ENDPOINT = Constant('DSValidateEndpoint',
    'Used to validate the channel that the message was received over')

SUBTOPIC = Constant('DSSubtopic',
    'Messages that were sent with a defined subtopic property indicate their '
    'target subtopic in this header.')

ERROR_HINT = Constant('DSErrorHint', 'Used to indicate that the ack is for a '
    'message that generated an error.')

RETRYABLE_ERROR_HINT = Constant('DSRetryableErrorHint', 'Used to indicate '
    'that the operation that generated the error may be retryable rather '
    'than fatal.')

# what the hell does this mean?!
SELECTOR = Constant('DSSelector', 'Subscribe commands issued by a consumer '
    'pass the consumer selector expression in this header.')
