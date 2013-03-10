''' Module
'''

from nugsl.tagtool import tagFix
from Utils import *

class fixHtml:

    def __init__(self, s):
        self.html = s
        self.delete_script()
        self.quote_href()
        self.quote_onclick()

    def delete_script(self):
        t = tagFix()
        self.html = t.tagfix('script',self.html,
                             matchfunc=deleteme)

    def quote_href(self):
        t = tagFix()
        self.html = t.tagfix('a',self.html,
                             regex='.*href="([^"?]*)\?([^"]*)".*',
                             matchfunc=quote_href)

    def quote_onclick(self):
        t = tagFix()
        self.html = t.tagfix('a',self.html,
                             regex='.*onClick="([^"?]*)\?([^"]*)".*',
                             matchfunc=quote_onclick)

