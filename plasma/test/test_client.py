# -*- coding: utf-8 -*-
#
# Copyright The Plasma Project.
# See LICENSE.txt for details.

"""Tests for Remoting client."""

import logging

from nose.tools import eq_, raises
from nose.twistedtools import reactor, deferred
from twisted.web.server import Site
from twisted.web.resource import Resource
from twisted.internet.defer import Deferred, inlineCallbacks
from pyamf.remoting import RemotingError, Envelope
from pyamf.remoting.gateway.twisted import TwistedGateway
from pyamf.remoting.gateway import authenticate
from pyamf import remoting
import pyamf

from plasma import client


def setup():
    global gateway
    gateway = TwistedGateway(logger=logging)
    gateway.isLeaf = True
    root = Resource()
    root.putChild('gw', gateway)
    root.putChild('bad', BadResource())
    root.putChild('badtype', BadContentTypeResource())

    site = Site(root)
    reactor.listenTCP(11111, site)
    pyamf.add_error_class(RegisteredError, u'RegisteredError')


def teardown():
    pyamf.remove_error_class(RegisteredError)
    reactor.stop()


def simple_authenticator(userid, password):
    return userid == 'testuser' and password == 'secret'


class BadResource(Resource):
    def render_POST(self, request):
        request.setResponseCode(500)
        return 'ERROR'


class BadContentTypeResource(Resource):
    def render_POST(self, request):
        return 'hello'


class FooService(object):
    def uppercase(self, request, string):
        return string.upper()

    def dummy(self, request):
        raise DummyError('test error')

    def reg_error(self, request):
        raise RegisteredError('I am registered')

    def needs_auth(self, request):
        return 'success'
    needs_auth = authenticate(needs_auth, simple_authenticator)


class DummyError(Exception):
    pass


class RegisteredError(Exception):
    pass


@raises(NotImplementedError)
def testRemotingBaseInstance():
    """
    Make sure that RemotingServiceBase.execute() raises NotImplementedError.

    """
    client.RemotingServiceBase().execute()


@raises(TypeError)
def test_create_noargs():
    """
    Make sure that HTTPRemotingService requires an URL.
    
    """
    client.HTTPRemotingService()


def test_url():
    service = client.HTTPRemotingService('http://example.org')

    eq_(service.url.scheme, 'http')
    eq_(service.url.hostname, 'example.org')


def test_amf3():
    service = client.HTTPRemotingService('http://example.org', pyamf.AMF3)
    eq_(service.amf_version, pyamf.AMF3)


def test_port():
    service = client.HTTPRemotingService('http://example.org:8080')
    eq_(service.url.hostname, 'example.org')
    eq_(service.url.port, 8080)


@raises(RemotingError)
@deferred()
def test_server_error():
    service = client.HTTPRemotingService('http://127.0.0.1:11111/bad',
                                         logger=logging)
    y = service.getService('foo')
    return y.bar()


@raises(RemotingError)
@deferred()
def test_bad_content_type():
    service = client.HTTPRemotingService('http://127.0.0.1:11111/badtype',
                                         logger=logging)
    y = service.getService('foo')
    return y.bar()


class TestHTTPRemotingServiceDry(object):
    def setup(self):
        self.service = client.HTTPRemotingService('http://example.org')
    
    def testAddPersistentHeaders(self):
        envelope = Envelope()
        persistent_headers = {'TestHeader': 9, 'AnotherTestHeader': 'test'}
        envelope.headers[remoting.REQUEST_PERSISTENT_HEADER] = \
            persistent_headers
        self.service._handleAMFResponse(envelope, [])
        eq_(self.service.headers, persistent_headers)

    def testChangeGatewayURL(self):
        envelope = Envelope()
        envelope.headers[remoting.REPLACE_GATEWAY_URL] = 'http://example.net'
        self.service._handleAMFResponse(envelope, [])
        eq_(self.service.url.hostname, 'example.net')

    def testAppendToGatewayURL(self):
        envelope = Envelope()
        envelope.headers[remoting.APPEND_TO_GATEWAY_URL] = \
            '/path/flash/gateway'
        eq_(self.service.url.path, '')
        self.service._handleAMFResponse(envelope, [])
        eq_(self.service.url.path, '/path/flash/gateway')

    def testAddRemoveHTTPHeader(self):
        self.service.addHTTPHeader('Referer', 'http://example.net/path')
        eq_(self.service.http_headers.get('Referer'),
            'http://example.net/path')
        self.service.removeHTTPHeader('Referer')
        assert 'Referer' not in self.service.http_headers

    @raises(TypeError)
    def testGetServiceWrongType(self):
        foo = self.service.getService('foo')
        self.service.getService(foo)


class TestHTTPRemotingServiceLive():
    @classmethod
    def setup_class(cls):
        gateway.addService(FooService, 'foo')

    @classmethod
    def teardown_class(cls):
        gateway.removeService(FooService)

    def setup(self):
        self.service = client.HTTPRemotingService('http://127.0.0.1:11111/gw',
                                                  logger=logging)

    @deferred(2)
    @inlineCallbacks
    def test_single_request(self):
        y = self.service.getService('foo.uppercase')

        assert isinstance(y, client.ServiceProxy)
        eq_(y._name, 'foo.uppercase')

        deferred = y('teststring')
        assert isinstance(deferred, Deferred)
        result = yield deferred
        eq_(result, 'TESTSTRING')

    @deferred(2)
    @inlineCallbacks
    def test_service_method(self):
        y = self.service.getService('foo')
        assert isinstance(y, client.ServiceProxy)

        uppercase = y.uppercase
        eq_(uppercase.name, 'uppercase')

        deferred = uppercase('teststring')
        assert isinstance(deferred, Deferred)
        result = yield deferred
        eq_(result, 'TESTSTRING')


    @deferred(2)
    @inlineCallbacks
    def test_dummy_error(self):
        y = self.service.getService('foo.dummy')

        try:
            yield y()
        except RemotingError, e:
            assert e.message == 'test error', 'Wrong error message'
        else:
            assert False, 'Expected a RemotingError'

    @deferred(2)
    @inlineCallbacks
    def test_registered_error(self):
        y = self.service.getService('foo.reg_error')

        try:
            yield y()
        except RegisteredError, e:
            eq_(str(e), 'I am registered')
        else:
            assert False, 'Expected a RegisteredError'

    @deferred(2)
    @inlineCallbacks
    def test_batch_call(self):
        upper = self.service.getService('foo.uppercase')
        regerror = self.service.getService('foo.reg_error')

        d_upper1 = self.service.addRequest(upper, 'to upper case')
        d_regerror = self.service.addRequest(regerror)
        d_upper2 = self.service.addRequest(upper, 'this too')
        self.service.execute()

        result1 = yield d_upper1
        eq_(result1, 'TO UPPER CASE')
        try:
            yield d_regerror
        except RegisteredError:
            pass
        else:
            assert False, 'Expected a RegisteredError'
        result2 = yield d_upper2
        eq_(result2, 'THIS TOO')

    @deferred(2)
    @inlineCallbacks
    def test_auth(self):
        self.service.setCredentials('testuser', 'secret')
        y = self.service.getService('foo')

        result = yield y.needs_auth()
        eq_(result, 'success')

    @deferred(2)
    @inlineCallbacks
    def test_wrong_credentials(self):
        self.service.setCredentials('testuser', 'wrong')
        y = self.service.getService('foo')

        try:
            yield y.needs_auth()
        except RemotingError, e:
            eq_(str(e), 'Authentication failed')
        else:
            assert False, 'Expected a RemotingError'

    def test_remove_request(self):
        upper = self.service.getService('foo.uppercase')

        req1 = self.service.addRequest(upper, 'str')
        self.service.removeRequest(req1)
        eq_(len(self.service.requests), 0)
