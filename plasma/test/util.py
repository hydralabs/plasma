# Copyright The Plasma Project.
# See LICENSE.txt for details.

"""
Test helpers and classes
"""

import inspect


def dict_for_slots(obj):
    """
    """
    slots = []

    for cls in inspect.getmro(obj.__class__):
        if hasattr(cls, '__slots__'):
            slots += cls.__slots__

    return dict(zip(slots, [getattr(obj, x) for x in slots]))