#!/usr/bin/python

import os,sys,re,csv
sys.path.append( os.getcwd() )
from renumerate.CategoryHint import categoryHinter
from renumerate.PenaltyEngine import penaltyEngine
from renumerate.IncomeStatement import incomeStatement
from renumerate.PursueTotals import assumptionSpec

spec = assumptionSpec()
ch = categoryHinter( 'config/test-jcategories.conf' )
pe = penaltyEngine

path='/home/bennett//Desktop/Work/Research/NPO-financials/financials/pdf/naikakufu/'

unpaper='unpaper -bn v,h -bs 3 -bd 100 -bp 2 -bt 0.9 -bi 0.95 -li 0.01 --overwrite --deskew-scan-step 0.05 --no-noisefilter --grayfilter-size 5 --grayfilter-step 1 --grayfilter-threshold 0.1'

filename = os.path.split( sys.argv[1] )[-1]
filename = os.path.splitext( filename )[0]
filename = filename.decode('utf8')
filename = filename.encode('utf8')

def analyze( text=None):
    if not text:
        text = open('RDATA.txt').read().decode('utf8')
    incomer = incomeStatement( ch, pe )
    incomer.read( text )
    incomer.analyze()
    data = []
    for section in ch.ordered_sections():
        data.append( [] )
        for number in incomer:
            #print number.info['nontotal']
            #print 'TOTAL: %s, state: %s' % (spec.TOTAL, number.state())
            if number.info['nontotal'] == section and not number.state():
                data[-1].append(number)
    line = [','.join( [y.str for y in  x] ) for x in data]
    print line
    #ofh = open( 'raw/%s/data.csv' % filename, 'w+')
    #c = csv.writer( ofh )
    #c.writerow( line )
    #ofh.close()

if os.path.exists('RDATA.txt'):
    analyze()
    sys.exit()
    
if len(sys.argv) > 1 and sys.argv[1].endswith('.txt'):
    text = open( sys.argv[1] ).read()
    analyze( text=text )
    sys.exit()
    
info = os.popen('pdfinfo %s' % sys.argv[1])
r = re.match('(?i)(?m)(?s).*pages: *([0-9])+.*',info.read())
pages = int(r.group(1))

for file in os.listdir('rtmp'):
    os.unlink('rtmp/' + file)

found_page = False
text = ''

for page in range(pages,0,-1):
    print 'Page %d' % page
    for file in os.listdir('rtmp'):
        os.unlink('rtmp/'+file)
    os.system('pdfimages -f %d -l %d %s rtmp/RDATA' % (page,page,sys.argv[1]))
    os.system('pnmcat -tb rtmp/RDATA-* | pnminvert | pgmtopbm > rtmp/RDATA.pbm')
    os.system('%s rtmp/RDATA.pbm rtmp/RDATA-CLEAN.pbm' % unpaper)
    os.system('pnmtotiff rtmp/RDATA-CLEAN.pbm > rtmp/RDATA.tif')
    os.system('tesseract rtmp/RDATA.tif rtmp/RDATA -l npx config/tess.conf')
    newtext = open('rtmp/RDATA.txt').read().decode('utf8')
    r = re.match('(?s)(?m).*%s.*' % ch.re_start,newtext)
    if r:
        found_page = True
    if found_page and not r:
        break
    text = newtext + text
    if not os.path.exists('raw/%s' % filename ):
        os.makedirs('raw/%s' % filename )
    os.system('cat rtmp/RDATA.pbm | pnmtopng > TEMP.png')
    os.system('mv TEMP.png raw/%s/page%0.5d.png' % (filename,page))

open('RDATA.txt','w+').write(text)

analyze()
