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
original 特定非営利活動法人グローバル・スポーツ・アライアンス
'''

example1 = '''
2004 年度会計収支計算書
2004年8月 1 日から2005年7月 31 日
特定非・書家・1商動構人村の千機構 5
科 目 金 額 (単位貸円）
〈貸金収支の部)
1 経常収支の部
1 会費 ・ 入会金収入 120000 120000
2 事業収入 0 0
3 寄付金収入 100000 100000
経常収入合計 220000
11 経常支出の部
1 事業費
7×地書・一9￥賃構賃の1】・支道事業 20000
公講販受ン千47の開道事業 0
1「書費支億等開賃の2府書事業 20000
）「百計道業講事業 126597
）2二講活動事業 25000 191597
経常支出合計 0
経常収支書額 191597
町 借の地貸金収入の部
二合の地貸金収入合計 0
村 るの地貸金支出の部
タ（の地貸金支出合計 0
当期収支書額 28403
百賃期構構収支書額 118361
7家期構講収支書額 146764
(五ら寄三助商七書加の部)
支「 11三四支助商道加の部
1 費商七費加額
当期収支書額 (講構） 28403
2 賃億活機額
支費加額合計 13289
町 年府助商成座の部
1 三賃商構座>額 28403
当期収支書額 （書書商）
2 賃億払書加額 12114
1成機額合計 13289
当期五三一助三助商道加額 13289
百万期講賃座年開助商額 106131
当費3五【家助商合計 119420
'''  

class TestSuite(unittest.TestCase):
    
    def setUp(self):
        self.ch = categoryHinter( os.path.join('config', 'test-jcategories.conf') )
        self.pe = penaltyEngine
        self.obj = incomeStatement( self.ch, self.pe )

    def testExample1(self):
        self.obj.read( example1 )
        self.obj.analyze()
        self.assertEqual( self.obj, [120000L, 120000L, 100000L, 100000L, 220000L]  )

if __name__ == "__main__":
    #unittest.main()
    unittest.TextTestRunner().run(TestSuite('testExample1'))

