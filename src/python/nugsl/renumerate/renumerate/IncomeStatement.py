''' Module
'''

#from renumerate.AmbiguousLine import ambiguousLine
from AmbiguousCluster import ambiguousCluster
from LineResolvers import lineResolvers
from Assumptions import assumptionsList
from PursueTotals import pursueTotals
from types import ListType
from DocumentChop import documentChop
from types import LongType

class incomeStatement(ListType):
    ''' Top-level class for financial statement OCR postparser
    
        This tool will attempt to reconstruct the numbers and sums
	contained in an OCR scan of a financial statement. This is
	mundane work, but more difficult than it might at first
	appear. The parsing engine performs a good deal of textual
	cleanup before first attempting to reconstruct the sums
	contained in the page as a set of double-entry accounting
	columns, and falling back to a totals-below-and-to-the-right
	format if the first attempt fails.  A categoryHinter object is
	required to instantiate this class.
        '''
    def __init__(self, category_hinter, penalty_engine ):
        self.category_hinter = category_hinter
        self.penalty_engine = penalty_engine
        self.raw = []
        
    def read(self, statement ):
        if type(statement) == type(u''):
            data = statement
        elif type(statement) == type(''):
            data = statement.decode('utf8')
        else:
            data = statement.read().decode('utf8')
        data = documentChop( self.category_hinter, data.strip().split('\n') )
        self.raw.extend( data )

    def analyze(self):
        totals = None
        resolvers = lineResolvers()
        max_value = 0
        for line_resolver in resolvers:
            preparsed_list = []
            for pos in range(0, len(self.raw), 1):
                result = line_resolver( self.raw[pos], self.category_hinter, line_number=pos )
                #
                # This moves unambiguous tokens outside their cluster
                result = self.disambiguate( result ) 
                preparsed_list.append( result )
            line_type = line_resolver.__module__.split('.')[0].lower()
            assumptions = assumptionsList( preparsed_list, line_type )
            for assumption in assumptions:
                if not isinstance(max(assumption),LongType):
                    print 'weird max number'
                if isinstance(max(assumption),LongType) and max(assumption) > max_value:
                    max_value = max(assumption)
            totals = pursueTotals( assumptions, self.penalty_engine )
            self.assumptions_count = totals.assumptions_count
            self.specs_count = totals.specs_count
            self.retries_count = totals.retries_count
            if totals:
                break
        self.max_value = max_value
        self.extend( totals )

    def disambiguate(self, clusters):
        mylist = []
        for cluster in clusters:
            buffer = []
            for pos in range(0,len(cluster),1):
                if cluster[pos].is_mergeable:
                    buffer.append( cluster[pos:] )
                    break
                else:
                    buffer.append( ambiguousCluster(cluster[pos], {} ) )
            buffer.reverse()
            mylist.extend( buffer )
        return mylist
