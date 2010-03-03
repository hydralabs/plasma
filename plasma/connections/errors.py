"""
Errors used by classes in the connection module.
"""

class ConnectionNotFoundError(Exception):
    """
    Raised when a ConnectionManager tries
    to load a Connection that does not exist.
    """
    pass

class DuplicateConnectionIdError(Exception):
    """
    Raised when a ConnectionManager tries
    to create a Connection with an id that
    already exists.
    """
