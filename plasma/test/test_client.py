# -*- coding: utf-8 -*-
#
# Copyright The Plasma Project.
# See LICENSE.txt for details.
from twisted.web.server import Site
from twisted.internet.defer import inlineCallbacks, Deferred

"""Tests for Remoting client."""

import logging

from nose.tools import eq_, raises, set_trace
from nose.twistedtools import reactor, deferred
from pyamf import remoting
from pyamf.remoting.gateway.twisted import TwistedGateway
import pyamf

from plasma import client


def setup():
    global gateway
    gateway = TwistedGateway(logger=logging)
    gateway.isLeaf = True
    site = Site(gateway)
    reactor.listenTCP(11111, site)


def teardown():
    reactor.stop()


def service_uppercase(request, string):
    return string.upper()


class ServiceMethodProxyTestCase():
    def test_create(self):
        x = client.ServiceMethodProxy('a', 'b')

        eq_(x.service, 'a')
        eq_(x.name, 'b')

    def test_call(self):
        tc = self

        class TestService(object):
            def __init__(self, s, args):
                self.service = s
                self.args = args

            def _call(self, service, *args):
                tc.assertTrue(self.service, service)
                tc.assertTrue(self.args, args)

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
        gateway.addService(service_uppercase, 'uppercase')

    @classmethod
    def teardown_class(cls):
        gateway.removeService(service_uppercase)
    
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
        y = x.getService('uppercase')

        assert isinstance(y, client.ServiceProxy)
        assert hasattr(y, '__call__')
        eq_(y._name, 'uppercase')
        
        deferred = y('teststring')
        assert isinstance(deferred, Deferred)
        result = yield deferred
        eq_(result, 'TESTSTRING')

#    def test_add_request(self):
#        gw = client.HTTPRemotingService('http://spameggs.net')
#
#        eq_(gw.request_number, 1)
#        eq_(gw.requests, [])
#        service = gw.getService('baz')
#        wrapper = gw.addRequest(service, 1, 2, 3)
#
#        eq_(gw.requests, [wrapper])
#        eq_(wrapper.gw, gw)
#        eq_(gw.request_number, 2)
#        eq_(wrapper.id, '/1')
#        eq_(wrapper.service, service)
#        eq_(wrapper.args, (1, 2, 3))
#
#        # add 1 arg
#        wrapper2 = gw.addRequest(service, None)
#
#        eq_(gw.requests, [wrapper, wrapper2])
#        eq_(wrapper2.gw, gw)
#        eq_(gw.request_number, 3)
#        eq_(wrapper2.id, '/2')
#        eq_(wrapper2.service, service)
#        eq_(wrapper2.args, (None,))
#
#        # add no args
#        wrapper3 = gw.addRequest(service)
#
#        eq_(gw.requests, [wrapper, wrapper2, wrapper3])
#        eq_(wrapper3.gw, gw)
#        eq_(gw.request_number, 4)
#        eq_(wrapper3.id, '/3')
#        eq_(wrapper3.service, service)
#        eq_(wrapper3.args, tuple())
#
#    def test_remove_request(self):
#        gw = client.RemotingService('http://spameggs.net')
#        eq_(gw.requests, [])
#
#        service = gw.getService('baz')
#        wrapper = gw.addRequest(service, 1, 2, 3)
#        eq_(gw.requests, [wrapper])
#
#        gw.removeRequest(wrapper)
#        eq_(gw.requests, [])
#
#        wrapper = gw.addRequest(service, 1, 2, 3)
#        eq_(gw.requests, [wrapper])
#
#        gw.removeRequest(service, 1, 2, 3)
#        eq_(gw.requests, [])
#
#        self.assertRaises(LookupError, gw.removeRequest, service, 1, 2, 3)
#
#    def test_get_request(self):
#        gw = client.RemotingService('http://spameggs.net')
#
#        service = gw.getService('baz')
#        wrapper = gw.addRequest(service, 1, 2, 3)
#
#        wrapper2 = gw.getRequest(str(wrapper))
#        eq_(wrapper, wrapper2)
#
#        wrapper2 = gw.getRequest('/1')
#        eq_(wrapper, wrapper2)
#
#        wrapper2 = gw.getRequest(wrapper.id)
#        eq_(wrapper, wrapper2)
#
#    def test_get_amf_request(self):
#        gw = client.RemotingService('http://example.org', pyamf.AMF3)
#
#        service = gw.getService('baz')
#        method_proxy = service.gak
#        wrapper = gw.addRequest(method_proxy, 1, 2, 3)
#
#        envelope = gw.getAMFRequest([wrapper])
#
#        eq_(envelope.amfVersion, pyamf.AMF3)
#        eq_(envelope.keys(), ['/1'])
#
#        request = envelope['/1']
#        eq_(request.target, 'baz.gak')
#        eq_(request.body, [1, 2, 3])
#
#        envelope2 = gw.getAMFRequest(gw.requests)
#
#        eq_(envelope2.amfVersion, pyamf.AMF3)
#        eq_(envelope2.keys(), ['/1'])
#
#        request = envelope2['/1']
#        eq_(request.target, 'baz.gak')
#        eq_(request.body, [1, 2, 3])
#
#    def test_execute_single(self):
#        gw = client.RemotingService('http://example.org/x/y/z')
#        dc = DummyConnection()
#        gw.connection = dc
#
#        dc.tc = self
#        dc.expected_headers = {'Content-Type': remoting.CONTENT_TYPE,
#                               'User-Agent': client.DEFAULT_USER_AGENT}
#
#        service = gw.getService('baz', auto_execute=False)
#        wrapper = service.gak()
#
#        response = DummyResponse(200, '\x00\x00\x00\x00\x00\x01\x00\x0b/1/onRe'
#            'sult\x00\x04null\x00\x00\x00\x00\x00\x02\x00\x05hello', {
#            'Content-Type': 'application/x-amf', 'Content-Length': 50})
#        response.tc = self
#
#        dc.expected_url = '/x/y/z'
#        dc.expected_value = '\x00\x00\x00\x00\x00\x01\x00\x07baz.gak\x00' + \
#            '\x02/1\x00\x00\x00\x00\x0a\x00\x00\x00\x00'
#        dc.response = response
#
#        gw.execute_single(wrapper)
#        eq_(gw.requests, [])
#
#        wrapper = service.gak()
#
#        response = DummyResponse(200, '\x00\x00\x00\x00\x00\x01\x00\x0b/2/onRe'
#            'sult\x00\x04null\x00\x00\x00\x00\x00\x02\x00\x05hello', {
#            'Content-Type': 'application/x-amf'})
#        response.tc = self
#
#        dc.expected_url = '/x/y/z'
#        dc.expected_value = '\x00\x00\x00\x00\x00\x01\x00\x07baz.gak\x00' + \
#            '\x02/2\x00\x00\x00\x00\n\x00\x00\x00\x00'
#        dc.response = response
#
#        gw.execute_single(wrapper)
#
#    def test_execute(self):
#        gw = client.RemotingService('http://example.org/x/y/z')
#        dc = DummyConnection()
#        gw.connection = dc
#
#        dc.tc = self
#        dc.expected_headers = {'Content-Type': 'application/x-amf',
#                               'User-Agent': client.DEFAULT_USER_AGENT}
#
#        baz = gw.getService('baz', auto_execute=False)
#        spam = gw.getService('spam', auto_execute=False)
#        wrapper = baz.gak()
#        wrapper2 = spam.eggs()
#
#        response = DummyResponse(200, '\x00\x00\x00\x00\x00\x02\x00\x0b/1/onRe'
#            'sult\x00\x04null\x00\x00\x00\x00\x00\x02\x00\x05hello\x00\x0b/2/o'
#            'nResult\x00\x04null\x00\x00\x00\x00\x00\x02\x00\x05hello', {
#                'Content-Type': 'application/x-amf'})
#        response.tc = self
#
#        dc.expected_url = '/x/y/z'
#        dc.expected_value = ('\x00\x00\x00\x00\x00\x02\x00\x07baz.gak\x00\x02'
#            '/1\x00\x00\x00\x00\n\x00\x00\x00\x00\x00\tspam.eggs\x00\x02/2'
#            '\x00\x00\x00\x00\n\x00\x00\x00\x00')
#        dc.response = response
#
#        gw.execute()
#        eq_(gw.requests, [])
#
#    def test_get_response(self):
#        gw = client.RemotingService('http://example.org/amf-gateway')
#        dc = DummyConnection()
#        gw.connection = dc
#
#        response = DummyResponse(200, '\x00\x00\x00\x00\x00\x00', {
#            'Content-Type': 'application/x-amf'
#        })
#
#        dc.response = response
#
#        gw._getResponse()
#
#        response = DummyResponse(404, '', {})
#        dc.response = response
#
#        self.assertRaises(remoting.RemotingError, gw._getResponse)
#
#        # bad content type
#        response = DummyResponse(200, '\x00\x00\x00\x00\x00\x00',
#            {'Content-Type': 'text/html'})
#        dc.response = response
#
#        self.assertRaises(remoting.RemotingError, gw._getResponse)
#
#    def test_credentials(self):
#        gw = client.RemotingService('http://example.org/amf-gateway')
#
#        self.assertFalse('Credentials' in gw.headers)
#        gw.setCredentials('spam', 'eggs')
#        self.assertTrue('Credentials' in gw.headers)
#        eq_(gw.headers['Credentials'],
#            {'userid': u'spam', 'password': u'eggs'})
#
#        envelope = gw.getAMFRequest([])
#        self.assertTrue('Credentials' in envelope.headers)
#
#        cred = envelope.headers['Credentials']
#
#        eq_(cred, gw.headers['Credentials'])
#
#    def test_append_url_header(self):
#        gw = client.RemotingService('http://example.org/amf-gateway')
#        dc = DummyConnection()
#        gw.connection = dc
#
#        response = DummyResponse(200, '\x00\x00\x00\x01\x00\x12AppendToGatewayUrl'
#            '\x01\x00\x00\x00\x00\x02\x00\x05hello\x00\x00', {
#            'Content-Type': 'application/x-amf'})
#
#        dc.response = response
#
#        response = gw._getResponse()
#        eq_(gw.original_url, 'http://example.org/amf-gatewayhello')
#
#    def test_replace_url_header(self):
#        gw = client.RemotingService('http://example.org/amf-gateway')
#        dc = DummyConnection()
#        gw.connection = dc
#
#        response = DummyResponse(200, '\x00\x00\x00\x01\x00\x11ReplaceGatewayUrl'
#            '\x01\x00\x00\x00\x00\x02\x00\x10http://spam.eggs\x00\x00', {
#            'Content-Type': 'application/x-amf'})
#
#        dc.response = response
#
#        response = gw._getResponse()
#        eq_(gw.original_url, 'http://spam.eggs')
#
#    def test_close_http_response(self):
#        gw = client.RemotingService('http://example.org/amf-gateway')
#        dc = DummyConnection()
#        gw.connection = dc
#        dc.response = DummyResponse(200, '\x00\x00\x00\x01\x00\x11ReplaceGatewayUrl'
#            '\x01\x00\x00\x00\x00\x02\x00\x10http://spam.eggs\x00\x00', {
#            'Content-Type': 'application/x-amf'})
#
#        gw._getResponse()
#        assert dc.response.closed is True
#
#    def test_add_http_header(self):
#        gw = client.RemotingService('http://example.org/amf-gateway')
#
#        eq_(gw.http_headers, {})
#
#        gw.addHTTPHeader('ETag', '29083457239804752309485')
#
#        eq_(gw.http_headers, {
#            'ETag': '29083457239804752309485'
#        })
#
#    @raises(KeyError)
#    def test_remove_http_header(self):
#        gw = client.RemotingService('http://example.org/amf-gateway')
#
#        gw.http_headers = {
#            'Set-Cookie': 'foo-bar'
#        }
#
#        gw.removeHTTPHeader('Set-Cookie')
#
#        eq_(gw.http_headers, {})
#        gw.removeHTTPHeader('foo-bar')
#
#    def test_http_request_headers(self):
#        gw = client.RemotingService('http://example.org/amf-gateway')
#        dc = DummyConnection()
#        gw.connection = dc
#        dc.tc = self
#        dc.expected_url = '/amf-gateway'
#        dc.expected_value = '\x00\x00\x00\x00\x00\x00'
#
#        gw.addHTTPHeader('ETag', '29083457239804752309485')
#        dc.expected_headers = {
#            'ETag': '29083457239804752309485',
#            'Content-Type': 'application/x-amf',
#            'User-Agent': gw.user_agent
#        }
#
#        dc.response = DummyResponse(200, '\x00\x00\x00\x01\x00\x11ReplaceGatewayUrl'
#            '\x01\x00\x00\x00\x00\x02\x00\x10http://spam.eggs\x00\x00', {
#            'Content-Type': 'application/x-amf'
#        })
#
#        gw.execute()
#        self.assertTrue(dc.response.closed, True)
#
#    def test_empty_content_length(self):
#        gw = client.RemotingService('http://example.org/amf-gateway')
#        dc = DummyConnection()
#        gw.connection = dc
#
#        http_response = DummyResponse(200, '\x00\x00\x00\x01\x00\x11ReplaceGatewayUrl'
#            '\x01\x00\x00\x00\x00\x02\x00\x10http://spam.eggs\x00\x00', {
#            'Content-Type': 'application/x-amf',
#            'Content-Length': ''
#        })
#
#        dc.response = http_response
#        gw._getResponse()
#
#        self.assertTrue(http_response.closed)
#
#    def test_bad_content_length(self):
#        gw = client.RemotingService('http://example.org/amf-gateway')
#        dc = DummyConnection()
#        gw.connection = dc
#
#        # test a really borked content-length header
#        http_response = DummyResponse(200, '\x00\x00\x00\x01\x00\x11ReplaceGatewayUrl'
#            '\x01\x00\x00\x00\x00\x02\x00\x10http://spam.eggs\x00\x00', {
#            'Content-Type': 'application/x-amf',
#            'Content-Length': 'asdfasdf'
#        })
#
#        dc.response = http_response
#        self.assertRaises(ValueError, gw._getResponse)
