'''
    Module
'''

import sys
import unittest,os,sys
sys.path.append( os.getcwd() )

import unittest
from renumerate.ClusterList import clusterList

class dummyNum:
    def __init__(self):
        self.str = '0'

class TestMethods(unittest.TestCase):

    def setUp(self):
        self.c = clusterList()

    def testExtend(self):
        self.c.extend(['one'])
        self.assertEqual(self.c,['one'])

    def testAppend(self):
        self.c.append('two')
        self.assertEqual(self.c,['two'])

    def testStrsEmpty(self):
        self.assertEqual(self.c.strs(), [])
        
    def testStrsWithVals(self):
        
        self.c.extend( [ dummyNum() ] )
        self.assertEqual(self.c.strs(), ['0'])
        
if __name__ == "__main__":
    unittest.main()
