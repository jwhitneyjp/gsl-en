''' Module
'''
import re
import urllib

def deleteme(txt):
        return ''

def quote_href(txt):
        r = re.match('.*href="([^"?]*)\?([^"]*)".*',txt)
        stub=r.group(1)
        args=urllib.quote( r.group(2) )
        return re.sub('(href=)"([^"]*)"','href="%s?%s"' % (stub, args),txt)

def quote_onclick(txt):
        r = re.match('.*onClick="([^"?]*)\?([^"]*)".*',txt)
        stub=r.group(1)
        args=urllib.quote( r.group(2) )
        return re.sub('(onClick=)"([^"]*)"','onClick="%s?%s"' % (stub, args),txt)

def fixbaddiv(txt):
        return re.sub('<div[^>]*>','',txt)

