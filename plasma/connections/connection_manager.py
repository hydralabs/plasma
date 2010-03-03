class ConnectionManager(object):
    """
    Loads and saves Connection objects.
    """

    def _handleLoadFailure(failure, id):
        """
        If self.load fails with a
        ConnectionNotFoundError, 
        create a new connection,
        otherwise pass the error on.
        """
        failure.trap(ConnectionNotFoundError)
        return defer.maybeDeferred(self.create, id)

    def get(self, id):
        """
        Tries to load a Connection.

        If the Connection does not exist,
        create a new Connection.
   
        :param id: FLEX_CLIENT_ID of connection
        :type  id: str
        :rtype: :class:`Deferred`
        """

        d = defer.maybeDeferred(self.load, id)
        d.addErrback(self._handleLoadFailure, id)
        return d
