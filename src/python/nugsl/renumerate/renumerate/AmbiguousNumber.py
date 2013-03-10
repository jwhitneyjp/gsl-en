''' Module
'''

from types import LongType, DictType

class ambiguousNumber(LongType):
    """ Simple wrapper class for numbers.
    
        This stores several items of metadata on a number, which
	travel with it through the remainder of processing.  The
	is_mergeable attribute is used during post-processing,
	ultimately to form up unambiguous assumptionObjects for the
	attempts to find totals.  The info attribute is a dict
	containing further items of metadata, including the category
	stamp in effect at this position; the number of
	ambiguousClusters in the line in which this number appears;
	the distance of this number from the start of the line; and
	the distance of this number from the end of the line. The
	positional values are used to assign penalties in advance of
	each retry attempt when pursuing totals within an
	assumptionObject.  The str attribute is used to preserve
        leading zeros on the string with which objects of this class
        are initialized.
	
        Special functions for pickle, copy and deepcopy are needed
	because the object instantiation interface differs from that
	of the standard long integer type.
    """
    def __new__(self, s, info):
        if not isinstance(info, DictType):
            raise TypeError
        if len(s) == 0:
            return None
        else:
            i = int( s )
            return LongType.__new__(self, i )

    def __init__(self, s, info):
        self.str = s
        if len(self.str) % 3 or self < 0:
            self.is_mergeable = False
        else:
            self.is_mergeable = True
        self.info = info

    # support for pickling, copy, and deepcopy
    def __reduce__(self):
        return (self.__class__, (self.str, self.info.copy()))

    def __copy__(self):
        return self.__class__(self.str, self.info.copy())

    def __deepcopy__(self, memo):
        return self.__class__(self.str, self.info.copy())

    def update(self, **info):
        ''' Update the info dictionary for this number.
        
            The number of items in a line and the absolute sequence
            position of a number are not known until the final collation
            of numbers into a single list by the get_assumption method
            of the assumptionsList class.  This method is invoked
            at that time.
        '''
        self.info.update( info )

    def state(self):
        if self.info.has_key('state'):
            return self.info['state']
        else:
            return ''
