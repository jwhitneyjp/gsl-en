''' Module
'''

from LineList import lineList
from AmbiguousCluster import ambiguousCluster

class type2Line(lineList):

    def __init__(self, s, category_hinter, line_number=None):
        """ Attempt to disambiguate assuming a cross-total exists
        
            This resolves if three numbers exist in a cluster such
	    that the third is the difference of the first two.
	    Resolution either works or it doesn't; the value returned
	    is an ambiguousCluster with a single value, or an empty
	    string.
        """
        lineList.__init__(self, s, category_hinter, line_number=line_number)
        for pos in range(len(self)-1,-1,-1):
            cluster = self[pos]
            income = None
            if len(cluster) > 2:
                income = self.cross_total( cluster )
            if income == None and len(cluster) > 1:
                income = self.paired_numbers( cluster )
            if income == None:
                self.pop(pos)
                continue
            self[pos] = ambiguousCluster( income, {} )
        self.max_only()

    def max_only(self):
        mx = None
        for i in self:
            if i[0] > mx:
                mx = i[0]
        for pos in range(len(self)-1,-1,-1):
            if self[pos][0] != mx:
                self.pop(pos)
        for pos in range(len(self)-2,-1,-1):
            self.pop(pos)

    def cross_total(self, cluster ):
        for pos in range(1,len(cluster)-1,1):
            for ppos in range(pos+1,len(cluster),1):
                budget = cluster.combine(ppos,None)
                income = cluster.combine(pos,ppos)
                difference = cluster.combine(0,pos)
                if None in [budget,income,difference]:
                    continue
                if budget - income == difference:
                    return cluster.combine(pos,ppos)

    def paired_numbers(self, cluster ):
        for pos in range(1,len(cluster)-1,1):
            if not cluster[pos].is_mergeable:
                return None
            one = cluster.combine(0,pos)
            other = cluster.combine(pos,None)
            if one and other and one == -other:
                return other
