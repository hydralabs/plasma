# Copyright The Plasma Project.
# See LICENSE.txt for details.

"""
Remoting client implementation.

"""

from urlparse import urlparse

from twisted.web.client import HTTPClientFactory
from twisted.internet import reactor
from twisted.internet.defer import Deferred

from pyamf import remoting
from pyamf.remoting import get_exception_from_fault
import pyamf

from plasma.version import version


class ServiceMethodProxy(object):
    """
    Serves as a proxy for calling a service method.

    :ivar service: the parent service
    :type service: :class:`~ServiceProxy`
    :ivar name: the name of the method
    :type name: `str` or `None`

    .. seealso:: :meth:`ServiceProxy.__getattr__`

    """

    def __init__(self, service, name):
        self.service = service
        self.name = name

    def __call__(self, *args):
        """
        Inform the proxied service that this function has been called.
        """
        return self.service._call(self, *args)

    def __str__(self):
        """
        Returns the full service name, including the method name if there is
        one.

        """
        service_name = str(self.service)

        if self.name is not None:
            service_name = '%s.%s' % (service_name, self.name)

        return service_name


class ServiceProxy(object):
    """
    Serves as a service object proxy for RPC calls. Generates
    :class:`~ServiceMethodProxy` objects for method calls.

    .. seealso:: :class:`~RequestWrapper` for more info.

    :ivar _gw: The parent gateway
    :type _gw: :class:`~RemotingService`
    :ivar _name: The name of the service
    :type _name: `str`
    :ivar _auto_execute: If set to `True`, when a service method is called,
        the AMF request is immediately sent to the remote gateway and a
        response is returned. If set to `False`, a :class:`~RequestWrapper` is
        returned, waiting for the underlying gateway to fire the
        :meth:`RemotingService.execute` method.

    """

    def __init__(self, gw, name, auto_execute=True):
        self._gw = gw
        self._name = name
        self._auto_execute = auto_execute

    def __getattr__(self, name):
        return ServiceMethodProxy(self, name)

    def _call(self, method_proxy, *args):
        """
        Executed when a :class:`~ServiceMethodProxy` is called.
        Adds a request to the underlying gateway. If `_auto_execute` is set to
        `True`, then the request is immediately called on the remote gateway.

        """
        d = self._gw.addRequest(method_proxy, *args)
        if self._auto_execute:
            self._gw.execute()
        return d

    def __call__(self, *args):
        """
        This allows services to be 'called' without a method name.

        """
        return self._call(ServiceMethodProxy(self, None), *args)

    def __str__(self):
        """
        Returns a string representation of the name of the service.

        """
        return self._name


class RequestWrapper(object):
    """
    A container object that wraps a service method request.

    :ivar id: The id of the request.
    :type id: `str`
    :ivar service: The service proxy.
    :type service: :class:`~ServiceProxy`
    :ivar args: The args used to invoke the call.
    :type args: `list`

    """

    def __init__(self, id_, service, *args):
        self.id = id_
        self.service = service
        self.args = args
        self.deferred = Deferred()


class RemotingServiceBase(object):
    """
    Acts as a client for AMF calls.

    :ivar requests: The list of pending requests to process.
    :type requests: `list`
    :ivar request_number: A unique identifier for tracking the number of
        requests.
    :ivar amf_version: The AMF version to use.
        See :data:`ENCODING_TYPES <pyamf.ENCODING_TYPES>`.
    :type amf_version: `int`
    :ivar headers: A list of persistent headers to send with each request.
    :type headers: :class:`~pyamf.remoting.HeaderCollection`
    :ivar strict: Whether to use strict AMF en/decoding or not.
    :type strict: `bool`

    """

    def __init__(self, amf_version=pyamf.AMF0, strict=False, logger=None):
        self.amf_version = amf_version

        self.requests = []
        self.request_number = 1
        self.headers = remoting.HeaderCollection()
        self.strict = strict
        self.logger = logger

    def addHeader(self, name, value, must_understand=False):
        """
        Sets a persistent AMF header to send with each request.

        :param name: Header name.
        :type name: `str`
        :param must_understand: Default is `False`.
        :type must_understand: `bool`

        """
        self.headers[name] = value
        self.headers.set_required(name, must_understand)

    def getService(self, name, auto_execute=True):
        """
        Returns a :class:`~ServiceProxy` for the supplied name. Sets up an
        object that can have method calls made to it that build the AMF
        requests.

        :param auto_execute: Default is `True`.
        :type auto_execute: `bool`
        :raise TypeError: `string` type required for `name`.
        :rtype: :class:`ServiceProxy`

        """
        if not isinstance(name, basestring):
            raise TypeError('string type required')

        return ServiceProxy(self, name, auto_execute)

    def addRequest(self, service, *args):
        """
        Adds a request to be sent to the remoting gateway.

        :return: a :class:`Deferred` that will callback when the invocation
                 result is available

        """
        request = RequestWrapper('/%d' % self.request_number, service, *args)

        self.request_number += 1
        self.requests.append(request)

        if self.logger:
            self.logger.debug('Adding request %s%r', request.service, args)

        return request.deferred

    def removeRequest(self, deferred):
        """
        Removes a request from the pending request list.

        :raise LookupError: Request not found.

        """
        for index, request in enumerate(self.requests):
            if request.deferred == deferred:
                if self.logger:
                    self.logger.debug('Removing request: %s', request)
                del self.requests[index]
                return

        raise LookupError("Request not found")

    def _createAMFRequest(self, requests):
        """
        Builds an AMF request :class:`~pyamf.remoting.Envelope` from the
        stored list of requests.

        :rtype: :class:`~pyamf.remoting.Envelope`

        """
        envelope = remoting.Envelope(self.amf_version)

        if self.logger:
            self.logger.debug('AMF version: %s', self.amf_version)

        for request in requests:
            service = request.service
            args = list(request.args)
            envelope[request.id] = remoting.Request(str(service), args)

        envelope.headers = self.headers
        return envelope

    def _handleAMFResponse(self, envelope, requests):
        """
        Handles the AMF response from the server.

        :type response: :class:`~pyamf.remoting.Envelope`

        """
        if self.logger:
            self.logger.debug('Response: %s' % envelope)

        if remoting.REQUEST_PERSISTENT_HEADER in envelope.headers:
            data = envelope.headers[remoting.REQUEST_PERSISTENT_HEADER]
            for k, v in data.iteritems():
                self.headers[k] = v

        for request in requests:
            response = envelope[request.id]
            if response.status == remoting.STATUS_OK:
                request.deferred.callback(response.body)
            elif response.status == remoting.STATUS_ERROR:
                exc_class = get_exception_from_fault(response.body)
                exception = exc_class(response.body.description)
                request.deferred.errback(exception)

    def _handleAMFError(self, failure, requests):
        for request in requests:
            request.deferred.errback(failure)

    def execute(self):
        """
        Builds, sends and handles the responses to all requests listed in
        `self.requests`.

        """
        raise NotImplementedError

    def setCredentials(self, username, password):
        """
        Sets authentication credentials for accessing the remote gateway.

        """
        self.addHeader('Credentials', dict(userid=unicode(username),
            password=unicode(password)), True)


class HTTPRemotingService(RemotingServiceBase):
    """
    Remoting service using standard HTTP/1.0 requests. Sends one request, or
    a batch of requests to the remote server, and invokes all the callbacks
    when it receives a reply.

    """

    BASE_HTTP_HEADERS = {'Content-Type': remoting.CONTENT_TYPE}

    user_agent = 'Plasma/%s' % version

    def __init__(self, url, amf_version=pyamf.AMF0,
                 user_agent=None, **kwargs):
        """
        :ivar url: The url of the remote gateway in parsed form
        :type url: :class:`~urlparse.ParseResult`
        :ivar user_agent: The User-Agent header to pass to the server
            (defaults to "Plasma/x.xx")
        :type user_agent: `str`

        """
        RemotingServiceBase.__init__(self, amf_version, **kwargs)
        self.url = urlparse(url)
        self.http_headers = self.BASE_HTTP_HEADERS.copy()
        if user_agent:
            self.user_agent = user_agent

    def addHTTPHeader(self, name, value):
        """
        Adds a header to the underlying HTTP connection.

        """
        self.http_headers[name] = value

    def removeHTTPHeader(self, name):
        """
        Deletes an HTTP header.

        """
        del self.http_headers[name]

    def execute(self):
        if self.logger:
            self.logger.debug('Sending POST request to %s', self.url.geturl())
            self.logger.debug('User-Agent: %s', self.user_agent)
            for key, value in self.http_headers.iteritems():
                self.logger.debug('%s: %s', key, value)

        # Make sure these requests won't get added to another batch
        requests = self.requests
        self.requests = []

        port = self.url.port or 80
        body = remoting.encode(self._createAMFRequest(requests),
                                   strict=self.strict).getvalue()

        factory = HTTPClientFactory(self.url.geturl(), 'POST', body,
                                    self.http_headers, self.user_agent)
        factory.deferred.addCallbacks(self._handleHTTPResponse,
                                      self._handleHTTPError,
                                      [factory],
                                      errbackArgs=[factory])
        factory.deferred.addCallback(remoting.decode, strict=self.strict)
        factory.deferred.addCallbacks(self._handleAMFResponse,
                                      self._handleAMFError,
                                      [requests],
                                      errbackArgs=[requests])
        reactor.connectTCP(self.url.hostname, port, factory)

    @staticmethod
    def _getHTTPHeader(http_headers, key):
        if key in http_headers:
            return http_headers[key][0]

    def _handleHTTPResponse(self, response_body, factory):
        """
        Handles the HTTP response from the remote gateway.

        :raise RemotingError: HTTP Gateway reported error status
        :raise RemotingError: Incorrect MIME type received

        """
        response_headers = factory.response_headers

        # Check content type
        content_type = self._getHTTPHeader(response_headers, 'content-type')
        if content_type != remoting.CONTENT_TYPE:
            if self.logger:
                self.logger.debug('Content-Type: %s', content_type)
            raise remoting.RemotingError(
                'Incorrect MIME type received. (got: %s)' % content_type)

        if self.logger:
            self.logger.debug('Content-Length: %s',
                self._getHTTPHeader(response_headers, 'content-length'))
            self.logger.debug('Server: %s',
                self._getHTTPHeader(response_headers, 'server'))
            self.logger.debug('Read %d bytes for the response',
                              len(response_body))
        return response_body

    def _handleHTTPError(self, error, factory):
        raise remoting.RemotingError('HTTP Gateway reported status %s %s' %
                                     (factory.status, factory.message))

    def _handleAMFResponse(self, response, requests):
        if remoting.APPEND_TO_GATEWAY_URL in response.headers:
            url_extension = response.headers[remoting.APPEND_TO_GATEWAY_URL]
            self.url = urlparse(self.url.geturl() + url_extension)
        elif remoting.REPLACE_GATEWAY_URL in response.headers:
            new_url = response.headers[remoting.REPLACE_GATEWAY_URL]
            self.url = urlparse(new_url)
        RemotingServiceBase._handleAMFResponse(self, response, requests)
