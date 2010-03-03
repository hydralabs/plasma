from plasma.connections.memory_connection_manager import MemoryConnectionManager

from test_connection_manager import ConnectionManagerTestCase

class MemoryConnectionManagerTestCase(ConnectionManagerTestCase):
    """
    Run ConnectionManagerTestCase
    using a MemoryConnectionManager.
    """

    def getConnectionManager(self):
        return MemoryConnectionManager()
