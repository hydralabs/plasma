# Copyright (c) 2009 The Plasma Project.
# See LICENSE.txt for details.

"""
Support for `flex.messaging.io`.

.. versionadded:: 0.1

"""


import pyamf.flex

__all__ = ['ArrayCollection', 'ArrayList', 'ObjectProxy']


ArrayCollection = pyamf.flex.ArrayCollection
ObjectProxy = pyamf.flex.ObjectProxy


class ArrayList(ArrayCollection):
    """
    .. seealso:: `ArrayList on LiveDocs
        <http://livedocs.adobe.com/flex/gumbo/langref/mx/collections/ArrayList.html>`_
    """

    class __amf__:
        external = True
        amf3 = True

    def __repr__(self):
        return "<flex.messaging.io.ArrayList %s>" % list.__repr__(self)


pyamf.register_package(globals(), package='flex.messaging.io')
