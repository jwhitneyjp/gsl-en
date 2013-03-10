#-*- encoding: utf8 -*-
'''
    Module
'''

import unittest
import os
import unittest,os,sys
sys.path.append( os.getcwd() )
from renumerate.PenaltyEngine import *
from renumerate.Type1Line import type1Line
from renumerate.CategoryHint import categoryHinter
from renumerate.Assumptions import assumptionsList
from renumerate.PursueTotals import assumptionSpec

class TestEngine(unittest.TestCase):
    def setUp(self):
        ch = categoryHinter( os.path.join('config', 'test-categories.conf') )
        bl = [type1Line( ' x 2007', ch )]
        bl.append( type1Line('', ch) )
        bl.append( type1Line('', ch) )
        bl.append( type1Line('', ch) )
        bl.append( type1Line('x 1. dues 10000', ch) )
        self.assumption = assumptionsList( bl )[0]
        self.assumption_spec = assumptionSpec()
        self.engine = penaltyEngine( self.assumption, self.assumption_spec )

    def testNumberBetterThanYear(self):
        year_p = self.assumption[0].penalty()
        num_p = self.assumption[2].penalty()
        self.assertTrue( sum_p < num_p )
        
    def testExplanatorySumBetterThanBullet(self):
        sum_p = self.assumption[3].penalty()
        bullet_p = self.assumption[1].penalty()
        self.assertTrue( sum_p > bullet_p )
        

if __name__ == "__main__":
    unittest.main()

