''' Module
'''

from LineList import lineList

class type1Line(lineList):

    def __init__(self, s, category_hinter, line_number=None ):
        ''' Attempt to disambiguate assuming a maximum of two numbers
        
            This resolves if there is a single unambiguous break-point
	    in the middle of the string, or if only one number can be
	    formed through concatenation, such that it cannot be
	    broken down further without making it smaller than the
	    concatenation of the remaining string.  This is the
	    fallback resolution method, and returns a multi-element
	    ambiguous number at the point where resolution fails.
        '''
        lineList.__init__(self, s, category_hinter, line_number=line_number )
        for pos in range(0,len(self),1):
            self[pos] = self.attempt_merge( self[pos] )

    def attempt_merge(self, cluster ):
        #
        # Check for an unmergeable break-point
        bestpos = None
        break_points = []
        for pos in range(0,len(cluster)-1,1):
            if not cluster[pos].is_mergeable:
                break_points.append( pos+1 )
        if len(break_points) == 1:
            bestpos = break_points[0]
        else:
            #
            # Fallback
            for pos in range(1,len(cluster),1):
                if not cluster[pos-1].is_mergeable: break
                if cluster.combine(0,pos) < cluster.combine(pos,None):
                    bestpos = pos+1
                    if not cluster[pos].is_mergeable: break
                else:
                    break
        if bestpos:
            cluster[0] = cluster.combine(0,bestpos)
            for pos in range(len(cluster)-1,0,-1):
                if pos < bestpos:
                    cluster.pop(pos)
        
        return cluster
