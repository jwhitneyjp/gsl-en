''' Module
'''
from types import ListType

from Type1Line import type1Line
from Type2Line import type2Line

class lineResolvers(ListType):
    def __init__(self):
        self.append( type2Line )
        self.append( type1Line )
