#-*- encoding: utf8 -*-
''' Module
'''

from AmbiguousCluster import ambiguousCluster
from types import ListType, StringTypes
import re

class lineList(ListType):
    ''' Abstraction of line data.
    
        This class provides methods for instantiating a line as a
        set of ambiguousClusters, and for trimming and evaluating
        its content.
    '''
    def __init__(self, s, category_hinter, line_number=None):
        self.category_hinter = category_hinter
        self.line_number = line_number
        self.init_line( s )
        
    def init_line(self, s):
        if isinstance(s, ListType):
            self.extend( s )
        elif isinstance(s, StringTypes):
            self.extend( self.init_string( s ) )
    
    def __getslice__(self, start, end):
        start = max(start, 0); end = max(end, 0);
        return self.__class__(self.__getitem__(slice(start,end,None)), self.category_hinter)

    def init_string(self, s):
        s = self.clean_string(s)
        return self.split_string(s)

    def clean_string(self, s):
        ''' A big, bad bundle of regular expressions.
        
            This should be made configurable for other sites.
        '''
        #
        # Wipe out nakaguro
        s = re.sub(' *・ *'.decode('utf8'),' ',s)
        #
        # Wipe out numbers that are almost certainly expanatory notes
        s = re.sub('\([^\(]*[^ △ー0-9][^\(]*[△ー 0-9]+[^\)]*\)'.decode('utf8'),'[NUMxNUM]',s)
        s = re.sub('\([^\(]*[△ー 0-9]+[^\)]*[^ △ー0-9][^\)]*\)'.decode('utf8'),'[NUMxNUM]',s)
        s = re.sub('[.,0-9]+ *(?:×|><) *[.,0-9]+'.decode('utf8'),'[NUMxNUM]',s)
        #
        # Wipe out lone numbers that cannot be part of a sum
        s = re.sub('([^- △ー×.,0-9])[1-9][0-9]*([^ ×.,0-9])'.decode('utf8'),'\\1[NUM]\\2',s)
        #
        # Cut all numbers that start a line AND are followed by a character
        s = re.sub('^[0-9]+ *([^ー△,0-9])'.decode('utf8'),'\\1',s)
        # XXX Untested
        s = re.sub('^[0-9]+ *([^,ー△0-9][^,ー△0-9])'.decode('utf8'),'\\1',s)
        #
        # Make reeeeeally big whitespace explicit break
        s = re.sub(' {3}',' [SPACE] ',s)
        #
        # Periods to commas.  Close space around commas.
        # Truncate multiple commas.
        s = re.sub('\.',',', s)
        s = re.sub(' *, *',',', s)
        s = re.sub(',,*',',', s)
        s = re.sub(',,*',',', s)
        #
        # Wipe out impossible negative signs
        s = re.sub('[ー△] *([^ 0-9]|$)'.decode('utf8'),'[MINUS]\\1',s)
        #
        # Cut numbers with 円 and 人
        s = re.sub('( *)([ ー△,0-9]+ *)(?:名|人|円)'.decode('utf8'),'\\1[NAMED]',s)
        #
        # Force single space before negative signs.
        s = re.sub(' *[ー△]'.decode('utf8'),' △'.decode('utf8'),s)
        #
        # Close space after negative sign.
        s = re.sub('[ー△] *([0-9])'.decode('utf8'),'△\\1'.decode('utf8'),s)
        #
        # Normalize negative sign to a hyphen.
        s = re.sub('[△ー]([0-9])'.decode('utf8'),'-\\1',s)
        #
        # Close leading zero for nonzero partner
        s = re.sub('([1-9]) (0[0-9])','\\1\\2',s)
        #
        # Close leading zero for multi-digit partner
        s = re.sub('([0-9][0-9]) (0[0-9])','\\1\\2',s)
        #
        # Force separate treatment of strings with more or less than three digits.
        s = re.sub('[.,]([0-9]{4,})',' \\1', s)
        s = re.sub('([0-9]{4,})[.,]','\\1 ', s)
        s = re.sub('[.,]([0-9]{1,2}(?:[^0-9]|$))',' \\1', s)
        s = re.sub('[.,]([0-9]{1,2}(?:[^0-9]|$))',' \\1', s)
        #
        # XXX needs test
        # Empty parens might be zeros
        s = re.sub('[（(][)）]'.decode('utf8'),'0', s)
        #
        # XXX needs test
        # No negative zeros!!
        s = re.sub('-0','0', s)
        #print s
        return s
    
    def split_string(self, s):
        items = re.findall('(?:%s|(?: *-*[,0-9]+)+)'.decode('utf8') % self.category_hinter.re, s)
        poppers = []
        #
        # XXX Untested
        self.category_hinter.line_reset()
        for pos in range(0,len(items),1):
            item = items[pos]
            if self.category_hinter.classify( item ):
                poppers.append(pos)
                continue
            info = {'category':self.category_hinter.current,'nontotal':self.category_hinter.nontotal,'line':self.line_number}
            item = item.replace(',','')
            items[pos] = ambiguousCluster( item, info )
        poppers.reverse()
        for pos in poppers:
            items.pop(pos)
        return items
