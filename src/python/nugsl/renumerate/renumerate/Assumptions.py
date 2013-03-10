''' Module
'''

from types import ListType, DictType
from exceptions import Exception
from copy import copy
from PenaltyEngine import penaltyEngine
from AmbiguousCluster import ResolveMinusSpliceError
from AmbiguousNumber import ambiguousNumber
import sys
from Type1Line import type1Line
from Type2Line import type2Line

class AmbiguityException(Exception):
    pass

class ThisCannotHappenException(Exception):
    pass

class assumptionsList(ListType):

    def __init__(self, biglist, line_module, combination_limit=500):
        self.line_type = line_module.split('.')[-1].lower()
        self.combination_limit = combination_limit
        self.ambig_config_sets = self.get_ambig_config( biglist )
        self.generate_assumptions( biglist )

    def generate_assumptions(self, biglist ):
        for ambig_config in self.ambig_config_sets:
            fresh_assumption = self.get_assumption( biglist, ambig_config )
            if fresh_assumption:
                self.append( fresh_assumption )

    def get_ambig_config(self, biglist ):
        ''' Return a spec object representing all possible combinations of ambiguous clusters
        '''
        self.breakme = False
        info = self.get_ambig_info( biglist )
        seed = [1 for x in info]
        combinations = [seed]
        for spos in range(0,len(seed),1):
            if self.breakme: break
            cluster_split = seed[spos]
            cluster_length = info[spos]
            for apos in range(1,cluster_length,1):
                if self.breakme: break
                for cpos in range(len(combinations)-1,-1,-1):
                    combination = copy(combinations[cpos])
                    #
                    # A fixed combination is just a split position
                    combination[spos] = apos
                    if len(combinations) > self.combination_limit:
                        self.breakme = True
                        break
                    if not combination in combinations:
                        combinations.append(combination)
        return combinations

    def get_ambig_info(self, biglist):
        ''' Return positions and lengths of clusters as a list of tuples
        '''
        info = []
        pos = 0
        for line in biglist:
            for cluster in line:
                info.append( len(cluster)+1 )
        return info

    def get_assumption(self, biglist, ambig_config):
        assumption = assumptionObject( self.line_type )
        cluster_pos = 0
        position_pos = 0
        line_pos = 0
        for line in biglist:
            fromstart_pos = 0
            for cluster in line:
                ##############################################################
                # This stuff around cluster resolution needs some attention
                # to make it more easily comprehensible.
                #
                # print '%d -> %s' % (ambig_config[config_pos],cluster)
                ##############################################################
                try:
                    cluster_tuple = cluster.resolve( ambig_config[cluster_pos] )
                except ResolveMinusSpliceError:
                    return None
                for number in cluster_tuple:
                    if number != None:
                        number.update( sequence=position_pos, line=line_pos, fromstart=fromstart_pos )
                        assumption.append( number )
                        position_pos += 1
                        fromstart_pos += 1
                cluster_pos += 1
            for p in range(position_pos-fromstart_pos, position_pos, 1):
                length = fromstart_pos
                fromend = length - assumption[p].info['fromstart'] - 1
                assumption[p].update( length=length, fromend=fromend )
            line_pos += 1
        return assumption
    
class assumptionObject(ListType):

    def __init__(self, line_type):
        ListType.__init__(self)
        self.line_type = line_type

    def length(self, spec):
        ''' Return length of assumptionObject, excluding CRUFT items
        '''
        return len(self) - spec.cruft_count()
    
    def zero_ok(self, pos, spec):
        ''' Approve or disapprove treating number at pos as a total
        
            Checks whether there are more zeros than other
            numbers before pos, excluding numbers marked as CRUFT
        '''
        if self.line_type == 'type2line':
            return False
        zeros = 0
        others = 0
        for p in range(0,pos,1):
            if spec[p] == spec.CRUFT:
                continue
            if self[p].str == '0':
                zeros += 1
            else:
                others += 1
        #print 'pos: %s, zeros: %d, others: %d' % (pos,zeros,others)
        #print self
        if zeros > others:
            return True
        else:
            return False

    def condense(self, oldspec):
        ''' Return an unambiguous structured list of numbers
        
            Starting with an assumption, build a new list that does
            not contain cruft numbers, and consists of component numbers,
            totals, and a grand total.
            
            The starting assumption may take one of three forms.  It may
            end in a grand total of zero.  It may end in a bare total.
            or it may end in a grand total.  Each case is processed as
            required to produce the final structured list of numbers.
        '''
        new = assumptionObject( [] )
        spec = copy(oldspec)
        aggressive_delete = True
        force_totals = False
        #
        # Compose a new list of numbers, containing no cruft, and
        # no trailers.
        append = False
        for pos in range(len(self)-1,-1,-1):
            if spec[pos] == spec.CRUFT:
                continue
            if not append and spec[pos] == spec.NON_TOTAL:
                continue
            if spec[pos]:
                append = True
            if append:
                new.append( ambiguousNumber( self[pos].str, self[pos].info.copy() ) )
                if spec[pos]:
                    new[-1].update( state=spec[pos] )
        new.reverse()
        #
        # We're not interested in zeros
        for pos in range(len(new)-2,-1,-1):
            if new[pos] == 0:
                new.pop(pos)
        #
        # Just in case
        if new[-1] == 0:
            new[-1].update( state=spec.GRAND_TOTAL )
            for pos in range(len(new)-2,-1,-1):
                new.pop(pos)
        #
        # Properly formed lists should be okay as they are.
        elif new[-1].state() == spec.GRAND_TOTAL:
            pass
        #
        # Normalize lists that include ordinary components in
        # the grand total.
        elif new[-1].state() == spec.TOTAL:
            new[-1].update( state=spec.GRAND_TOTAL )
            force_totals = True
            for pos in range(len(new)-2,-1,-1):
                if new[pos].state():
                    force_totals = False
                if force_totals:
                    num = new[pos].str
                    info = new[pos].info.copy()
                    new.insert(pos+1, ambiguousNumber( num, info ) )
                    new[pos+1].update( state=spec.TOTAL )

        else:
            print new
            print 'last value: %d, state of last value: %d' % (new[-1],new[-1].state())
            raise ThisCannotHappenException
        return new
