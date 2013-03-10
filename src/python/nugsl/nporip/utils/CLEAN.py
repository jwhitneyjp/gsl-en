#!/usr/bin/python
#-*- encoding: utf8 -*-

import csv, sys, re, os

FILENAMES = []
FILENAMES.append( ('00-naikakufu.csv','00-内閣府.csv') )
FILENAMES.append( ('01-hokkaido.csv','01-北海道.csv') )
FILENAMES.append( ('02-aomori.csv','02-青森県.csv') )
FILENAMES.append( ('03-iwate.csv','03-岩手県.csv') )
FILENAMES.append( ('04-akita.csv','04-秋田県.csv') )
FILENAMES.append( ('05-miyagi.csv','05-宮城県.csv') )
FILENAMES.append( ('06-yamagata.csv','06-山形県.csv') )
FILENAMES.append( ('07-fukushima.csv','07-福島県.csv') )
FILENAMES.append( ('08-ibaragi.csv','08-茨城県.csv') )
FILENAMES.append( ('09-tochigi.csv','09-栃木県.csv') )
FILENAMES.append( ('10-gunma.csv','10-群馬県.csv') )
FILENAMES.append( ('11-saitama.csv','11-埼玉県.csv') )
FILENAMES.append( ('12-chiba.csv','12-千葉県.csv') )
FILENAMES.append( ('13-tokyo.csv','13-東京都.csv') )
FILENAMES.append( ('14-kanagawa.csv','14-神奈川県.csv') )
FILENAMES.append( ('15-yamanashi.csv','15-山梨県.csv') )
FILENAMES.append( ('16-niigata.csv','16-新潟県.csv') )
FILENAMES.append( ('17-nagano.csv','17-長野県.csv') )
FILENAMES.append( ('18-toyama.csv','18-富山県.csv') )
FILENAMES.append( ('19-ishikawa.csv','19-石川県.csv') )
FILENAMES.append( ('20-fukui.csv','20-福井県.csv') )
FILENAMES.append( ('21-gifu.csv','21-岐阜県.csv') )
FILENAMES.append( ('22-shizuoka.csv','22-静岡県.csv') )
FILENAMES.append( ('23-aichi.csv','23-愛知県.csv') )
FILENAMES.append( ('24-mie.csv','24-三重県.csv') )
FILENAMES.append( ('25-shiga.csv','25-滋賀県.csv') )
FILENAMES.append( ('26-kyoto.csv','26-京都府.csv') )
FILENAMES.append( ('27-osaka.csv','27-大阪府.csv') )
FILENAMES.append( ('28-hyogo.csv','28-兵庫県.csv') )
FILENAMES.append( ('29-nara.csv','29-奈良県.csv') )
FILENAMES.append( ('30-wakayama.csv','30-和歌山県.csv') )
FILENAMES.append( ('31-tottori.csv','31-鳥取県.csv') )
FILENAMES.append( ('32-shimane.csv','32-島根県.csv') )
FILENAMES.append( ('33-okayama.csv','33-岡山県.csv') )
FILENAMES.append( ('34-hiroshima.csv','34-広島県.csv') )
FILENAMES.append( ('35-yamaguchi.csv','35-山口県.csv') )
FILENAMES.append( ('36-tokushima.csv','36-徳島県.csv') )
FILENAMES.append( ('37-kagawa.csv','37-香川県.csv') )
FILENAMES.append( ('38-ehime.csv','38-愛媛県.csv') )
FILENAMES.append( ('39-tokachi.csv','39-高知県.csv') )
FILENAMES.append( ('40-fukuoka.csv','40-福岡県.csv') )
FILENAMES.append( ('41-saga.csv','41-佐賀県.csv') )
FILENAMES.append( ('42-nagasaki.csv','42-長崎県.csv') )
FILENAMES.append( ('43-kumamoto.csv','43-熊本県.csv') )
FILENAMES.append( ('44-oita.csv','44-大分県.csv') )
FILENAMES.append( ('45-miyazaki.csv','45-宮崎県.csv') )
FILENAMES.append( ('46-kagoshima.csv','46-鹿児島県.csv') )
FILENAMES.append( ('47-okinawa.csv','47-沖縄県.csv') )

CITIES = '(市*[^区市]+?(?:市市|市|島|郡|村|町|区))(?:([^区]+)区)*.*'.decode('utf8')

for file in os.listdir('alldata'):
    ifh = open('alldata/' + file)
    csvread = csv.reader(ifh)

    for filename in FILENAMES:
        if filename[1] == file:
            file = filename[0]
    
    ofh = open('cleaned/' + file, 'w+')
    csvwrite = csv.writer(ofh)

    print 'Processing ' + file

    linecount = 1
    
    for line in csvread:
        r = re.match(CITIES,line[4].decode('utf8'))
        if r:
            if r.group(2):
                ku = r.group(2)
            else:
                ku = ''
            
            line.insert(5,ku)
            line.insert(5,r.group(1)[-1])
            line.insert(5,r.group(1)[:-1])
        elif len(line[4]) == 2:
            line.insert(5,"")
            line.insert(5,"")
            line.insert(5,"")
        elif line[4] == 'main_office':
            line.insert(5,'ku')
            line.insert(5,'entity_type')
            line.insert(5,'entity_name')
        else:
            line.insert(5,"")
            line.insert(5,"")
            line.insert(5,"")
            print '  WARNING: Unparsed address at line %d: %s' % (linecount, line[4])
        
        csvwrite.writerow( line )
        
        linecount += 1
        