''' Module
'''

from types import ListType

class clusterList(ListType):
    
    def strs(self):
        return [x.str for x in self]

    