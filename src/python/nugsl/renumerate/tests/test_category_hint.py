#-*- encoding: utf8 -*-
'''
    Module
'''

import unittest
import os
import unittest,os,sys
sys.path.append( os.getcwd() )
from renumerate.CategoryHint import *
from ConfigParser import ConfigParser

class testCH(categoryHinter):
    def __init__(self, *args):
        ConfigParser.__init__(self)
        self.initialize_vars()

class TestHinter(unittest.TestCase):
    def setUp(self):
        pass
    
    def testConstructor(self):
        self.assertEqual( 1, 1 )

class TestConfigFromFile(unittest.TestCase):
    def setUp(self):
        self.hinter = testCH()

    def testLoadConfig(self):
        path = os.path.join('config', 'test-categories.conf')
        res = self.hinter.read( path ) 
        self.assertEqual( res, [path] )
        
class TestConfigFileCompiler(unittest.TestCase):
    def setUp(self):
        self.hinter = testCH()
        self.hinter.add_section('Start')
        self.hinter.set('Start','phrase1','mystart1')
        self.hinter.set('Start','phrase2','mystart2')
        self.hinter.add_section('End')
        self.hinter.set('End','phrase1','myend1')
        self.hinter.set('End','phrase2','myend2')
        self.hinter.add_section('SomeCategory')
        self.hinter.set('SomeCategory','phrase1','wowie')
        self.hinter.set('SomeCategory','phrase2','zowie')
        self.hinter.compile()

    def testLoadStart(self):
        self.assertEqual( self.hinter.re_start, '(?i)(mystart1|mystart2)' )  

    def testLoadEnd(self):
        self.assertEqual( self.hinter.re_end, '(?i)(myend1|myend2)' )  

    def testCompileOk(self):
        self.assertEqual( self.hinter.re, '(?i)(?:wowie|zowie)'.decode('utf8') )

class TestConfigFileExceptions(unittest.TestCase):
    def setUp(self):
        self.hinter = testCH()
    
    def testNoStart(self):
        self.hinter.add_section('End')
        self.hinter.add_section('SomeCategory')
        self.hinter.set('SomeCategory','phrase1','wowie-zowie')
        self.assertRaises( MissingStartException, self.hinter.validate)

    def testNoEnd(self):
        self.hinter.add_section('Start')
        self.hinter.add_section('SomeCategory')
        self.hinter.set('SomeCategory','phrase1','wowie-zowie')
        self.assertRaises( MissingEndException, self.hinter.validate)

    def testNoCategory(self):
        self.hinter.add_section('Start')
        self.hinter.add_section('End')
        self.assertRaises( MissingCategoryException, self.hinter.validate)

    def testNoPhrase(self):
        self.hinter.add_section('Start')
        self.hinter.set('Start','phrase1','mystart')
        self.hinter.add_section('End')
        self.hinter.set('End','phrase1','myend')
        self.hinter.add_section('SomeCategory')
        self.assertRaises( MissingPhraseException, self.hinter.validate)

    def testNoProblem(self):
        self.hinter.add_section('Start')
        self.hinter.set('Start','phrase1','mystart')
        self.hinter.add_section('End')
        self.hinter.set('End','phrase1','myend')
        self.hinter.add_section('SomeCategory')
        self.hinter.set('SomeCategory','phrase1','wowie-zowie')
        self.assertEqual( self.hinter.validate(), None )

class TestClassifier(unittest.TestCase):

    def setUp(self):
        self.hinter = testCH()
        self.hinter.addHint('Has o','o')
        self.hinter.addHint('Has 本'.decode('utf8'),'本'.decode('utf8'))

    def testRe(self):
        self.assertEqual( self.hinter.re, '(?i)(?:o|本)'.decode('utf8'))
        
    def testAppendToCategory(self):
        self.hinter.addHint('Has o', 'O')
        self.hinter.classify('O. Henry')
        self.assertEqual( self.hinter.current, 'Has o')
        
    def testSimpleString(self):
        self.hinter.classify('wow')
        self.assertEqual( self.hinter.current, 'Has o')
        
    def testNotMatching(self):
        self.hinter.classify('slog')
        self.hinter.classify('ziggy')
        self.assertEqual( self.hinter.current, 'Has o')
        
    def testKanji(self):
        self.hinter.classify('日本語'.decode('utf8'))
        self.assertEqual( self.hinter.current, 'Has 本'.decode('utf8'))

    def testFullWordMatch(self):
        self.hinter.classify('wow')
        self.assertEqual( self.hinter.current, 'Has o')

if __name__ == "__main__":
    unittest.main()

