#-*- encoding: utf8 -*-
'''
    Module
'''

import unittest
import unittest,os,sys
sys.path.append( os.getcwd() )
from renumerate.CategoryHint import categoryHinter
from renumerate.LineList import lineList
from renumerate.Type2Line import type2Line
from renumerate.AmbiguousNumber import ambiguousNumber
from renumerate.AmbiguousCluster import ambiguousCluster

from types import LongType

class TestConstructor(unittest.TestCase):

    def setUp(self):
        self.chint = categoryHinter()
        self.chint.addHint('Dues','dues')
        self.ac111 = ambiguousCluster( ambiguousNumber('111', {} ), None)
        self.ac222 = ambiguousCluster( ambiguousNumber('222', {} ), None)
        self.ac333 = ambiguousCluster( ambiguousNumber('333', {} ), None)
        self.ac444 = ambiguousCluster( ambiguousNumber('444', {} ), None)

    def testComplexLine(self):
        l = type2Line('Ordinary members 1,000 x 50 members 40,000 50,000 △10,000'.decode('utf8'), self.chint)
        self.assertEqual( l.ints(), [[50000]])

    def testMaxOnlyWithTwoMaxVals(self):
        t = type2Line( '', self.chint )
        t.extend( [self.ac444, self.ac222, self.ac444, self.ac111] )
        t.max_only()
        self.assertEqual( t.ints(), [[444]])
        
    def testMaxOnly(self):
        t = type2Line( '', self.chint )
        t.extend( [self.ac333, self.ac222, self.ac111] )
        t.max_only()
        self.assertEqual( t.ints(), [[333]])
        
    def testComplexLine(self):
        t = type2Line( 'Ordinary members 1,000 x 50 members 40,000 50,000 △10,000'.decode('utf8'), self.chint )
        self.assertEqual( t.ints(), [[50000]])

    def testNonTotal(self):
        t = type2Line( '333 111 222 222 333', self.chint )
        self.assertEqual( t.ints(), [])
    
    def testMultipleValidSums(self):
        t = type2Line( '333 111 222 blah 555 222 333', self.chint )
        self.assertEqual( t.ints(), [[222]])
    
    def testThreeOk2(self):
        t = type2Line( '333 111 222', self.chint )
        self.assertEqual( t.ints(), [[111]] )

    def testBrokenCruftOk2(self):
        t = type2Line( 'This is a pen 3 33 11 1 2 22 garble', self.chint )
        self.assertEqual( t.ints(), [[111]] )

    def testMoreBrokenCruftOk2(self):
        t = type2Line( ',3 , 33 1 1 1 2 22', self.chint )
        self.assertEqual( t.ints(), [[111]] )

    def testFourOk2(self):
        t = type2Line( '3 33 111 222', self.chint )
        self.assertEqual( t.ints(), [[111]] )

    def testThreeNg2(self):
        t = type2Line( '123 456 789', self.chint )
        self.assertEqual( t, [] )
        
    def testEmpty2(self):
        t = type2Line( '', self.chint )
        self.assertEqual( t, [])

if __name__ == "__main__":
    unittest.main()
