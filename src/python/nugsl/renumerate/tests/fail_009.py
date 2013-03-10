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
Type2 sheet with reverse ordering of totals and elements, and two-column entries
Fun!
'''

example1 = '''
平成18年度特定非営利活動講入[二係る事業会計収支計算書
平成1 8年4月 1 日から平成1 9年3月 31 日まで
（特定非常利活動5ま人 開商三業書売上4ン75費寄家る会)
(単位 , 円)
科 目 子算額 5業算額 書事 億等
事業活動収支の部
1, 事業活動収入
1)会費収入 102,000 111,000 △9, 000
入会金収入 0 1,000 △1 , 000 四村 雑
会費収入 102,000 110,000 △8, 000
2) 事業収入 100,000 0 100,000
【二1一村・」1書・一タ一事業 100,000 0 100,000
3)補助金収入 0 0 0
補助金収入 0 0 0
4) 寄付金収入 270,000 0 270,000
寄付金収入 270,000 0 270,000
5)雑収入 0 338 △338
受取利息 0 338 △338
雑収入 0 0 0
事業活動収入合計 472,000 111,338 360,662
1, 事業活動支出
'''  

class TestSuite(unittest.TestCase):
    
    def setUp(self):
        self.ch = categoryHinter( os.path.join('config', 'test-jcategories.conf') )
        self.pe = penaltyEngine
        self.obj = incomeStatement( self.ch, self.pe )

    def testExample1(self):
        self.obj.read( example1 )
        self.obj.analyze()
        self.assertEqual( self.obj, [534000L, 840000L, 1374000L, 103000L, 181000L, 25000L, 309000L, 723L, 723L, 1683723L] )

if __name__ == "__main__":
    #unittest.main()
    unittest.TextTestRunner().run(TestSuite('testExample1'))

