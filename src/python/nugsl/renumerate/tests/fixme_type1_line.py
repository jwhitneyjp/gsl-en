#-*- encoding: utf8 -*-
'''
    Module
'''


import unittest
import unittest,os,sys
sys.path.append( os.getcwd() )
from renumerate.CategoryHint import categoryHinter
from renumerate.Type1Line import type1Line
from renumerate.LineList import lineList

class TestConstructor(unittest.TestCase):

    def setUp(self):
        self.chint = categoryHinter()
        self.chint.addHint('Dues','dues')

    def testMergeFailure(self):
        t = type1Line('111 111 2 222 9 999', self.chint)
        self.assertEqual( t.ints(), [[9999, 222, 2, 111, 111]])

    def testComplexLine(self):
        l = type1Line('Ordinary members 1,000 x 50 members 40,000 50,000 △10,000'.decode('utf8'), self.chint)
        self.assertEqual( l.ints(), [[1000], [50], [-10000, 50000, 40000]])

    def testType(self):
        t = type1Line('911 9 99', self.chint)
        u = t[0:2]
        self.assertTrue( isinstance(u, type1Line) )

    def testUnmergeableBreakPoint(self):
        t = type1Line('666 000 1 999 999 999 999 999', self.chint)
        self.assertEqual( t.ints(), [[1999999999999999, 666000]])

    def testType1ThreeItemsToTwo(self):
        t = type1Line('911 9 999', self.chint)
        self.assertEqual( t.ints(), [[9999, 911]])

    def testType1ThreeItemsBrokenButMergeable(self):
        #
        # Would probably be a bad scan, but no point in aborting
        t = type1Line('999 8 11', self.chint)
        self.assertEqual( t.ints(), [[11, 8, 999]])

    def testType1SimpleOne(self):
        t = type1Line('999', self.chint)
        self.assertEqual( t.ints(), [[999]])
        
    def testEmpty1(self):
        t = type1Line('', self.chint)
        self.assertEqual( t, [])

    def testType1TwoItems(self):
        t = type1Line('999 888', self.chint)
        self.assertEqual( t.ints(), [[999888]])
        
    def testAmbiguityFixWithSimplePair(self):
        t = type1Line('111 88', self.chint)
        self.assertFalse( t[0][1].is_ambiguous)

    def testSimplePair(self):
        t = type1Line('111 88', self.chint)
        self.assertEqual( t.ints(), [[88, 111]])

    def testEmbeddedNegative(self):
        t = type1Line('999△888'.decode('utf8'), self.chint)
        self.assertEqual( t.ints(), [[-888, 999]])

if __name__ == "__main__":
    unittest.main()

