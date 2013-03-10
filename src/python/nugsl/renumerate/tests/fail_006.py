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
original 特定非営利活動法人キャリア　パスポート
BAD SCAN
36000 should be 30000
'''

example1 = '''
(￥五賃書 28 業賃百 1 事賃 「百百事業年度の特定書構営手賃]活書1]【二払』益る事業会計収支計算書」)
1 8年度 特定非常利活動に係る事業会計収支計算書
18年 4月 1日から 19年 3月 31日まで
特定非営手1]1書賃】」￥払三人貸5￥ り 7,<二<万受・一 1×
科 日 金 額 (単位 二 円)
1 経常収入の部
1 入会金・会費収入 0
入会金収入 (0 円 ×0 人合） 950 000
会費収入 1 (50, 000 円 ><19 人タ受) 36000 980 000
会費収入2 (10,000 円><3 人会) 】 ￥
2 事業収入
講日市￥)「支道事業収入 3, 020, 000
七 三 十一事業収入 205, 000 3, 225, 000
3 雑 収 入
受取利息 207 207
経常収入合計 4, 205, 207
11 経常支出の部
1 事業費
講構市￥】「賃道事業費 250, 000
12 三 十一事業費 52, 428 302, 428
2 費費費・
  3, 000, 000
一での地費費費 865, 209 3, 865, 209
3 るの地支出
7（の地支出 0 0
経常支出合計 4, 167, 637
経常収支書額 37, 570
111 ・・6の地貸金収入の部
1 7（の地貸金収入
0 0
2 一での地の事業会書十から品業入 107, 609
家七 の地貸金収人合計 107, 609
村 受の地賃金支出の部
1 るの地貸金支出
0 0
)合の地貸金支出合計 0
当期収支書額 37, 570
補期非業構収支書額 107, 609
販期講業構収支書額 1415, 179

(五三ら1賃助商ま書7成の部）
支「 五三助賃助商億二書方1]の部
1 貸商ま費加額
当期収支費額(講借) 37, 570
, ・ ・ ・ 0
2 費億構金額
, ・ ・ ・ 0
出書加額合計 37, 570
町 年開助商補機の部
1 貸商補座額
  (書書』寄) (74 十7・ の品合) 0
2 賃借費出書加額
書成機額合計 37,570
当期五三度億助商出書方日額 （￥成り額) 37, 570
百賃期市業定し書2五5ら1賃助商額 107, 609
当期年家助商合計 145, 179
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

