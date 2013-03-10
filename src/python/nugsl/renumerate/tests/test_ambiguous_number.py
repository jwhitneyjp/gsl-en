'''
    Module
'''

import sys
import unittest,os,sys
sys.path.append( os.getcwd() )

import unittest
from renumerate.AmbiguousNumber import ambiguousNumber
from types import ListType

from copy import deepcopy, copy

class TestCopy(unittest.TestCase):

    def setUp(self):
        self.a = ambiguousNumber( '1', {'category':'mycat'})
        #
        # Use copy, not deepcopy, for this class, it's lighter and it works.
        self.b = copy( self.a )

    def testType(self):
        self.assertTrue( isinstance(self.b, ambiguousNumber) )
    
    def testIntValue(self):
        self.assertEqual( int(self.a), int(self.b) )

    def testStringValue(self):
        self.assertEqual( self.a.str, self.b.str )
        
    def testInfoValue(self):
        self.assertEqual( self.a.info['category'], self.b.info['category'] )
        
    def testTrueCopyDiff(self):
        self.a.update( category='yourcat')
        self.assertNotEqual( self.a.info['category'], self.b.info['category'] )

    def testTrueCopyCheckCategory(self):
        self.a.update( category='yourcat')
        self.assertEqual( self.b.info['category'], 'mycat' )

class TestSinglePositiveDigit(unittest.TestCase):

    def setUp(self):
        self.n = ambiguousNumber( '1', {})

    def testInt(self):
        self.assertEqual( self.n, 1 )

    def testStr(self):
        self.assertEqual( self.n.str, '1' )

    def testMergeable(self):
        self.assertEqual( self.n.is_mergeable, False )

class TestNegative(unittest.TestCase):

    def setUp(self):
        self.n = ambiguousNumber( '-1', {})

    def testInt(self):
        self.assertEqual( self.n, -1 )

    def testStr(self):
        self.assertEqual( self.n.str, '-1' )

    def testMergeable(self):
        self.assertEqual( self.n.is_mergeable, False )

class TestZero(unittest.TestCase):

    def setUp(self):
        self.n = ambiguousNumber( '0', {})

    def testInt(self):
        self.assertEqual( self.n, 0 )

    def testStr(self):
        self.assertEqual( self.n.str, '0' )

    def testMergeable(self):
        self.assertEqual( self.n.is_mergeable, False )

class TestThreeDigits(unittest.TestCase):

    def setUp(self):
        self.n = ambiguousNumber( '123', {})

    def testInt(self):
        self.assertEqual( self.n, 123 )

    def testStr(self):
        self.assertEqual( self.n.str, '123' )

    def testMergeable(self):
        self.assertEqual( self.n.is_mergeable, True )

class TestThreeZeros(unittest.TestCase):

    def setUp(self):
        self.n = ambiguousNumber( '000', {})

    def testInt(self):
        self.assertEqual( self.n, 0 )

    def testStr(self):
        self.assertEqual( self.n.str, '000' )

    def testMergeable(self):
        self.assertEqual( self.n.is_mergeable, True )

class TestError(unittest.TestCase):

    def testNoPeriodToComma(self):
        self.assertRaises( ValueError, ambiguousNumber, '0.123', {} )

class TestCategories(unittest.TestCase):

    def setUp(self):
        self.n = ambiguousNumber( '1000', {'category':'Dunno'})

    def testInstantiated(self):
        self.assertEqual( self.n.info['category'], 'Dunno' )
    
    def testUpdateByParam(self):
        self.n.update( category='Gottaclue' )
        self.assertEqual( self.n.info['category'], 'Gottaclue' )

    def testUpdateByMultipleParams(self):
        self.n.update( category='Red', size='Green' )
        self.assertEqual( self.n.info['size'], 'Green' )

if __name__ == "__main__":
    unittest.main()
