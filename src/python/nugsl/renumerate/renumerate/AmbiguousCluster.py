#-*- encoding: utf8 -*-
''' Module
'''

import re
from AmbiguousNumber import ambiguousNumber
from copy import copy
from ClusterList import clusterList
from exceptions import Exception
from types import StringTypes, DictType, LongType, IntType, ListType

class ResolveFromZeroError(Exception):
    pass

class ResolveMinusSpliceError(Exception):
    pass

class ClusterArgumentError(Exception):
    def __init__(self, t):
        self.args = list(self.args) + ['%s arg "%s" to ambiguousCluster must be %s' % t]

class ambiguousCluster(clusterList):
    ''' Class to disambiguate a list of numbers based on punctuation alone
    
        After instantiation, the object list attribute will contain a 
        (possibly) simplified list of numbers.  This class also provides
        methods for managing the splicing of ambiguous numbers into larger
        units.
    '''
    def __init__(self, nums, info):
        self.info = self.init_info(nums,info)
        self.extend( self.init_nums(nums) )

    def __getslice__(self, start, end):
        start = max(start, 0); end = max(end, 0);
        return self.__class__(self.__getitem__(slice(start,end,None)), self.info.copy())

    def init_info(self, nums, info):
        if isinstance(nums, ambiguousNumber):
            return nums.info
        elif isinstance(info, DictType):
            return info
        else:
            raise ClusterArgumentError(('Second','info','<DictType>'))

    def init_nums(self, nums):
        if isinstance(nums, ListType):
            return nums
        elif isinstance(nums, ambiguousNumber):
            return [nums]
        elif isinstance(nums, StringTypes):
            nums = nums.split()
            nums.reverse()
            l = []
            for num in nums:
                l.append( ambiguousNumber( num, self.info ) )
            return l
        else:
            raise ClusterArgumentError(('First','nums','<ambiguousCluster>, <ambiguousNumber> or <string>'))

    def combine(self, start, end):
        ''' Combine a slice of numbers.
        
            Numbers are combined in reverse order, concatenating them
            as strings, then returning them as a single ambiguousNumber.
            An attempt to combine a string with an embedded negative
	    sign will return None.
        '''
        numlist = self.strs()[start:end]
        numlist.reverse()
        try:
            return ambiguousNumber( ''.join( numlist ), self.info.copy() )
        except ValueError:
            return None

    def resolve(self, pos):
        ''' Return one or two integers representing a split-point in the cluster
        
            Variable names "first" and "second" refer to the internal list order.
            This is reversed to put the integers in page order for final output.
            Receiving functions must cope with the possibility that the value of 
            an integer may be None.
        '''
        if pos == 0:
            raise ResolveFromZeroError
        if pos > 1:
            for p in range(0,pos-1,1):
                if self[p] < 0:
                    raise ResolveMinusSpliceError
        if pos < len(self)-1:
            for p in range(pos,len(self)-1,1):
                if self[p] < 0:
                    raise ResolveMinusSpliceError
        first = self.combine(0,pos)
        second = self.combine(pos,None)
        return (second, first)
