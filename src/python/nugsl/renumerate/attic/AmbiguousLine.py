#-*- encoding: utf8 -*-
''' Module
'''

import re
from renumerate.LineResolverPlugins.Type1Line import type1Line
from renumerate.LineResolverPlugins.Type2Line import type2Line
from renumerate.LineList import lineList

class ambiguousLine:
    ''' Class to prepare two partially cleaned versions of a line.
    
        A financial report might be presented in single-entry (type1) or
        double-entry (type2) form, and the portion of a line that is of
        interest is different for each.  This class prepares a
        version of the line suitable for each form of processing.  It
        takes a string consisting of a single line of text as input.
        The type2 attribute returns an unambiguous list of tokens appropriate
        for (first-attempted) double-entry processing.  In this case,
        some confidence can be placed in the returned income figure,
        even if the overall total fails.  The type1 attribute
        returns a potentially ambiguous list that may contain tokens
        with multiple elements.  Type1 processing requires a further
        layer of processing, to attempt every possible combination
        of elements in pursuit of a valid total, before the results
        can be trusted.
    '''
    
    def __init__(self, s, category_hinter, line_number=None):
        self.type1 = type1Line( s, category_hinter, line_number=line_number )
        self.type2 = type2Line( s, category_hinter, line_number=line_number )
