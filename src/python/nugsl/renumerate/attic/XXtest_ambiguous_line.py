#-*- encoding: utf8 -*-
'''
    Module
'''

import unittest
from renumerate.CategoryHint import categoryHinter
from renumerate.AmbiguousLine import ambiguousLine

class TestConstructor(unittest.TestCase):

    def setUp(self):
        self.chint = categoryHinter()
        self.chint.addHint('Dues','dues')
        self.chint.addHint('Dues','Membership Fee')
        self.chint.addHint('Projects','project')

    def testType1ThreeItemsToTwo(self):
        l = ambiguousLine('911 9 999', self.chint)
        self.assertEqual( l.type1.ints(), [[9999, 911]])
        
    def testType1TwoItemsUnmergeable(self):
        l = ambiguousLine('888 999', self.chint)
        self.assertEqual( l.type1.ints(), [[999, 888]])
        
    def testType1TwoItems(self):
        l = ambiguousLine('999 888', self.chint)
        self.assertEqual( l.type1.ints(), [[999888]])
        
    def testType1SimpleOne(self):
        l = ambiguousLine('999', self.chint)
        self.assertEqual( l.type1.ints(), [[999]])
        
    def testNonTotal(self):
        l = ambiguousLine('333 111 222 222 333', self.chint)
        self.assertEqual( l.type2.ints(), [])
    
    def testMultipleValidSums(self):
        l = ambiguousLine('333 111 222 blah 555 222 333', self.chint)
        self.assertEqual( l.type2.ints(), [[222]])
    
    def testThreeOk2(self):
        l = ambiguousLine('333 111 222', self.chint)
        self.assertEqual( l.type2.ints(), [[111]] )

    def testBrokenCruftOk2(self):
        l = ambiguousLine('This is a pen 3 33 11 1 2 22 garble', self.chint)
        self.assertEqual( l.type2.ints(), [[111]] )

    def testMoreBrokenCruftOk2(self):
        l = ambiguousLine(',3 , 33 1 1 1 2 22', self.chint)
        self.assertEqual( l.type2.ints(), [[111]] )

    def testFourOk2(self):
        l = ambiguousLine('3 33 111 222', self.chint)
        self.assertEqual( l.type2.ints(), [[111]] )

    def testThreeNg2(self):
        l = ambiguousLine('123 456 789', self.chint)
        self.assertEqual( l.type2, [] )

    def testTwo2(self):
        l = ambiguousLine('123 456', self.chint)
        self.assertEqual( l.type1, [[456, 123]] )

    def testEmpty2(self):
        l = ambiguousLine('', self.chint)
        self.assertEqual( l.type2, [])

    def testEmpty1(self):
        l = ambiguousLine('', self.chint)
        self.assertEqual( l.type1, [])

if __name__ == "__main__":
    unittest.main()
