# Copyright The Plasma Project.
# See LICENSE.txt for details.

"""
Support for `flex.messaging` namespace.

.. versionadded:: 0.1

"""

# this is required because PyAMF also registers class aliases for
# flex.messaging.* so we force the import here so that we can override the
# registered classes with our own implementation.
import pyamf.flex.messaging