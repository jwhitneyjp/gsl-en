#-*- encoding: utf8 -*-
'''
    Module
'''

import os,sys
sys.path.append( os.getcwd() )
import unittest
from renumerate.Type1Line import type1Line
from renumerate.CategoryHint import categoryHinter
from renumerate.PursueTotals import pursueTotals, assumptionSpec
from renumerate.Assumptions import assumptionsList
from ConfigParser import ConfigParser

class testPT(pursueTotals):
    def __init__(self, numsets):
        pass

class testCH(categoryHinter):
    def __init__(self, *args):
        ConfigParser.__init__(self)
        self.initialize_vars()

class TestAssumptionSpec(unittest.TestCase):
    
    def setUp(self):
        self.ch = testCH()
        self.ch.read( os.path.join('config', 'test-categories.conf') )
        bl = [type1Line( 'project 100 blah 100 blah 200', self.ch )]
        self.assumptions = assumptionsList( bl, 'type1' )
        self.assumption = self.assumptions[0]

    def testUnwindTotal(self):
        as = assumptionSpec()
        as.mark_total(1)
        as.mark_total(2)
        new_as = as.unwind_total()
        self.assertEqual( new_as[2], as.NON_TOTAL )
        
    def testSpecAsList(self):
        as = assumptionSpec()
        as.mark_total(1)
        as.mark_total(2)
        self.assertEqual( as.spec_as_list(), [(1,1),(2,1)] )
        
    def testUnwindTotalScopeOfUnwind(self):
        as = assumptionSpec()
        as.mark_total(1)
        as.mark_total(2)
        as.unwind_total()
        self.assertEqual( as[1], as.TOTAL )
        
    def testMarkCruftCount(self):
        as = assumptionSpec()
        as.mark_cruft(1)
        self.assertEqual( as.cruft_count(), 1 )
        
    def testMarkCruft(self):
        as = assumptionSpec()
        as.mark_cruft(1)
        self.assertEqual( as[1], as.CRUFT )
        
    def testMarkTotal(self):
        as = assumptionSpec()
        as.mark_total(1)
        self.assertEqual( as[1], as.TOTAL )
        
    def testMarkCruft(self):
        as = assumptionSpec()
        as.mark_grand_total(1)
        self.assertEqual( as[1], as.GRAND_TOTAL )
        
    def testSpecNoKey(self):
        as = assumptionSpec()
        self.assertEqual( as['wowza'], None )

    def testSpecKeyExists(self):
        assumption = self.assumptions[0]
        as = assumptionSpec()
        as['wowza'] = 'whoopie'
        self.assertEqual( as['wowza'], 'whoopie' )

    def testInstantiation(self):
        spec = assumptionSpec()
        self.assertFalse( spec.NON_TOTAL == spec.TOTAL )

class TestSuite(unittest.TestCase):

    def setUp(self):
        self.ch = testCH()
        self.ch.read( os.path.join('config', 'test-categories.conf') )

    def testSimpleSum(self):
        bl = [type1Line( 'project 100 blah 100 blah 200', self.ch )]
        self.pt = testPT( bl )
        self.assertEqual( None, None)

if __name__ == "__main__":
    unittest.main()

