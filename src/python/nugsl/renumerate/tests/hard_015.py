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

example1 = '''
平成18年度「特定書構営手【]活動1二係る事業会書一十」収支計算書
平成17年9月 1 日 から平成18年8月 31 日 まで
特定非営利活動￥支三人 7二1てタルの会・21
単位二 円
（ , の,,
, 1経常収入の部
1会費・入会金収入 0 0
1）入会金収入 0 0
一 2)「二会賃会費収入 0 0
0 0
3〉賃助会賃会費収入 0 0
2事業収入 0 0
]算1賃間商に開講る億講書講事 ・ 30,000 30,000 0 事業手1受書書参昭
3補助金等収入 0 0
5雑収入 0 0
経常収入合計 30,000 30,000
五経常支出の部
, 1事業費 0 0
]県1算『品講1二開参る億書機商業事・ 30,000 30,000 0 事業事1受書書参開
2タ賃書費 0 0
3子億費 0 0
1）子億費 0 0
経常支出合計 30,000 30,000
  経常収支書額 0 0
1]1るの地貸金収入の部
11三て1定貸商売却収入 0 0
2寄業入金収入 0 0
  3借入金収入 0 0
タ（の地賃金収入合計 0 0
1支「一ての地賃金支出の部
1 商 定貸商取構支出
2借入金返手費支出
タ（の地貸金支出合計 0 0
当期収支書額 0 0 ,
百賃期寄業道収支書額 25,000 25,000
販期寄業返収支書額 25,000 25,000 0
（五度構助商ま費成の部)
げ年家助商道加の部
1費商上書加額 0 0 0
2賃借家成機額 0 0 0
町年家助商成のの部
1貸度成機額 0
2賃億五書加額 0 0 0
1)費期借入金講書加額 ・ 0 0
当期五三座構助商支書加額 0 0
助期家業道年・家助商額 25,000 25,000
'''  

class TestSuite(unittest.TestCase):
    
    def setUp(self):
        self.ch = categoryHinter( os.path.join('config', 'test-jcategories.conf') )
        self.pe = penaltyEngine
        self.obj = incomeStatement( self.ch, self.pe )

    def testExample1(self):
        self.obj.read( example1 )
        self.obj.analyze()
        self.assertEqual( self.obj, [30000L, 30000L, 30000L])

if __name__ == "__main__":
    #unittest.main()
    unittest.TextTestRunner().run(TestSuite('testExample1'))

