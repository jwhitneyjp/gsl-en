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
sample negative  一1,260,000
'''

example1 = '''
平成18年度 (業1期) 特定書構営手・1活動1二1県れる事業会賃十収支計算書
(平成18年9月11日方>ら平成19年3月31日まで)
特定非営利計1費入 て) < し < ら×事書 (単位 3 円)
科目 ・, ,,
】》上・出1 2  
1 ・上「単・収入の部
1 会費 ・ 入△金収入
入タ「寄・金 入 180 000
会費収入 114 000 294 000
2 収入
1 講支出二ルし家るり地 ×
2「1）・】二ン子一一レ三1ン・）・【ン】￥・7事『動 0
日・・・県・費三￥ の『・金の六二2支『）の・書構 日1共・て）講>】『・ 0
日2付（ 七の講円 1, 動 224 742 224 742
2 タ , 書五 0
3 ,目12支県業 0
4 △単事民 構 0
5 売・の11』」目町書三・ ・賃・る「二02）の,> 0
3 補   入 0
4 「付金 入
人からの・ 7付 38 000
五賃団 からの「 ・付 201 000 239 000
5 子6）位 入
和書1 1（入 114 114
6 ・て合の ・ からの△『入 0 0
  支入合書 757 856
11 』・七機 出0）計三
1 一 < ,,
1 講）・（ 七二「タレし定る1）り）  
方1）」てン子・一レ三1ン・)《ン1×17手・動 26 450
日『・県座・ の・」7金の7て三62>の】単・ 子日1共』支）講>町￥・ 0
日2に）・< 七の講7二レ11・計 247 707 274 157
2 書事 0 0
3 目取子県業部 0 0
4 ・単 1書 7 0 0
5 ・書の・地』目加73>三>< ・賃・る7・二七（3て）の一・￥費 0 0
6 ￥五人4・ 地等単り 70 000 70 000 344 157
2 費五講5
1 手受 事民動1 0 0
2 1, ・・書手当 0 0
3 活営業 「出費 0 0
4 道1書・ 費 0 0
5   △ 費 0 0
6 月   0 0
7   2 874 2 874
8 講品借 52 000 52 000 54 874
3 子億費
子借 0 0 0
二1・共 支 合書 399 031
111 当,, 収支書・ 358 825
111 収期等・業構収支書額 358,825

平成18年度 (業1期） 寄の地0）事業 会計収支計算書
(平成18年9月11日から平成19年3月31日まで)
特定非営利活動活人・） 〈 し< ら×3書
科目 ×△額 単位二円
八上『地「  
1 収入の書「三
1 ×収入
1 ・』・ 三（れ7・（七事助・千・の 書< 2 0
2 会事1「費八の】五書 ・ ・   0 0
  収入合書 0 0
支入△書 0
11 支 』の位5
  41
1 付三三<れ7て七助・活の 書 二 0
2 会事民（×の】五借 < 0 0
2賃期費 0 0
3 一『定ま 』け千動1二賃・1る三1)る 会書 ××の 』金 0 0
  ・   0 0 0
  収 書・ , 0

'''  

class TestSuite(unittest.TestCase):
    
    def setUp(self):
        self.ch = categoryHinter( os.path.join('config', 'test-jcategories.conf') )
        self.pe = penaltyEngine
        self.obj = incomeStatement( self.ch, self.pe )

    def testExample1(self):
        self.obj.read( example1 )
        self.obj.analyze()
        self.assertEqual( self.obj, [180000L, 114000L, 294000L, 224742L, 224742L, 38000L, 201000L, 239000L, 114L, 114L, 757856L])

if __name__ == "__main__":
    #unittest.main()
    unittest.TextTestRunner().run(TestSuite('testExample1'))

