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
2006年度特定非営利活動に係る事業会計収支計算書
2006年4月 1 日から2007年3月 31 日まで
特定非営利活動5ま人 日 事】 《一・）十ル方5一構会
科 目 額 (単位 円）
（> 収 の,)
1経常収入の部
1会費収入
年会賃( 1団人・5ま人） 1,360,000
費助会賃(借人・賃五人) 0
書講定講日市 495,000 1,855,000
2事業収入
講講構定事業収入 11,182,000
補業位活動事業収入 0
講費・町開事業収入 1,185,000
町借・講座・講講事業収入 2,107,468
座講事業収入 288,660
受の地 収入 0 14,763,128
3講ま金道開収入
講取金利息収入 964 964
経常収入合計 16,619,092
0経常支出の部
1事業費
位講構定事業費 6,277,297
補業ま活動事業費 0
  2,727,102
町借・講座・講） 業費 222,910
座事度事業費 1,411,805
での地 費 0 10,639,114
2費費費
人特費 834,500
賃借料 970,000
借品費 0
道1書費 302,243
事講5常事講品費 525,270
販費支道費 184,430
和講公講 0
補会費 11,500
書 商費 40,000
  17,654
講特支構費 25,500
支払手額料 22,120
雑費 , 58,922 2,992,139
経常支出合計 13,631,253
経常収支書額 2,987,839
当期収支費額 2,987,839
補期構講収 額 4,682,882
家期寄業講収 額 7,670,721
（年開助商ま費道の部)
町年構助商借加の部
1貸度構加額
当期収支書額 2,987,839
2賃億5成公額
構加額合計 0 2,987,839 2,987,839
村年町助費道機の部
1賃商補出額
当期収支書額 0
2賃億構加額
5成金額合計 0 0 0
当期年特助 日加額（動公額) 2,987,839
補期経講町ま助構額 4,682,882
当期年特助度合計 7,670,721
'''  

class TestSuite(unittest.TestCase):
    
    def setUp(self):
        self.ch = categoryHinter( os.path.join('config', 'test-jcategories.conf') )
        self.pe = penaltyEngine
        self.obj = incomeStatement( self.ch, self.pe )

    def testExample1(self):
        self.obj.read( example1 )
        self.obj.analyze()
        self.assertEqual( self.obj,  [1360000L, 495000L, 1855000L, 11182000L, 1185000L, 2107468L, 288660L, 14763128L, 964L, 964L, 16619092L] )

if __name__ == "__main__":
    #unittest.main()
    unittest.TextTestRunner().run(TestSuite('testExample1'))

