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
original 特定非営利活動法人ホー ルアース研究所
Very small print, rescanned with pdftoppm -r 320
'''

example1 = '''
特定非営利活動1（係る事業収支書十算書
特定非営利活動5ま』に
市一ル7一2町講販
目2006年4月 1日
講2007年3月31日
（単 1 二円)
科 目 金 額
[費金収支の部 ]
1 講常収入の部
1 会・費・入会金収入
（1）入会金 0
(2) 金費 200,000 200,000
2事業収入
(11 百 都講体講活動・講1書￥共・賃等1二開一まる金・1町2て」て7・09・5△書書6五事業収入 22,020,025
(2) 書品体事戻活動1等1二開て算・る「書公げ等方和らの受書五事業収入 44,035,377 66,963,402
3寄付金収入
(1) 事県構三算構等5【費事業1二村まる寄1講金収入 26,522,344 26,522,344
4雑収入
（1】受 取 手11 息 3,628
(21 雑 1111 入 840,091 843,719
経常収入合計 04,529,465
11 講費常支出の部
1 事業費
(11 日タ1・1費体書算活書11・講講都1百講1二開・まる道町五2げ7・0タ・5△事地事業費 24,702,815
(2] 日構費体講活助等1二開まる書・公1千等01らの受書五事業費 50,391,732
(31 講構1講1書事5て書事業費 37,066,990 112,161,537
2費 1事 費
賃 賃 料 72,450
71( 道 5・6   費 23,080
道 1書 費 951,616
55 開 費 99,552
手日 講31 公 講 1,215,598
事 手算 1手1 品 費 250,355
座 借 費 1・三 費 1,007,621
支 11, 手 動 料 671,970
講 会 費 155,924
講 118 団 1 費 129,505
会 講 費 27,030
雑 , 費 50,128
講常支出合賃十 116,911,366
講常収支書額 ・22,331,901
111 道・の地費金収入（1)部
億 受 金 1111 入 10,817,601
借 入 金 収 入 8,173,704
るの地費金収入合計 18,991,305
111 ・五・の地費金支出の部
11支 受 金 支 出 0,775,140
借入金返講支出 2,280,791
・活の地費金支出合計 12,055,940
当 期 1111 支 書 額 ・15,446,536
町 期 寄書 構 収 支 書 講賃 14,494,456
家 期 構 構 収 支 書 額 ・1,048,086
[三1三日ま助費ま費三成の部]
11 1三【1ま助度ま書11[】の部
1費 度 ま貸 1111 額
当 191 収 支 書 額 (計品) 45,446,536
2 賃 11 21成 出 額
1172 受 金 9,775,149
品 期 借 入 金 2,200,791
1書 1111 額 合 計・ 一3,300,596
171 年四ま助商ま,成9>の部
1費 費 5成 出 額
2 賃 構 1費 1111 額
[度 受 金 10,817,601
賃 期 借 入 金 8,173,704
2成 出 額 合 計 10,001,305
当期三五11ま助度ま費加額 一22,381,901
補期寄事講座二1]三「】ま期・費額 0,330,187
当期三1三昭三助商合書・書・額 一13,05￥,714
'''  

class TestSuite(unittest.TestCase):
    
    def setUp(self):
        self.ch = categoryHinter( os.path.join('config', 'test-jcategories.conf') )
        self.pe = penaltyEngine
        self.obj = incomeStatement( self.ch, self.pe )

    def testExample1(self):
        self.obj.read( example1 )
        self.obj.analyze()
        self.assertEqual( self.obj,  None )

if __name__ == "__main__":
    #unittest.main()
    unittest.TextTestRunner().run(TestSuite('testExample1'))

