# Copyright (c) 2007-2009 The Plasma Project.
# See LICENSE.txt for details.


import unittest


# some Python 2.3 unittest compatibility fixes
if not hasattr(unittest.TestCase, 'assertTrue'):
    unittest.TestCase.assertTrue = unittest.TestCase.failUnless
if not hasattr(unittest.TestCase, 'assertFalse'):
    unittest.TestCase.assertFalse = unittest.TestCase.failIf
