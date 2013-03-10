'''
    Module
'''

import sys
import unittest,os,sys
sys.path.append( os.getcwd() )

import unittest
from brazil.UnZip import unZip

class TestZip(unittest.TestCase):

    def setUp(self):
        pass

    def testGoodZip(self):
        content = unZip( 'tests/goodzip.ZIP' )
        self.assertTrue( content != None)
    
    def testBadZip(self):
        content = unZip( 'tests/badzip.ZIP' )
        self.assertTrue( content == None)
    
if __name__ == "__main__":
    unittest.main()
