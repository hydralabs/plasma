# -*- coding: utf-8 -*-
#
# Copyright The Plasma Project.
# See LICENSE.txt for details.
from pyamf.remoting.gateway import authenticate

"""Tests for Remoting client."""

import logging

from nose.tools import eq_, raises, set_trace
from nose.twistedtools import reactor, deferred
from twisted.web.server import Site
from twisted.internet.defer import Deferred, inlineCallbacks
from pyamf.remoting import RemotingError
from pyamf.remoting.gateway.twisted import TwistedGateway
import pyamf

from plasma import client


def setup():
    global gateway
    gateway = TwistedGateway(logger=logging)
    gateway.isLeaf = True
    site = Site(gateway)
    reactor.listenTCP(11111, site)
    pyamf.add_error_class(RegisteredError, u'RegisteredError')


def teardown():
    pyamf.remove_error_class(RegisteredError)
    reactor.stop()


def simple_authenticator(userid, password):
    return userid == 'testuser' and password == 'secret'


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


class ServiceMethodProxyTestCase():
    def test_create(self):
        x = client.ServiceMethodProxy('a', 'b')

        eq_(x.service, 'a')
        eq_(x.name, 'b')

    def test_call(self):
        class TestService(object):
            def __init__(self, s, args):
                self.service = s
                self.args = args

            def _call(self, service, *args):
                eq_(self.service, service)
                eq_(self.args, args)

        x = client.ServiceMethodProxy(None, None)
        ts = TestService(x, [1, 2, 3])
        x.service = ts

        x(1, 2, 3)

    def test_str(self):
        x = client.ServiceMethodProxy('spam', 'eggs')
        eq_(str(x), 'spam.eggs')

        x = client.ServiceMethodProxy('spam', None)
        eq_(str(x), 'spam')


class TestRemotingService():
    @classmethod
    def setup_class(cls):
        gateway.addService(FooService, 'foo')

    @classmethod
    def teardown_class(cls):
        gateway.removeService(FooService)

    @raises(TypeError)
    def test_create_noargs(self):
        client.HTTPRemotingService()

    def test_url(self):
        service = client.HTTPRemotingService('http://example.org')

        eq_(service.url.scheme, 'http')
        eq_(service.url.hostname, 'example.org')

    def test_amf3(self):
        service = client.HTTPRemotingService('http://example.org', pyamf.AMF3)
        eq_(service.amf_version, pyamf.AMF3)

    def test_port(self):
        service = client.HTTPRemotingService('http://example.org:8080')
        eq_(service.url.hostname, 'example.org')
        eq_(service.url.port, 8080)

    @deferred(2)
    @inlineCallbacks
    def test_single_request(self):
        x = client.HTTPRemotingService('http://127.0.0.1:11111')
        y = x.getService('foo.uppercase')

        assert isinstance(y, client.ServiceProxy)
        eq_(y._name, 'foo.uppercase')

        deferred = y('teststring')
        assert isinstance(deferred, Deferred)
        result = yield deferred
        eq_(result, 'TESTSTRING')

    @deferred(2)
    @inlineCallbacks
    def test_service_method(self):
        x = client.HTTPRemotingService('http://127.0.0.1:11111')

        y = x.getService('foo')
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
        x = client.HTTPRemotingService('http://127.0.0.1:11111')
        y = x.getService('foo.dummy')

        try:
            yield y()
        except RemotingError, e:
            assert e.message == 'test error', 'Wrong error message'
        else:
            assert False, 'Expected a RemotingError'

    @deferred(2)
    @inlineCallbacks
    def test_registered_error(self):
        x = client.HTTPRemotingService('http://127.0.0.1:11111')
        y = x.getService('foo.reg_error')

        try:
            yield y()
        except RegisteredError, e:
            eq_(str(e), 'I am registered')
        else:
            assert False, 'Expected a RegisteredError'

    @deferred(2)
    @inlineCallbacks
    def test_batch_call(self):
        x = client.HTTPRemotingService('http://127.0.0.1:11111')
        upper = x.getService('foo.uppercase')
        regerror = x.getService('foo.reg_error')

        d_upper1 = x.addRequest(upper, 'to upper case')
        d_regerror = x.addRequest(regerror)
        d_upper2 = x.addRequest(upper, 'this too')
        x.execute()

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
        x = client.HTTPRemotingService('http://127.0.0.1:11111')
        x.setCredentials('testuser', 'secret')
        y = x.getService('foo')

        result = yield y.needs_auth()
        eq_(result, 'success')

    @deferred(2)
    @inlineCallbacks
    def test_wrong_credentials(self):
        x = client.HTTPRemotingService('http://127.0.0.1:11111')
        x.setCredentials('testuser', 'wrong')
        y = x.getService('foo')

        try:
            yield y.needs_auth()
        except RemotingError, e:
            eq_(str(e), 'Authentication failed')
        else:
            assert False, 'Expected a RemotingError'

    def test_remove_request(self):
        x = client.HTTPRemotingService('http://127.0.0.1:11111')
        upper = x.getService('foo.uppercase')
        
        req1 = x.addRequest(upper, 'str')
        x.removeRequest(req1)
        eq_(len(x.requests), 0)
