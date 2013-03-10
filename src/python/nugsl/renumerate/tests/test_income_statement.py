#-*- encoding: utf8 -*-
'''
    Module
'''

import unittest,os,sys
sys.path.append( os.getcwd() )
from renumerate.IncomeStatement import incomeStatement
from renumerate.CategoryHint import categoryHinter
from renumerate.PenaltyEngine import penaltyEngine
from StringIO import StringIO

'''
sample negative  一1,260,000
'''

type2string = '''Income statement for 2007
Super duper do-everything organization

Budget Actual Accounting
Income
Category 1: Dues
Ordinary members 30 000 50 000 △20,000
Corporate members 20,000 20,000 0
Total dues 50,000 70,000 △ 20,000
Category 2: Projects
Project A 100,000 88,000 12,000
Project B 100,000 102,000 △ 2,000
Total projects 200,000 190,000 10,000
Grand total 250,000 260,000 △10,000
Other stuff 2345
'''

type1string = '''Income statement for Heisei 19
Central Therapeutic Hurdy-Gurdy Admiration Society
Income
Membership dues
Individual contributions 30000
Corporate contributions 0
Total dues 30000
Projects and activities
Hurdy-Gurdy renovation 15000
Performance (quartet) 25000
Performance (solo)   5000   45 000
Interest income 100 100
Total income 75,100

expenditures
'''

class TestSuite(unittest.TestCase):

    def setUp(self):
        self.ch = categoryHinter( os.path.join('config', 'test-categories.conf') )
        self.pe = penaltyEngine
        self.obj = incomeStatement( self.ch, self.pe )
        self.io = StringIO()
        self.io.write(type2string)
        self.io.seek(0)

    def testAnalyzeType1Example(self):
        self.obj.read( type1string )
        self.obj.analyze()
        self.assertEqual( self.obj,  [30000L, 30000L, 15000L, 25000L, 5000L, 45000L, 100L, 100L, 75100L] )

    def testAnalyzeType2Example(self):
        self.obj.read( type2string )
        self.obj.analyze()
        self.assertEqual( self.obj, [50000L, 20000L, 70000L, 88000L, 102000L, 190000L, 260000L] )

    def testLinePreParseEmptyLine(self):
        self.obj.read( '' )
        self.obj.analyze()
        self.assertEqual( self.obj, [] )

    def testLinesRead(self):
        self.obj.read( type2string )
        self.assertEqual( self.obj.raw[6], 'Ordinary members 30 000 50 000 △20,000'.decode('utf8') )

    def testConstructor(self):
        self.assertEqual( self.obj, [] )

if __name__ == "__main__":
    #unittest.main()
    unittest.TextTestRunner().run(TestSuite('testAnalyzeType2Example'))

