'''
    Module
'''

import sys
import unittest,os,sys
sys.path.append( os.getcwd() )

import unittest
from brazil.FixHtml import fixHtml

class dummyFixHtml(fixHtml):
    def __init__(self):
        pass

class TestFix(unittest.TestCase):

    def setUp(self):
        self.fix = dummyFixHtml()

    def testDeleteScript(self):
        self.fix.html = '<div><script>Wow</script></div>'
        self.fix.delete_script()
        self.assertEqual( self.fix.html, '<div></div>')
    
    def testQuoteHref(self):
        self.fix.html = '<div><a href="myurl?hello=1&good_bye=2">Wow</a></div>'
        self.fix.quote_href()
        self.assertEqual( self.fix.html, '<div><a href="myurl?hello%3D1%26good_bye%3D2">Wow</a></div>')
    
    def testQuoteOnclick(self):
        self.fix.html = '<div><a onClick="myurl?hello=1&good_bye=2">Wow</a></div>'
        self.fix.quote_onclick()
        self.assertEqual( self.fix.html, '<div><a onClick="myurl?hello%3D1%26good_bye%3D2">Wow</a></div>')
    
if __name__ == "__main__":
    unittest.main()
