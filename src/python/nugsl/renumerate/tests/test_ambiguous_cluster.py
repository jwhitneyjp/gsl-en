#-*- encoding: utf8 -*-
''' Module
'''

import unittest
import unittest,os,sys
sys.path.append( os.getcwd() )
from renumerate.AmbiguousNumber import ambiguousNumber
from renumerate.AmbiguousCluster import *

class bareAC(ambiguousCluster):
    def __init__(self, nums, info):
        pass

class TestCombineOperations(unittest.TestCase):
        
    def setUp(self):
        self.c = ambiguousCluster('1 2 3 4 5',{})
        
    def testNilCluster(self):
        self.c = ambiguousCluster('',{})
        self.assertEqual(self.c.combine(0,1),None)
    
    def testSpanMinusSign(self):
        self.c = ambiguousCluster('1 2 3 -4 5',{})
        self.assertEqual(self.c.combine(0,3),None)
    
    def testOverLength(self):
        self.assertEqual(self.c.combine(0,6),12345)
        
    def testNormalRight(self):
        self.assertEqual(self.c.combine(0,3),345)
    
    def testNormalMid(self):
        self.assertEqual(self.c.combine(1,3),34)
    
    def testInvalidStart(self):
        self.assertRaises(TypeError, self.c.combine,'0',3)
        
    def testInvalidEnd(self):
        self.assertRaises(TypeError, self.c.combine,0,'3')
        
    def testNoneToEnd(self):
        self.assertEqual(self.c.combine(2,None),123)

    def testNoneToStart(self):
        self.assertEqual(self.c.combine(None,3),345)

class TestInitMethods(unittest.TestCase):

    def setUp(self):
        self.c = bareAC( None,None)

    def testInitInfoError(self):
        self.assertRaises(ClusterArgumentError, self.c.init_info, 'string', 'string OOPS')

    def testInitNumberError(self):
        self.assertRaises(ClusterArgumentError, self.c.init_nums, 1)
        
    def testInitInfoAmbiguousNumber(self):
        n = ambiguousNumber('1',{'key1':'val1'})
        ret = self.c.init_info( n, {})
        self.assertEqual(ret['key1'],'val1')

    def testInitInfoDict(self):
        d = {'key1':'val1'}
        ret = self.c.init_info('blah',d)
        self.assertEqual(ret['key1'], 'val1')
        
    def testInitNumsNumber(self):
        n = ambiguousNumber('1',{})
        ret = self.c.init_nums(n)
        self.assertEqual(ret,[1])
        
    def testInitNumsString(self):
        n = '1'
        self.c.info={}
        ret = self.c.init_nums(n)
        self.assertEqual(ret,[1])

class TestInstantiation(unittest.TestCase):

    def testNilInstantiation(self):
        c = ambiguousCluster('',{})
        self.assertEqual(c,[])
        
    def testInvalidData(self):
        self.assertRaises(ValueError,ambiguousCluster,'1- 2',{})
        
class TestSlice(unittest.TestCase):
    def setUp(self):
        self.c = ambiguousCluster( '1 2 3', {} )
    
    def testSlice(self):
        self.new = self.c[1:]
        self.assertEqual(self.new, [2,1])
        
class TestResolve(unittest.TestCase):
    def setUp(self):
        self.c = ambiguousCluster( '1 2 3', {} )

    def testZeroOfThreeNegativeBlock(self):
        self.c = ambiguousCluster( '-1 2 3', {} )
        self.assertRaises( ResolveFromZeroError, self.c.resolve, 0 )
        
    def testOneOfThreeNegativeBlock(self):
        self.c = ambiguousCluster( '1 -2 3', {} )
        self.assertRaises( ResolveMinusSpliceError, self.c.resolve, 1 )

    def testTwoOfThreeNegativeBlock(self):
        self.c = ambiguousCluster( '1 2 -3', {} )
        self.assertRaises( ResolveMinusSpliceError, self.c.resolve, 2 )

    def testThreeOfThreeNegative(self):
        self.c = ambiguousCluster( '-1 2 3', {} )
        res = self.c.resolve(3)
        self.assertEqual(res, (None,-123))
        
    def testZeroOfThree(self):
        res = self.c.resolve
        self.assertRaises( ResolveFromZeroError, self.c.resolve, 0 )
        
    def testOneOfThree(self):
        res = self.c.resolve(1)
        self.assertEqual(res, (12,3))
        
    def testTwoOfThree(self):
        res = self.c.resolve(2)
        self.assertEqual(res, (1,23))
        
    def testThreeOfThree(self):
        res = self.c.resolve(3)
        self.assertEqual(res, (None,123))

if __name__ == "__main__":
    unittest.main()
    #loader = unittest.TestLoader()
    #tests = loader.loadTestsFromTestCase(TestResolve)
    #runner = unittest.TextTestRunner(verbosity=2) 
    #runner.run(tests)

