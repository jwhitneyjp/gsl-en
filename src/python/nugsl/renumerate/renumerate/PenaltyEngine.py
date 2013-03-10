''' Module
'''

from PenaltyEngineBase import penaltyEngineBase
import re

class penaltyEngine(penaltyEngineBase):
    ''' Controlling methods for the number-discard penalty engine.

        Depending on the characteristics of your input data, you may 
        want to use this class as a template for creating your own
        custom penalty engine.

        The value returned when a number is fed to a "_penalty" method
	is one penalty value for that number.  The total penalty is
	the total of values from all methods applied to that number.  
	See the ambiguousNumber class for metadata values available
	during number processing.
    '''
    def all_ones_penalty(self, assumption, pos):
        penalty = 0
        number = assumption[pos]
        if len(number.str) > 3 and re.match('^[1]+$',number.str):
            penalty = -1100
        return penalty

    def explanatory_sum_penalty(self, assumption, pos):
        number = assumption[pos]
        penalty = 0
        if number.info['length'] > 2:
            if number.info['fromend'] == 0:
                if number * assumption[pos-1] == assumption[pos-2]:
                    penalty = -2000
            elif number.info['fromend'] == 1:
                if number * assumption[pos+1] == assumption[pos-1]:
                    penalty = -2000
        return penalty

    def bullet_numbers_penalty(self, assumption, pos):
        number = assumption[pos]
        penalty = 0
        if number.info['fromstart'] == 0:
            if len(number.str) == 1:
                penalty = -1000
            elif len(number.str) == 2:
                penalty =  -1000
        return penalty

    def top_dates_penalty(self, assumption, pos):
        number = assumption[pos]
        penalty = 0
        if number.info['line'] < 7:
            if len(number.str) < 3 or len(number.str) == 4:
                penalty = -2000
            else:
                penalty = -150
        return penalty

    #def no_category_penalty(self, assumption, pos):
    #    number = assumption[pos]
    #    penalty = 0
    #    if number.category() == 'Unknown':
    ##        penalty = -500
    #    return penalty

    def small_digits_penalty(self, assumption, pos):
        number = assumption[pos]
        penalty = 0
        if len(number.str) < 3:
            penalty = -1500
        #
        # NEVER drop a lone zero.
        if number == 0:
            penalty = 15000
        return penalty

    def reward_for_size_penalty(self, assumption, pos):
        number = assumption[pos]
        penalty = 0
        if len(number.str) > 3:
            penalty = +1000
        elif len(number.str) == 2:
            penalty = -5
        else:
            penalty = -10
        return penalty

    def reward_for_neighbours(self, assumption, pos):
        penalty = 0
        num = assumption[pos]
        if num.info['fromend'] == 0 and num.info['fromstart'] > 0:
            if num == assumption[pos-1]:
                penalty = +1800
        if num.fromend == 1:
            if num == assumption[pos+1]:
                penalty = +1800
        return penalty
