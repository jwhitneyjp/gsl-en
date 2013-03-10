#-*- encoding: utf8 -*-
''' Module

    A module for stuff related to number penalties.
'''

class penaltyEngineBase:
    ''' Class to manage and calculate number penalties.
    
        Number penalties are used to decide which item to
        discard before each retry when pursuing totals.
    '''

    def __init__(self, assumption, spec):
        self.spec = spec
        self.get_penalizers()
        self.assign_penalties_to_assumption( assumption )
        self.get_offenders( assumption )
        
    def get_penalizers(self):
        self.penalizers = []
        for penalizer in dir(self):
            if penalizer.endswith('_penalty'):
                self.penalizers.append( getattr(self, penalizer) )

    def assign_penalties_to_assumption(self, assumption ):
        for pos in range(0, len(assumption), 1):
            self.assign_penalties_to_number( assumption, pos )

    def assign_penalties_to_number(self, assumption, pos ):
        penalty = sum( [ penalizer(assumption, pos) for penalizer in self.penalizers ] )
        assumption[pos].update( penalty=penalty )

    def get_offenders(self, assumption ):
        self.offenders = []
        for number in assumption:
            if number.info['penalty'] < 0:
                self.offenders.append( ( number.info['penalty'], number.info['sequence'] ) )
        self.offenders.sort( self.offenders_sorter )

    def offenders_sorter(self, a, b):
        if a[0] > b[0]:
            return 1
        elif a[0] == b[0]:
            return 0
        else:
            return -1
