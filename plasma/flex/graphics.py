# Copyright (c) 2009 The Plasma Project.
# See LICENSE.txt for details.

"""
Support for C{flex.graphics} packages.
"""

import pyamf


class ImageSnapshot(object):
    """
    This class corresponds to C{mx.graphics.ImageSnapshot} on the client.
    Clients may choose to capture images and send them to the server via a
    RemoteObject call.

    @ivar contentType:  The content type for the image encoding format that
        was used to capture this snapshot.
    @type contentType: C{str}
    @ivar width: The image width in pixels.
    @type width: C{int}
    @ivar height: The image height in pixels.
    @type height: C{int}
    @ivar properties: Additional properties of the image.
    @type properties: C{dict}
    @ivar data: The encoded data representing the image snapshot.
    @type data: C{file} object
    @see: U{ImageSnapshot on Livedocs (external)
        <http://livedocs.adobe.com/flex/3/langref/mx/graphics/ImageSnapshot.html>}
    """

    def __init__(self, **kwargs):
        self.contentType = kwargs.pop('contentType', None)
        self.properties = kwargs.pop('properties', {})
        self.width = kwargs.pop('width', 0)
        self.height = kwargs.pop('height', 0)
        self.data = kwargs.pop('data', None)


pyamf.register_package(globals(), 'flex.graphics')
