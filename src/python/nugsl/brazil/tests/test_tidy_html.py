'''
    Module
'''

import sys
import unittest,os,sys
sys.path.append( os.getcwd() )

import unittest
from brazil.TidyHtml import tidyHtml

class TestFix(unittest.TestCase):

    def setUp(self):
        pass

    def testDeleteScript(self):
        tidy = tidyHtml( '<html>wow' )
        self.assertEqual( tidy.html, '<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 3.2//EN">\n\n<html>\n<head>\n  <meta name="generator" content="HTML Tidy for Linux/x86 (vers 1 September 2005), see www.w3.org">\n\n  <title></title>\n</head>\n\n<body>\n  wow\n</body>\n</html>\n')
    
if __name__ == "__main__":
    unittest.main()
