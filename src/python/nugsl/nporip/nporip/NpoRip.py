#!/usr/bin/python
#-*- encoding: utf-8 -*-


'''
    This module is used to rip the Japanese national
    NPO registry to CSV.
'''
import re,sys
from exceptions import Exception
import urllib2
import urllib
import libxml2
import cookielib
import tidy
from cStringIO import StringIO
import os

class LevelError(Exception):
    pass

DATE_RX = '(.*)年(.*)月(.*)日.*'

FIELDS = []
FIELDS.append( ('name','団体名称') )
FIELDS.append( ('authority','所轄庁') )
FIELDS.append( ('founding','法人認証年月日') )
FIELDS.append( ('prefecture','都道府県') )
FIELDS.append( ('main_office','主たる事務所') )
FIELDS.append( ('other_offices','従たる事務所') )
FIELDS.append( ('representative','代表者名') )
FIELDS.append( ('purpose','目的') )

AREAS = []
AREAS.append(('1','医療又は福祉の増進を図る活動'))
AREAS.append(('2','社会教育の推進を図る活動'))
AREAS.append(('3','まちづくりの推進を図る活動'))
AREAS.append(('4','学術、文化、芸術又はスポーツの振興を図る活動'))
AREAS.append(('5','環境の保全を図る活動'))
AREAS.append(('6','災害救助活動'))
AREAS.append(('7','地域安全活動'))
AREAS.append(('8','人権の擁護又は平和の推進を図る活動'))
AREAS.append(('9','国際協力の活動'))
AREAS.append(('10','男女共同参画社会の形成の促進を図る活動'))
AREAS.append(('11','子どもの健全育成を図る活動'))
AREAS.append(('12','情報化社会の発展を図る活動'))
AREAS.append(('13','科学技術の振興を図る活動'))
AREAS.append(('14','経済活動の活性化を図る活動'))
AREAS.append(('15','職業能力の開発又は雇用機会の拡充を支援する活動'))
AREAS.append(('16','消費者の保護を図る活動'))
AREAS.append(('17','前各号の掲げる活動を行う団体の運営又は活動に関する連絡、助言又は援助の活動'))

class npoRip:
    def __init__(self, debug=False):
        self.debug = debug
        self.cj = cookielib.LWPCookieJar()

    def sanitize(self, orgname ):
        orgname = orgname.decode('utf8')
        orgname = orgname.strip().replace(' ','')
        orgname = orgname.replace('(','')
        orgname = orgname.replace(')','')
        orgname = orgname.replace('/','')
        orgname = orgname.replace( unichr(12288), '' )
        orgname = orgname.replace( unichr(65293), unichr(12540) )
        orgname = orgname.replace( unichr(8722), unichr(12540) )
        orgname = orgname.replace( unichr(65374), unichr(12316) )
        orgname = orgname.encode('utf8')
        return orgname

    def fetch(self,stub='/npoportal/Portal_search',
                   urlbase='http://www.npo-homepage.go.jp',
                   params=[],
                   makedoc=True,
                   usetidy=True,
                   encoding='Shift-JIS',
                   raw=False,
                   useget=False,
                   dump=False,
                   headers={}):
        uopen = urllib2.urlopen
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
        urllib2.install_opener(opener)

        txheaders =  {}
        txheaders['User-agent'] = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        txheaders['Content-Type'] = 'application/x-www-form-urlencoded'

        txheaders.update( headers )
        
        request = urllib2.Request
        
        if useget:
            req = request(urlbase + stub, headers=txheaders)
        else:
            #urlparams = urllib.urlencode(params)
            req = request(urlbase + stub, data=params, headers=txheaders)
            
        ifh = uopen(req)
        txt = ifh.read()
        
        if dump:
            open('dump_before_tidy.html','w+').write( txt )
            
        if not raw:
            if not 'charset=' in txt:
                charset = '<META content=text/html;charset=%s http-equiv=Content-Type>'
                charset = charset % encoding
                r = re.match('(?ms)^(.*<head[^>]*>)(.*)',txt)
                txt = r.group(1) + charset + r.group(2)
            else:
                txt = re.sub('charset="[^ "]*"+','charset=UTF8',txt)
                txt = re.sub('charset=\'[^ \']*\'+','charset=UTF8',txt)
                txt = re.sub('charset=[^ \'"]+','charset=UTF8',txt)
            txt = txt.decode(encoding, 'replace').encode('UTF8')
            txt = txt.replace(' id=',' idX=')
            txt = txt.replace(' name=',' nameX=')

            if usetidy:
                txt = re.sub('(?i)<form [^>]*>','',txt)
                txt = re.sub('(?i)</form>','',txt)
                io = StringIO()
                options = dict(char_encoding='utf8')
                tdoc = tidy.parseString( txt, **options)
                tdoc.write( io )
                io.seek(0)
                txt = io.read()
            
            if dump:
                open('dump_after_tidy.html','w+').write( txt )
            
            if makedoc:
                html = txt.decode('UTF8','replace')
                #html = html.replace(unichr(12), u'')
                html = html.encode('UTF8','replace')
                txt = libxml2.htmlParseDoc(html,'UTF8')
        return txt

    def pdf2gocr(self,file):
        path,filename = os.path.split( file )
        basename = os.path.splitext( filename )[0]
        
        sys.stdout.write(':')
        sys.stdout.flush()
        os.popen('pdftoppm %s/%s %s/%s' % (path,filename,path,basename))
        # Scan files in reverse order, because the income statement
        # is generally on one of the last pages
        files = os.listdir( path )
        files.remove( filename )
        files.sort()
        files.reverse()
        sys.stdout.write('(%d)' % len(files) )
        sys.stdout.flush()
        numbers = []
        ppms = []
        shuu_files = []
        for f in files:
            if not f.endswith('.ppm'):
                continue
            sys.stdout.write('u')
            sys.stdout.flush()
            os.popen('unpaper -bn v -bs 1 -bd 70 -bp 1 -bt 0.9 -bi 1 -li 0.01 --overwrite --grayfilter-size 5 --grayfilter-step 1 --grayfilter-threshold 0.1 %s/%s %s/%s-unpaper 2>/dev/null' % (path,f,path,f))
            sys.stdout.write('g')
            sys.stdout.flush()
            txt = os.popen('gocr -s 15 -a 85 -l 200 -m 2 -C []0123456789,収l %s/%s-unpaper 2>/dev/null' % (path,f)).read()
            # Need to train Tesseract to recognize 収, then we'll move in this direction
            # As a hacked alternative, we could use gocr to identify pages, but this would be slooooow
            #os.popen('tesseract %s/%s TXT 2>/dev/null' % (path,f))
            #txt = popen('cat TXT.txt').read()
            if '収' in txt:
                shuu_files.append( f )
                txt = '\n'.join( txt.split( '\n' )[1:] )
                ppms.append(f)
                # If a comma is identified, it can only be preceded by
                # three numerals max.  Anything more is a lost
                # column break
                txt = re.sub('l','1',txt)
                txt = re.sub('([0-9]), ([0-9])','\\1,\\2',txt)
                txt = re.sub('(7)([0-9]{3}[^0-9])',',\\1\\2',txt)
                txt = re.sub(',([0-9]{3})([0-9])','\\1 \\2',txt)
                txt = re.sub(',','',txt)
                #open('%s/%s-text' % (path,f),'w+').write(txt)
                numbers.extend( re.findall('[0-9]+', txt) )
                sys.stdout.write('!')
                sys.stdout.flush()
            else:
                sys.stdout.write('.')
                sys.stdout.flush()
                if shuu_files:
                    break
        

        if numbers:
            mymax = max( [int(x) for x in numbers] )
            # This is getting nuts
            if mymax < 100:
                numbers = []
                for f in shuu_files:
                    txt = os.popen('gocr -s 20 -a 85 -l 200 -m 2 -C []0123456789,収l %s/%s-unpaper 2>/dev/null' % (path,f)).read()
                    txt = '\n'.join( txt.split( '\n' )[1:] )
                    txt = re.sub('l','1',txt)
                    txt = re.sub('([0-9]), ([0-9])','\\1,\\2',txt)
                    txt = re.sub('(7)([0-9]{3}[^0-9])',',\\1\\2',txt)
                    txt = re.sub(',([0-9]{3})([0-9])','\\1 \\2',txt)
                    txt = re.sub(',','',txt)
                    numbers.extend( re.findall('[0-9]+', txt) )
                    mymax = max( [int(x) for x in numbers] )
                    sys.stdout.write('?')
                    sys.stdout.flush()
        else:
            mymax = -1

        sys.stdout.write('[%s]' % mymax)
        sys.stdout.write('\n')
        sys.stdout.flush()
        return (mymax, ppms)

    
    def get_toplist(self):
        webdoc = self.fetch(stub='/npoportal/Portal_search',
                            encoding='Shift-JIS')
        options = webdoc.xpathEval('//select[@namex="S_Syokatu"]/option')
        toplist = [ ( x.prop('value'), x.content.strip() ) for x in options]
        return toplist
    
    def get_sublist(self,S_Syokatu):

        params='DispID=search&FunctionID=01&Mode=&S_Attest_Date_F=&S_Attest_Date_T=&S_Activity_Field_Bit=00000000000000000&S_Syokatu=%s&S_NPO_Name=&DATE_SYEAR=&DATE_SMONTH=&DATE_SDAY=&S_MDSCHCOND=1&DATE_EYEAR=&DATE_EMONTH=&DATE_EDAY=&S_Perfecture_Main=&S_Address_Main=&S_Address_Sub=&S_Purpose='
        
        webdoc = self.fetch('/npoportal/Portal_searchresult',
                       params=params % S_Syokatu )

        anchors = webdoc.xpathEval('//a[contains(@href,"ShowDetail")]')
        sublist = [x.prop('href')[23:31] for x in anchors]

        return sublist

    def get_labels(self):
        return [x[0] for x in FIELDS] + [x[0] for x in AREAS]
    
    def get_infopage(self,S_Syokatu,NPO_ID):

        params = 'DispID=searchresult&FunctionID=01&Mode=&NPO_ID=%s&S_Syokatu=%s&S_NPO_Name=&S_APP_Code=null&S_Attest_Date_F=&S_MDSCHCOND=1&S_Attest_Date_T=&S_Perfecture_Main=&S_Address_Main=&S_Address_Sub=&S_Purpose=&S_Activity_Field_Bit=00000000000000000'
        
        webdoc = self.fetch('/npoportal/Portal_detail',
                           params=params % (NPO_ID,S_Syokatu))

        fields = []
        field = ''
        for field in [x[1] for x in FIELDS]:
            item = webdoc.xpathEval('//td[contains(.,"'+field+'")]//following-sibling::td')[0].content
            if field == '法人認証年月日':
                r = re.match(DATE_RX,item)
                if r:
                    item = '%s-%s-%s'%(r.group(1),r.group(2),r.group(3))
                else:
                    item = '0000-00-00'
            fields.append(item)
            
        areas = []
        for area in [x[1] for x in AREAS]:
            item = webdoc.xpathEval('//table[@summary="活動分野の表"]//td[contains(.,"'+area+'")]//preceding-sibling::td//img')
            if not item:
                item = webdoc.xpathEval('//table[@summary="活動分野の表"]//td[contains(.,"'+area+'")]//img')
            item = item[-1].prop('src')
            if item.strip().endswith('on.gif'):
                item = 'TRUE'
            else:
                item = 'false'
            
            areas.append(item)
        return [x.strip() for x in fields + areas]
