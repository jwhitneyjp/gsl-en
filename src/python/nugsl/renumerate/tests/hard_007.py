#-*- encoding: utf8 -*-
'''
    Module
'''

import unittest,os
import unittest,os,sys
sys.path.append( os.getcwd() )
from renumerate.IncomeStatement import incomeStatement
from renumerate.CategoryHint import categoryHinter
from renumerate.PenaltyEngine import penaltyEngine
from StringIO import StringIO

'''

'''

example1 = '''
平成18年度特定非営手1]活動収支業預講
平成19年3月 31 日 預益
特定書構営手】]活動￥ま人 人村開三書7費費1品会
科 目 ・ま商 費 金 額 (単位二円）
（1〉1,   140,000
2, 会費収入 160,000
3, 事業収入 0
4, ン（の地 11
経常収支合計 0 300,011
(2)
1,事業費 12070
2・費支事費 131,710
3,子億費 0
経常支出合計 143,780
経常収支書額 156,231
当 期 収 支 書 額 156,231
百百期ま業講座収支書額 225,954
収年度子業定座収支費額 382,185

平成昭年度寄の地事業会計収支業構家
・ 平成19年3月 31 日事寄支 ・
特定非常和活動手書人 人村開五講費「品会
料 百 ・書商 費 金 額 (単位二円）
(1)
1 ・会費収入 0
2・事業収入 0
3,一での地 0
経常収支合計  
(2)
1,事業費 0
2,費費費 0
3,千億費 0
経常支出合計 0
経常収支書額 0
当 期 収 支 費 額 0
百1]期寄業構収支書額 0
家年度構構収支書額 0
'''  

class TestSuite(unittest.TestCase):
    
    def setUp(self):
        self.ch = categoryHinter( os.path.join('config', 'test-jcategories.conf') )
        self.pe = penaltyEngine
        self.obj = incomeStatement( self.ch, self.pe )

    def testExample1(self):
        self.obj.read( example1 )
        self.obj.analyze()
        self.assertEqual( self.obj, [140000L, 140000L, 160000L, 160000L, 11L, 11L, 300011L] )

if __name__ == "__main__":
    #unittest.main()
    unittest.TextTestRunner().run(TestSuite('testExample1'))

