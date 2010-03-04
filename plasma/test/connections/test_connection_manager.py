import time

from twisted.internet import defer
from twisted.trial import unittest

from plasma.connections.connection import Connection
from plasma.connections.errors import ConnectionNotFoundError, DuplicateConnectionIdError

class ConnectionManagerTestCase(unittest.TestCase):
    """
    Tests for ConnectionManager classes.
    """
    def setUp(self):
        self.manager = self.getConnectionManager()

    def assertConnectionId(self, connection, id):
        self.assertIsInstance(connection, Connection)
        self.assertEquals(id, connection.id)

    def assertLoadedConnection(self, connection, original_connection):
        self.assertEquals(original_connection.id, connection.id)
        self.assertNotEquals(id(original_connection), id(connection))
        self.assertEquals(original_connection.session, connection.session)

    def failCallback(self, result, message):
        self.fail(message)

    def test_loadBadRaisesConnectionNotFound(self):
        def _assertConnectionNotFound(failure):
            self.assertIsInstance(failure.value, ConnectionNotFoundError)

        d = defer.maybeDeferred(self.manager.load, 'non-existent id')
        d.addCallback(self.failCallback, "ConnectionNotFoundError not raised.")
        d.addErrback(_assertConnectionNotFound)

    def test_create(self):
        id = 'new id'
        d = defer.maybeDeferred(self.manager.create, id)
        d.addCallback(self.assertConnectionId, id)

    def test_createDuplicateRaisesDuplicateConnection(self):
        def _assertDuplicateConnection(failure):
            self.assertIsInstance(failure.value, DuplicateConnectionIdError)

        def _createDup(result, connection):
            d = defer.maybeDeferred(self.manager.create, connection.id)
            d.addCallback(self.failCallback, "DuplicateConnectionIdError not raised.")
            d.addErrback(_assertDuplicateConnection)

        def _saveConnection(connection):
            d = defer.maybeDeferred(self.manager.save, connection)
            d.addCallback(_createDup, connection)

        d = defer.maybeDeferred(self.manager.create, 'dup')
        d.addCallback(_saveConnection)

    def test_get(self):
        id = 'new id'
        d = defer.maybeDeferred(self.manager.get, id)
        d.addCallback(self.assertConnectionId, id)

    def test_loadAndSave(self):
        id = 'new id'

        def _loadConnection(result, original_connection):
            d = defer.maybeDeferred(self.manager.load, original_connection.id)
            d.addCallback(self.assertLoadedConnection, original_connection)

        def _saveConnection(connection):
            connection.session['foo'] = 'bar'
            d = defer.maybeDeferred(self.manager.save, connection)
            d.addCallback(_loadConnection, connection)

        
        d = defer.maybeDeferred(self.manager.create, id)
        d.addCallback(_saveConnection)

    def test_clean(self):
        id = 'new id'
        def _assertConnectionNotFound(failure):
            self.assertIsInstance(failure.value, ConnectionNotFoundError)

        def _assertCleaned(result, id):
            d = defer.maybeDeferred(self.manager.load, id)
            d.addCallback(self.failCallback, "Connection not cleaned.")
            d.addErrback(_assertConnectionNotFound)

        def _clean(result, connection):
            time.sleep(1)
            d = defer.maybeDeferred(self.manager.clean, connection.id, time.time())
            d.addCallback(_assertCleaned, connection.id)

        def _saveConnection(connection):
            d = defer.maybeDeferred(self.manager.save, connection)
            d.addCallback(_clean, connection)

        d = self.manager.get(id)
        d.addCallback(_saveConnection)

    def test_cleanAll(self):
        id = 'new id'

        def _assertConnectionNotFound(failure):
            self.assertIsInstance(failure.value, ConnectionNotFoundError)

        def _assertCleaned(result, id):
            d = defer.maybeDeferred(self.manager.load, id)
            d.addCallback(self.failCallback, "Connection not cleaned.")
            d.addErrback(_assertConnectionNotFound)
       
        def _cleanAll(result, connection):
            time.sleep(1)
            d = defer.maybeDeferred(self.manager.cleanAll, time.time())
            d.addCallback(_assertCleaned, connection.id)

        def _saveConnection(connection):
            d = defer.maybeDeferred(self.manager.save, connection)
            d.addCallback(_cleanAll, connection)

        d = self.manager.get(id)
        d.addCallback(_saveConnection)
