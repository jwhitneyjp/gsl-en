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

PARAMS = 'pagenum=%d&id=&isdelete=0&organization_name=&purpose_text=&content=&andor=1'

DETAIL_PARAMS = 'pagenum=%d&id=%s&isdelete=0&organization_name=&purpose_text=&content=&andor=1'

MEMBERS = '.*?(?:個人会員 *([0-9]+)名)*.*?(?:団体会員 *([0-9]+)団体)*.*'

FIELDS = []
FIELDS.append( ('phonetic','団体名フリガナ') )
FIELDS.append( ('location','所在地') )
FIELDS.append( ('founding','団体設立年') )
FIELDS.append( ('incorporation','法人格取得年') )
FIELDS.append( ('representative','代表者') )
FIELDS.append( ('phone','電話番号') )
FIELDS.append( ('fax','FAX') )
FIELDS.append( ('url','URL') )
FIELDS.append( ('email','Eメール') )
FIELDS.append( ('budget','年間予算規模') )
FIELDS.append( ('members','会員数') )
FIELDS.append( ('environmentalism','環境保全活動') )
FIELDS.append( ('purpose','団体の設立目的') )
FIELDS.append( ('area','活動の分野') )
FIELDS.append( ('method','活動のしかた') )
FIELDS.append( ('activities','活動の内容') )
FIELDS.append( ('action_area','活動を行う地域') )
FIELDS.append( ('participation','参加方法') )
FIELDS.append( ('contact','連絡方法') )
FIELDS.append( ('publications','定期刊行物') )
FIELDS.append( ('blurb','一言PR') )


class envoRip:
    def __init__(self, debug=False):
        self.debug = debug

    def fetch(self,stub='/jfge/NGO2006/html/result.php',params=[]):
        urlbase = 'http://www.erca.go.jp'
        uopen = urllib2.urlopen
        request = urllib2.Request
        urlparams = params
        txheaders =  {}
        txheaders['User-agent'] = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        txheaders['Content-Type'] = 'application/x-www-form-urlencoded'
        
        req = request(urlbase + stub, urlparams, txheaders)

        ifh = uopen(req)
        html = ifh.read().decode('Shift-JIS','replace')
        
        html = html.replace(unichr(12), u'')
        html = html.replace(unichr(11), u'')
        html = html.replace('&nbsp;',' ')
        html = re.sub('[&＆]([^;]*)$','&amp;\\1',html)
        
        html = html.replace('";>',';">')
        
        html = html.encode('Shift-JIS','replace')
        
        #open('ERRORS.html','w+').write( html )
        
        doc = libxml2.htmlParseDoc(html,'SHIFT-JIS')

        return doc
    
    def get_size(self):
        webdoc = self.fetch()
        size = webdoc.xpathEval('//span[@class = "c-red"]')
        size = size[0].content.decode('utf8','replace')
        return int( size[:-1] )

    def get_labels(self):
        labels = ["name"] + [x[0] for x in FIELDS][:]
        pos = labels.index( 'members' )
        labels[pos] = 'persons'
        labels.insert(pos+1,'organizations')
        return labels

    def get_list(self,page=0):
        params = PARAMS % page
        webdoc = self.fetch(params=params)
        items = [x.prop('href') for x in webdoc.xpathEval('//a[contains(@href,"detail")]')]
        items = [x[18:-1] for x in items]
        return items

    def sanitize(self,x):
        return x.replace('　','')
    
    def get_detail(self,page,item_id):
        
        params = DETAIL_PARAMS % (page, item_id)
        webdoc = self.fetch(stub='/jfge/NGO2006/html/detail.php',params=params)

        name = self.sanitize( webdoc.xpathEval('//table[@width = "100%"]/tr/td')[0].content.strip() )
        
        fields = []
        for field in FIELDS:
            data = webdoc.xpathEval('//table[@width = "485"]//tr//td[contains(.,"'+field[1]+'")]//following::td')
            if data:
                data = self.sanitize( data[0].content.strip() )
                if field[1] == '会員数':
                    r = re.match(MEMBERS,data)
                    if r:
                        fields.append( r.group(1) )
                        fields.append( r.group(2) )
                    else:
                        fields.append( data )
                        fields.append( "" )
                else:
                    fields.append( data )
            else:
                fields.append( "" )
                fields.append( "" ) 
   
        return [name] + fields
