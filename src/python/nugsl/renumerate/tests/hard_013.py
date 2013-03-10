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
特定非営利活動法人ソウルフル・エクスチェンジ協会.pdf
平成18年度 特定非常利活動に係る事業会計収支計算書
(平成18年9月5日和平成19年8月31助
特定非営利活動構人7市ル7ル・二タ×十手ン9補会
料 日 業 額 億 書
1 41入の書5
1 入会金収入
年会賃
2 会費収入
年会目
賃助会目
3 事業収入
四助書支講事業
4 雑収入
受取和息
5 補助金等収人
補助金収入
6 寄付金等収入
寄付金収入
当期収入合計(助 0
期期雑地収支費額 0
収入合計(町 0
0 支出の部
1 事業費
の助書支機事業 の町町 市一△村一9開体費
2 費講費
貸借料
事講人特費
道借道機費
補講品費
補和億単費
構費支道費
地道売講費
付講億品費
期事会道営費
構会道営費
会講費
事講間道営費
部業費 出町町) 講五費講等付特費開一成
雑費
3 寄の地支出
け講億品講入支出
講講加入構講入支出
当期支出合計(0 座町町
当期収支書額（△レ10 2町四0
家期講業講収支書額 （13)一（6) ・250,000
（単位二円)
'''  

class TestSuite(unittest.TestCase):
    
    def setUp(self):
        self.ch = categoryHinter( os.path.join('config', 'test-jcategories.conf') )
        self.pe = penaltyEngine
        self.obj = incomeStatement( self.ch, self.pe )

    def testCategory(self):
        self.obj.read( example1 )
        self.obj.analyze()
        self.assertEqual( self.obj[0].info['category'], 'Total' )

    def testState(self):
        self.obj.read( example1 )
        self.obj.analyze()
        self.assertEqual( self.obj[0].state(), 2 )

    def testExample1(self):
        self.obj.read( example1 )
        self.obj.analyze()
        self.assertEqual( self.obj, [0])

if __name__ == "__main__":
    unittest.main()
    #unittest.TextTestRunner().run(TestSuite('testCategoryNonTotal'))

