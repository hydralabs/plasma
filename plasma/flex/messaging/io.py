# Copyright (c) 2009 The Plasma Project.
# See LICENSE.txt for details.

"""
Support for `flex.messaging.io`.

.. versionadded:: 0.1

"""


import pyamf

__all__ = ['ArrayCollection', 'ArrayList', 'ObjectProxy']


class ArrayCollection(list):
    """
    I represent the ActionScript 3 based class
    `flex.messaging.io.ArrayCollection` used in the Flex framework.

    The `ArrayCollection` class is a wrapper class that exposes an
    Array as a collection that can be accessed and manipulated using the
    methods and properties of the `ICollectionView` or `IList`
    interfaces in the Flex framework.

    .. seealso:: `ArrayCollection on Livedocs
        <http://livedocs.adobe.com/flex/201/langref/mx/collections/ArrayCollection.html>`_
            

    .. note:: This class does not implement the RemoteObject part of the
        documentation.

    :ivar length: [read-only] The number of items in this collection.
        .. versionadded:: 0.4
    :type length: `int`

    """

    class __amf__:
        external = True
        amf3 = True

        exclude = ('length',)

    def __init__(self, source=None):
        if source is not None:
            if isinstance(source, dict):
                raise TypeError('Cannot convert dicts to %s' % (self.__class__,))

            if hasattr(source, '__iter__'):
                self.extend(source)

    def __repr__(self):
        return "<flex.messaging.io.%s %s>" % (
            self.__class__.__name__, list.__repr__(self))

    def __readamf__(self, input):
        data = input.readObject()

        if hasattr(data, 'source'):
            data = data.source

        try:
            self.extend(data)
        except TypeError:
            raise pyamf.DecodeError('Unable to read a list '
                'when decoding %s' % (self.__class__.__name__,))

    def __writeamf__(self, output):
        output.encoder.writeList(
            list(self), use_references=True, use_proxies=False)

    def _get_length(self):
        return len(self)

    def _set_length(self, length):
        raise AttributeError("Property length is read-only")

    length = property(_get_length, _set_length)

    def addItem(self, item):
        """
        Adds the specified item to the end of the list.

        :param item: The object to add to the collection.
        :type item: `mixed`.

        """
        self.append(item)

    def addItemAt(self, item, index):
        """
        Adds the item at the specified index.

        :param item: The object to add to the collection.
        :type item: `mixed`
        :param index: The index at which to place the item.
        :raise IndexError: If index is less than 0 or greater than the length
            of the list.

        """
        if index < 0:
            raise IndexError

        if index > len(self):
            raise IndexError

        self.insert(index, item)

    def getItemAt(self, index, prefetch=0):
        """
        Gets the item at the specified index.

        :param index: The index in the list from which to retrieve the item.
        :type index: `int`
        :param prefetch: This param is ignored and is only here as part of the
            interface.
        :raise IndexError: if `index < 0` or `index >= length`
        :return: The item at index `index`.
        :rtype: `mixed`.

        """
        if index < 0:
            raise IndexError

        if index > len(self):
            raise IndexError

        return self.__getitem__(index)

    def getItemIndex(self, item):
        """
        Returns the index of the item if it is in the list such that
        `getItemAt(index) == item`.

        :param item: The item to find.
        :type item: `mixed`.
        :return: The index of the item or -1 if the item is not in the list.
        :rtype: `int`

        """
        try:
            return self.index(item)
        except ValueError:
            return -1

    def removeAll(self):
        """
        Removes all items from the list.
        """
        while len(self) > 0:
            self.pop()

    def removeItemAt(self, index):
        """
        Removes the item at the specified index and returns it. Any items that
        were after this index are now one index earlier.

        :param index: The index from which to remove the item.
        :return: The item that was removed.
        :rtype: `mixed`.
        :raise IndexError: If index is less than 0 or greater than length.

        """
        if index < 0:
            raise IndexError

        if index > len(self):
            raise IndexError

        x = self[index]

        del self[index]

        return x

    def setItemAt(self, item, index):
        """
        Places the item at the specified index. If an item was already at that
        index the new item will replace it and it will be returned.

        :param item: The new item to be placed at the specified index.
        :type item: `mixed`.
        :param index: The index at which to place the item.
        :type index: `int`
        :return: The item that was replaced, or `None`.
        :rtype: `mixed` or `None`.
        :raise IndexError: If index is less than 0 or greater than length.

        """
        if index < 0:
            raise IndexError

        if index > len(self):
            raise IndexError

        tmp = self.__getitem__(index)
        self.__setitem__(index, item)

        return tmp

    def toArray(self):
        """
        Returns an Array that is populated in the same order as the `IList`
        implementation.

        :return: The array.
        :rtype: `list`

        """
        return self


class ArrayList(ArrayCollection):
    """
    .. seealso:: `ArrayList on LiveDocs
        <http://livedocs.adobe.com/flex/gumbo/langref/mx/collections/ArrayList.html>`_
        
    """

    class __amf__:
        external = True
        amf3 = True


class ObjectProxy(object):
    """
    I represent the ActionScript 3 based class
    :class:`flex.messaging.io.ObjectProxy` used in the Flex framework.
    Flex's :class:`~ObjectProxy` class allows an anonymous, dynamic
    ActionScript Object to be bindable and report change events.

    .. seealso:: `ObjectProxy on Livedocs
        <http://livedocs.adobe.com/flex/201/langref/mx/utils/ObjectProxy.html>`_

    """

    class __amf__:
        external = True
        amf3 = True

    def __init__(self, object=None):
        if object is None:
            self._amf_object = pyamf.ASObject()
        else:
            self._amf_object = object

    def __repr__(self):
        return "<flex.messaging.io.ObjectProxy %r>" % self._amf_object

    def __getattr__(self, name):
        return getattr(self.__dict__['_amf_object'], name)

    def __setattr__(self, name, value):
        if name == '_amf_object':
            self.__dict__['_amf_object'] = value
        else:
            setattr(self._amf_object, name, value)

    def __readamf__(self, input):
        self._amf_object = input.readObject()

    def __writeamf__(self, output):
        output.writeObject(self._amf_object, use_proxies=False)


def unproxy_object(obj):
    """Returns the unproxied version of the object."""
    if isinstance(obj, ArrayCollection):
        return list(obj)
    elif isinstance(obj, ObjectProxy):
        return obj._amf_object

    return obj


if pyamf.__version__ < (1, 0):
    from pyamf import flex

    pyamf.unregister_class(flex.ObjectProxy)
    pyamf.unregister_class(flex.ArrayCollection)


pyamf.register_package(globals(), package='flex.messaging.io')
