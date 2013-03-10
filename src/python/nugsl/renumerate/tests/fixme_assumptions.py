#-*- encoding: utf8 -*-
'''
    Module
'''

import unittest
import os
import unittest,os,sys
sys.path.append( os.getcwd() )
from renumerate.Assumptions import assumptionsList
from renumerate.PursueTotals import assumptionSpec
from renumerate.Type1Line import type1Line
from renumerate.CategoryHint import categoryHinter

class testGA(assumptionsList):
    def __init__(self, biglist):
        pass

ch = categoryHinter()
ch.read( os.path.join('config', 'test-categories.conf') )

class TestSuite(unittest.TestCase):

    def setUp(self):
        self.bl = [type1Line( '1 2 3', ch )]
        self.ga = testGA( self.bl )
        self.ga.combination_limit = 100

    def testCondense(self):
        bl = [type1Line( '1 blah 2 blah 3 blah 4 blah 5', ch )]
        assumptions = assumptionsList( bl )
        spec = assumptionSpec()
        spec.mark_cruft(1)
        spec.mark_total(2)
        spec.mark_grand_total(3)
        self.assertEqual( assumptions[0].condense( spec ), [1, 3, 4] )
        
    def testAssumptionLength(self):
        bl = [type1Line( '1 blah 2 blah 3', ch )]
        assumptions = assumptionsList( bl )
        spec = assumptionSpec()
        spec.mark_cruft(1)
        self.assertEqual( assumptions[0].length( spec ), 2)
        
    def testGetAllAssumptions(self):
        bl = [type1Line( '1 2 3', ch )]
        ga = testGA( bl )
        ga.combination_limit = 100
        ga.ambig_config_sets = ga.get_ambig_config( bl )
        ga.generate_assumptions( bl )
        self.assertEqual(ga, [[12, 3], [1, 23], [123]] )

    def testSequenceNumber(self):
        bl = [type1Line( '1 2 3', ch )]
        ga = testGA( bl )
        ga.biglist = bl
        ga.combination_limit = 100
        aconf = ga.get_ambig_config( bl )
        assumption = ga.get_assumption( bl, aconf[0] )
        self.assertEqual(assumption[1].sequence(), 1 )

    def testGetAssumption(self):
        bl = [type1Line( '1 2 3', ch )]
        ga = testGA( bl )
        ga.biglist = bl
        ga.combination_limit = 100
        aconf = ga.get_ambig_config( bl )
        assumption = ga.get_assumption( bl, aconf[0] )
        self.assertEqual(assumption, [12, 3] )

    def testComplexAmbigConfig(self):
        bl = [type1Line( '1 2 3 blash 1 2 3', ch )]
        ga = testGA( bl )
        ga.combination_limit = 100
        aconf = ga.get_ambig_config( bl )
        #
        # This is a modest illustration of how the volume of possibilities
        # can quickly explode out of control when commas are dropped from 
        # a document.
        self.assertEqual(aconf, [[1, 1], [2, 1], [3, 1], [3, 2], [2, 2], [1, 2], [1, 3], [2, 3], [3, 3]] )

    def testSimpleAmbigConfig(self):
        self.aconf = self.ga.get_ambig_config( self.bl )
        self.assertEqual(self.aconf, [[1], [2], [3]] )

    def testAmbigInfo(self):
        bl = [type1Line( '1 2 3', ch )]
        ga = testGA( bl )
        ainfo = ga.get_ambig_info( bl )
        self.assertEqual(ainfo, [4] )

    def testInstantiate(self):
        g = testGA( [] )
        g.hello = None
        self.assertEqual( g.hello, None )

if __name__ == "__main__":
    unittest.main()
