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
上1支 支 書十 算 書
￥支二て人4書11×11)01五人7レ・<7六平1業地金成7手（1タン3ン昭売商 日 平成 18 年 4 月 1 日
講  19年 3月 31 日機算
科 日 金 額
1 支書 加 億 団 の 部
事 業 収 入
事 業 収 入 43,020,958 43,020,958
会 費 収 入
年 会 賃 会 費 収 入 676,000
費 助 会 費 会 費 収 入 150,000 826,000
寄 付 金 収 入
寄 付 金 収 入 4,563,518 4,563,518
雑 収 入
受 取 利 息 129 129
合 計 48,410,605
11 1>成 座 億 団 の 部
事 業 費
事 業 県 1町
講費府）千売71賃受ン手4 7・書成 526,657
支 億 活 動 2,200,024
万位 書受 三事 営 35,639,638 38,366,319
タ賃 三単 費
人 14二 費
講合 料 手 当 6,597,872
構 定 補 利 費 50,805
千事 利 1事 単 費 55,956 6,714,633
ン（ の 地 0) 経 費
方講 費 支 道 費 2,064,584
構 業賃三 品 費 611,502
受6 書講1 71< 料 費 11,703
賃 借 料 699,328
額2 書 1品 「三業   119,160
  講1 費 1,907,218 5,413,495
合 計 50,494,447
当期1三ら・構助商寄>成度額 △2,083,842
補期ま業道2年四賃助商額 1,831,986
期三1三三1三ら1書助商合計額 △251,856
'''  

class TestSuite(unittest.TestCase):
    
    def setUp(self):
        self.ch = categoryHinter( os.path.join('config', 'test-jcategories.conf') )
        self.pe = penaltyEngine
        self.obj = incomeStatement( self.ch, self.pe )

    def testExample1(self):
        self.obj.read( example1 )
        self.obj.analyze()
        self.assertEqual( self.obj, [43020958L, 43020958L, 676000L, 150000L, 826000L, 4563518L, 4563518L, 129L, 129L, 48410605L] )

if __name__ == "__main__":
    #unittest.main()
    unittest.TextTestRunner().run(TestSuite('testExample1'))

