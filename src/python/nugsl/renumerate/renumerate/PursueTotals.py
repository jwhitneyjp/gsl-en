''' Module
'''

from types import ListType, DictType
from copy import copy
import sys
from AmbiguousNumber import ambiguousNumber

class AmbiguityException(Exception):
    pass

class pursueTotals(ListType):
    ''' Seek totals and grand totals in a list of unambiguous number lists.
    
        Stored value is a list of numbers stamped as values, totals or
        grand totals.
    '''

    def __init__(self, assumptions, penalty_engine, debug=0):
        self.debug = debug
        self.penalty_engine = penalty_engine
        self.assumptions = assumptions
        self.process_assumptions()

    def process_assumptions(self):
        ''' Exhaust all configurations of all assumptions in pursuit of a valid set of totals
        
            This is the top-level method for the processing of assumptions.  It returns
            the pursueTotals object itself, either empty, or as a list of ambiguousNumber
            objects with appropriate metadata.
        '''
        self.candidates = []
        self.success = False
        self.fallback = None
        self.assumptions_count = 0
        self.specs_count = 0
        self.retries_count = 0
        for assumption in self.assumptions:
            if self.success: break
            self.assumptions_count += 1
            spec_seed = [assumptionSpec()]
            self.process_spec_seed(assumption, spec_seed)
            #sys.stdout.write('!')
            #sys.stdout.flush()
        if self.candidates:
            mx = max( [x[-1] for x in self.candidates] )
            if self.fallback > mx:
                self.fallback.info.update( {'state': spec_seed[0].GRAND_TOTAL } )
                self.append( self.fallback )
            else:
                for x in self.candidates:
                    if x[-1] == mx:
                        self.extend( x )
                        break
        elif self.fallback:
            self.fallback.info.update( {'state': spec_seed[0].GRAND_TOTAL } )
            self.append( self.fallback )
        return self

    def process_spec_seed(self, assumption, spec_seed):
        for spec in spec_seed:
            if self.success: break
            self.specs_count += 1
            penalty_engine = self.penalty_engine( assumption, spec )
            if self.debug:
                print '----------------------------------'
                for offender in penalty_engine.offenders:
                    n = assumption[offender[1]]
                    print '    %d @ %s,%s,%s (%s)' % (n,n.info['line'],n.info['fromstart'],n.info['sequence'],n.info['penalty'])
            offenders = [None] + [x[1] for x in penalty_engine.offenders]
            self.process_offenders( assumption, spec, offenders )
            #sys.stdout.write('+')
            #sys.stdout.flush()
            if spec.has_total():
                new_spec = spec.unwind_total()
                spec_seed.append( new_spec )
                
    def process_offenders(self, assumption, spec, offenders):
        for offender in offenders:
            if self.success: break
            self.retries_count += 1
            if offender != None:
                spec.mark_cruft(offender)
            self.process_one_series( assumption, spec)
            #sys.stdout.write('-')
            #sys.stdout.flush()

    def process_one_series(self, assumption, spec):
        provisional_total = 0
        totals = []
        seen_total_hint = False
        for pos in range(0, len(assumption), 1):
            if self.success: break
            if spec[pos] == spec.CRUFT:
                continue
            number = assumption[pos]
            if not seen_total_hint and number == 0 and number.info['category'] == 'Total':
                if assumption.zero_ok( pos, spec ):
                    seen_total_hint = True
                    spec[pos] = spec.GRAND_TOTAL
                    new_candidate = assumption.condense(spec)
                    spec.pop(pos)
                    self.candidates.append( new_candidate )
                continue
            if number != 0 and spec[pos] != spec.NON_TOTAL:
                #print 'pos/key: %s, number: %s, spec[pos]: %s' % (pos,number,spec[pos])
                if number == provisional_total:
                    if number.info['category'] == 'Total':
                        seen_total_hint = True
                    spec[pos] = spec.TOTAL
                    totals.append( provisional_total )
                    provisional_total = 0
                    number_of_totals = 0
                    for key in spec.keys():
                        if spec[key] == spec.TOTAL or spec[key] == spec.NON_TOTAL:
                            number_of_totals += 1
                    if number.info['category'] == 'Total' and number_of_totals == 1:
                        new_candidate = assumption.condense(spec)
                        self.candidates.append( new_candidate )
                    continue
                if sum(totals) and number == sum(totals) + provisional_total:
                    spec[pos] = spec.GRAND_TOTAL
                    #
                    # Aha!  Condense affected the spec.  Now _that_ is evil.
                    #
                    self.candidates.append( assumption.condense(spec) )
                    break
                #
                # XXX Untested
                if not seen_total_hint and number.info['category'] == 'Total':
                    seen_total_hint = True
                    nstr = str(number.str)
                    if len(nstr) % 2 == 0:
                        if nstr[len(nstr)/2:] == nstr[:len(nstr)/2]:
                            nstr = nstr[:len(nstr)/2]
                    self.fallback = ambiguousNumber( nstr, number.info.copy())
                if number.info['category'] == 'Total':
                    seen_total_hint = True
            provisional_total += number
            #sys.stdout.write('.')
            #sys.stdout.flush()
        
class assumptionSpec(DictType):

    def __init__(self):
        self.CRUFT = 0
        self.TOTAL = 1
        self.GRAND_TOTAL = 2
        self.NON_TOTAL = 3
        self.ZERO_TOTAL = 4

    def __getitem__(self, key):
        if self.has_key(key):
            return DictType.__getitem__(self, key)
        else:
            return None

    def mark_cruft(self, pos):
        ''' Mark the number at the specified position as cruft
        '''
        self[pos] = self.CRUFT
        
    def mark_total(self, pos):
        ''' Mark the number at the specified position as a total
        '''
        self[pos] = self.TOTAL

    def mark_grand_total(self, pos):
        ''' Mark the number at the specified position as a grand total
        '''
        self[pos] = self.GRAND_TOTAL

    def cruft_count(self):
        cruftcount = 0
        for key in self.keys():
            if self[key] == self.CRUFT:
                cruftcount += 1
        return cruftcount

    def unwind_total(self):
        ''' Mark the specified number as a non-total
        
            Returns the position of the number on success,
            otherwise None.
        '''
        spec_as_list = self.spec_as_list()
        spec_copy = copy( self )
        for pos in range( len(spec_as_list)-1,-1,-1 ):
            if spec_as_list[pos][1] == self.TOTAL:
                key = spec_as_list[pos][0]
                spec_copy[key] = self.NON_TOTAL
                return spec_copy
        return None

    def has_total(self):
        ''' Check for a total in current spec.
        
            Return True of total exists, otherwise False.
        '''
        positions = [x[1] for x in self.spec_as_list()]
        if self.TOTAL in positions:
            return True
        return False
    
    def spec_as_list(self):
        ''' Return spec dictionary as a sorted list of tuples
        
            This is a workaround, there may be a more efficient way of
            getting both map and list behaviour from the assumptionSpec
            object.
        '''
        spec_as_list = [ (k,self[k]) for k in self.keys() ]
        spec_as_list.sort( self.spec_sort )
        return spec_as_list

    def spec_sort(self, a, b):
        if a[0] > b[0]:
            return 1
        elif a[0] == b[0]:
            return 0
        else:
            return -1

