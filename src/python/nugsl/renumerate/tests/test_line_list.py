#-*- encoding: utf8 -*-
'''
    Module
'''

import unittest
import unittest,os,sys
sys.path.append( os.getcwd() )
from renumerate.AmbiguousNumber import ambiguousNumber
from renumerate.AmbiguousCluster import ambiguousCluster
from renumerate.LineList import lineList
from renumerate.CategoryHint import categoryHinter
from ConfigParser import ConfigParser

class testLL(lineList):
    def __init__(self, s, category_hinter, line_number=None):
        pass

class testCH(categoryHinter):
    def __init__(self, *args):
        ConfigParser.__init__(self)
        self.initialize_vars()

class TestSplitString(unittest.TestCase):
    
    def setUp(self):
        ch = testCH()
        ch.addHint('Dummy','dummy')
        self.ll = testLL('',ch)
        self.ll.category_hinter = ch
        self.ll.line_number = 1

    def testHandleCommas(self):
        line = self.ll.split_string('1,2')
        self.assertEqual( line[0][0], 12)
        
    def testNumberType(self):
        line = self.ll.split_string('1')
        self.assertTrue( isinstance( line[0][0], ambiguousNumber ) )
        
    def testClusterType(self):
        line = self.ll.split_string('1')
        self.assertTrue( isinstance( line[0], ambiguousCluster ) )
        
    def testLineType(self):
        self.assertTrue( isinstance( self.ll, lineList ) )
        
    def testLineNumbering(self):
        line = self.ll.split_string('100 200 300')
        self.assertEqual( line[-1][-1].info['line'], 1)
        
    def testHintPop(self):
        line = self.ll.split_string('100 dummy 200 smartie 300')
        self.assertEqual( len(line), 3)
        
    def testKnownCategory(self):
        line = self.ll.split_string('100 dummy 200 300')
        self.assertEqual( line[1][0].info['category'], 'Dummy')
        
    def testUnknownCategory(self):
        line = self.ll.split_string('100 dummy 200 300')
        self.assertEqual( line[0][0].info['category'], 'Unknown')
        
    def testNegatives(self):
        self.assertEqual( self.ll.split_string('-100 -200 -300'), [[-300,-200,-100]])
        
    def testOneCluster(self):
        self.assertEqual( self.ll.split_string('100 200 300'), [[300,200,100]])
        


class TestCleanString(unittest.TestCase):

    def setUp(self):
        self.ll = testLL('',None)

    def testRealNumberAtStart(self):
        self.assertEqual(self.ll.clean_string('11, 960, 000'.decode('utf8')), '11,960,000')
        
    def testLessThanThreeAfter2(self):
        self.assertEqual(self.ll.clean_string('m 200,1,2'.decode('utf8')), 'm 200 1 2')

    def testLessThanThreeAfter1(self):
        self.assertEqual(self.ll.clean_string('m 200,1'.decode('utf8')), 'm 200 1')

    def testMoreThanThreeAfter(self):
        self.assertEqual(self.ll.clean_string('m 311,2007'.decode('utf8')), 'm 311 2007')

    def testMoreThanThreeBefore(self):
        self.assertEqual(self.ll.clean_string('m 2007,005'.decode('utf8')), 'm 2007 005')

    def testDoNotCloseLeadingZero2(self):
        self.assertEqual(self.ll.clean_string('m 10 0'.decode('utf8')), 'm 10 0')

    def testCloseLeadingZero2(self):
        self.assertEqual(self.ll.clean_string('m 10 001'.decode('utf8')), 'm 10001')

    def testDoNotCloseLeadingZero1(self):
        self.assertEqual(self.ll.clean_string('m 1 0'.decode('utf8')), 'm 1 0')

    def testCloseLeadingZero1(self):
        self.assertEqual(self.ll.clean_string('m 1 001'.decode('utf8')), 'm 1001')

    def testNormalizeNegative(self):
        self.assertEqual(self.ll.clean_string('m △1000 ー 2000 -3000'.decode('utf8')), 'm -1000 -2000 -3000')

    def testCloseTrailingSpaceOnMinus(self):
        self.assertEqual(self.ll.clean_string('m 1000 △ 2000'.decode('utf8')), 'm 1000 -2000')

    def testLeadingSpaceOnMinus(self):
        self.assertEqual(self.ll.clean_string('m 1000△2000'.decode('utf8')), 'm 1000 -2000')

    def testLeadingNumber(self):
        self.assertEqual(self.ll.clean_string('1   first 1000'.decode('utf8')), 'first 1000')
        
    def testNamedNumber(self):
        self.assertEqual(self.ll.clean_string('m 100円 1000'.decode('utf8')), 'm [NAMED] 1000')
        
    def testComma4(self):
        self.assertEqual(self.ll.clean_string('m 1, , ,200'), 'm 1,200')
        
    def testComma3(self):
        self.assertEqual(self.ll.clean_string('m 1,,200'), 'm 1,200')
        
    def testComma2(self):
        self.assertEqual(self.ll.clean_string('m 1 , 200'), 'm 1,200')
        
    def testComma1(self):
        self.assertEqual(self.ll.clean_string('m 1.200'), 'm 1,200')
        
    def testNakaguro(self):
        self.assertEqual(self.ll.clean_string('m 1・2'.decode('utf8')), 'm 1 2')
        
    def testBadNegative3(self):
        self.assertEqual(self.ll.clean_string('m 100 △'.decode('utf8')), 'm 100 [MINUS]')
        
    def testBadNegative1(self):
        self.assertEqual(self.ll.clean_string('m 100 △m'.decode('utf8')), 'm 100 [MINUS]m')
        
    def testBadNegative2(self):
        self.assertEqual(self.ll.clean_string('m 100 ーm'.decode('utf8')), 'm 100 [MINUS]m')
        
    def testExplanatoryNotes1(self):
        self.assertEqual(self.ll.clean_string('m 1000 (10 members x 100 yen)'), 'm 1000 [NUMxNUM]')
        
    def testExplanatoryNotes2(self):
        self.assertEqual(self.ll.clean_string('m 1000 (each member 10 yen x 100)'), 'm 1000 [NUMxNUM]')
        
    def testExplanatoryNotes3(self):
        self.assertEqual(self.ll.clean_string('m 1000 10 × 100'.decode('utf8')), 'm 1000 [NUMxNUM]')
        
    def testLoneNumbers(self):
        self.assertEqual(self.ll.clean_string('m1m 2 3'), 'm[NUM]m 2 3')
        
    def testBigWhiteSpace2(self):
        self.assertEqual(self.ll.clean_string('mmm1,   140,000'), 'mmm1,[SPACE] 140,000')

    def testBigWhiteSpace(self):
        self.assertEqual(self.ll.clean_string('m 1   3'), 'm 1 [SPACE] 3')

class TestInitMethods(unittest.TestCase):

    def setUp(self):
        ch = testCH()
        ch.addHint('Dummy','dummy')
        self.ll = testLL('',ch)
        
    # XXX
    
    def testInitLineFromList(self):
        self.ll.init_line( ['one'] )
        self.assertEqual(self.ll, ['one'] )

class TestBareConstructor(unittest.TestCase):

    def setUp(self):
        self.ll = testLL('',None)

    def testAppend(self):
        self.ll.append('wow')
        self.assertEqual(self.ll, ['wow'])
        
    def testExtend(self):
        self.ll.extend(['wow'])
        self.assertEqual(self.ll, ['wow'])

    def testBareInit(self):
        self.assertEqual(self.ll, [])

if __name__ == "__main__":
    unittest.main()


