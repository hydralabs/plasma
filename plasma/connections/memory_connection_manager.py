import time

from connection import Connection
from connection_manager import ConnectionManager
from errors import ConnectionNotFoundError, DuplicateConnectionIdError

class MemoryConnectionManager(ConnectionManager):
    """
    Stores Connection objects in memory.
    """

    def __init__(self, *args, **kwargs):
        ConnectionManager.__init__(self, *args, **kwargs)
        self._connections = {}

    def create(self, id):
        """
        Create a new Connection.

        :param id: FLEX_CLIENT_ID of connection to load.
        :type  id: str
        :rtype: :class:`Connection`
        :raises: :class:`DuplicateConnectionIdError` when connection with id already exists.
        """
        if id in self._connections:
            raise DuplicateConnectionIdError("Connection id already exists.")
        return Connection(id, last_active=time.time())

    def load(self, id):
        """
        Loads a Connection.

        :param id: FLEX_CLIENT_ID of connection to load.
        :type  id: str
        :rtype: :class:`Connection`
        :raises: :class:`ConnectionNotFoundError` when connection does not exist
        """
        if id not in self._connections:
            raise ConnectionNotFoundError("Connection not found.")

        data = self._connections[id]
        return Connection(data['id'], last_active=data['last_active'],
            last_polled=data['last_polled'], flex_user=data['flex_user'],
            session=dict(data['session']))

    def save(self, connection):
        """
        Saves a Connection.

        :param connection: Connection to save
        :type  connection: :class:`Connection`
        """

        data = {
            'id': connection.id,
            'last_active': connection.last_active,
            'last_polled': connection.last_polled,
            'flex_user': connection.flex_user,
            'session': dict(connection.session)
        }

        self._connections[connection.id] = data

    def delete(self, id):
        """
        Deletes a Connection.

        :param id: FLEX_CLIENT_ID of connection to load.
        :type  id: str
        """
        if id in self._connections:
            del self._connections[id]

    def clean(self, id, cutoff):
        """        
        Delete connection if it is expired.

        :param id: FLEX_CLIENT_ID of connection to load.
        :type  id: str
        :param cutoff: connections with last_active values <
            this value will be deleted
        :type cutoff: float
        """
        if id in self._connections:
            if self._connetions[id]['last_active'] < cutoff:
                self.delete(id)

    def cleanAll(self, cutoff):
        """
        Delete expired connections.

        :param cutoff: connections with last_active values <
            this value will be deleted
        :type cutoff: float
        """

        # Use callLater to avoid blocking
        # if the number of connections
        # is high.
        #
        # Use keys() instead of iterkeys() in-case
        # another function changes self._connections.
        iter = self._connections.keys().__iter__()
        
        def _cleanLater():
           try:
               id = iter.next()
               self.clean(id, cutoff)
               defer.callLater(0, _cleanLater)
           except StopIteration:
               pass

        _cleanLater()
