# Copyright (c) 2007-2009 The Plasma Project.
# See LICENSE.txt for details.

import unittest


def failUnlessIdentical(self, first, second, msg=None):
    """
    Fail the test if C{first} is not C{second}.  This is an
    obect-identity-equality test, not an object equality (i.e. C{__eq__}) test.

    @param msg: if msg is None, then the failure message will be
        '%r is not %r' % (first, second)
    """
    if first is not second:
        raise AssertionError(msg or '%r is not %r' % (first, second))

    return first

def failIfIdentical(self, first, second, msg=None):
    """
    Fail the test if C{first} is C{second}.  This is an
    object-identity-equality test, not an object equality
    (i.e. C{__eq__}) test.
    
    @param msg: if msg is None, then the failure message will be
        '%r is %r' % (first, second)
    """
    if first is second:
        raise AssertionError(msg or '%r is %r' % (first, second))

    return first


if not hasattr(unittest.TestCase, 'failUnlessIdentical'):
    unittest.TestCase.failUnlessIdentical = failUnlessIdentical

if not hasattr(unittest.TestCase, 'failIfIdentical'):
    unittest.TestCase.failIfIdentical = failIfIdentical

if not hasattr(unittest.TestCase, 'assertIdentical'):
    unittest.TestCase.assertIdentical = unittest.TestCase.failUnlessIdentical

if not hasattr(unittest.TestCase, 'assertNotIdentical'):
    unittest.TestCase.assertNotIdentical = unittest.TestCase.failIfIdentical
