# Copyright The Plasma Project.
# See LICENSE.txt for details.

"""
Support for `flex.graphics` packages.

.. versionadded:: 0.1

"""

import pyamf


class ImageSnapshot(object):
    """
    This class corresponds to `mx.graphics.ImageSnapshot` on the client.
    Clients may choose to capture images and send them to the server via a
    RemoteObject call.

    :ivar contentType:  The content type for the image encoding format that
        was used to capture this snapshot.
    :type contentType: `str`
    :ivar width: The image width in pixels.
    :type width: `int`
    :ivar height: The image height in pixels.
    :type height: `int`
    :ivar properties: Additional properties of the image.
    :type properties: `dict`
    :ivar data: The encoded data representing the image snapshot.
    :type data: `file` object

    """

    def __init__(self, **kwargs):
        self.contentType = kwargs.pop('contentType', None)
        self.properties = kwargs.pop('properties', {})
        self.width = kwargs.pop('width', 0)
        self.height = kwargs.pop('height', 0)
        self.data = kwargs.pop('data', None)


pyamf.register_package(globals(), 'flex.graphics')
