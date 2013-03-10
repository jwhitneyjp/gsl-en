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
cleared by culling likely explanatory comments in LineList
'''

example1 = '''
書成算12
18年度 特定非常利活動に係る事業会計収支計算書
1額 4月 1日方昭) 四年 3月31日まで
特定非営利活動構人100万人の県る書七団構・億業道動補道・支機七ンタ一
(単位 3 円)
科 日 金 額
1 収入の部
1 会費・入会金収入
入会金収入
受費書 り支)に 4 419 000 4 419 000
2 事業収入
書 書書町支)× 61 763 949 61 763 949
3 補助金等収入
, 地方公共団体補助金収入
民間助成金収入 0
4 事手円1金単座支〉× 21,564,608 21,564,608
5 寄の地収入
業構げ支]× 21,570
利息収入 4, 490
益賃 り4金り支）× 36,747 62,807
6 収益事業会計からの経入
当期収人合計 87 810 364
'''  

class TestSuite(unittest.TestCase):
    
    def setUp(self):
        self.ch = categoryHinter( os.path.join('config', 'test-jcategories.conf') )
        self.pe = penaltyEngine
        self.obj = incomeStatement( self.ch, self.pe )

    def testExample1(self):
        self.obj.read( example1 )
        self.obj.analyze()
        self.assertEqual( self.obj,  [4419000L, 4419000L, 61763949L, 61763949L, 21564608L, 21564608L, 21570L, 4490L, 36747L, 62807L, 87810364L])

if __name__ == "__main__":
    #unittest.main()
    unittest.TextTestRunner().run(TestSuite('testExample1'))

