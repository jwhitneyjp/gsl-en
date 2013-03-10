'''
    Module
'''

import unittest
from tagtool import tagFix
from tagtool.TagFix import TaggingError
import re

class TestTagFix(unittest.TestCase):

    def setUp(self):
        self.tagFix = tagFix()
    
    def testNoop(self):
        txt = '<x></x>'
        res = self.tagFix.tagfix('y',txt)
        self.assertEqual(txt,res)
        
if __name__ == "__main__":
    unittest.main()
