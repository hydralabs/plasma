class Connection(object):
    """
    A connection tracks information about an individual
    client's state.

    :ivar id: the FLEX_CLIENT_ID of the connected user
    :type id: str
    :ivar last_active: timestamp when the user last connected to the server
    :type last_active: float
    :ivar last_polled: timestamp when the client last polled for messages
    :type last_polled: float
    :ivar flex_user: username of authenticated user
    :type flex_user: str
    :ivar session: user set session values
    :type session: dict
    """

    def __init__(self, id, last_active=None, last_polled=None,
        flex_user=None, session=None):
        self.id = id
        self.last_active = last_active
        self.last_polled = last_polled
        self.flex_user = flex_user

        if session is None:
            session = {}
        self.session = session

    def touch(self):
        """
        Updates last_active to now.
        """
        self.last_active = time.time()

    def touchPolled(self):
        """
        Updates last_polled to now.
        """
        self.last_polled = time.time()
