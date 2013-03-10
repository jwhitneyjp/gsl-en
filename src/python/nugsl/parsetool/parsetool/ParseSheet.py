#!/usr/bin/python
#-*- encoding: utf8 -*-

'''
  Extract team info from XLS file to handy CSV
'''

from pyExcelerator import *
import csv,re,sys

class parseSheet:
    def __init__(self, filename,
                     headingcol=-1,
                     controlexpr=None,
                     controlcol=-1,
                     variexpr=None,
                     varilabel=None,
                     varisub=None):
        self.headingcol=headingcol
        self.controlexpr=controlexpr
        self.controlcol=controlcol
        self.variexpr=variexpr
        self.varilabel=varilabel
        self.varisub=varisub
        if filename.endswith('.xls'):
            self.filestub = filename[:-4]
        else:
            self.filestub = filename
            filename += '.xls'
        
        if self.variexpr:
            self.variexpr = self.variexpr.decode('utf8')
        
        self.data = ImportXLS.parse_xls(filename)[0][1]
        self._csv_data = []
        self.set_key_rows()
        self.set_headings()
        for keyrow in self._key_rows:
            self.extract_data( keyrow )

    def dump_csv(self):
        ocsv = csv.writer( open( self.filestub + '.csv', 'w+') )
        for line in self._csv_data:
            ocsv.writerow( line )

    def extract_data(self, keyrow ):
        '''
          Currently ends processing if no data is contained
          in column 1.  Args of controlcol and controlexpr
          can be used to target a particular entry or set
          of entries in the possible set of rows.
        '''
        
        row = keyrow+1
        
        entry_pos = 0
        while 1:
            if not self.data.has_key( (row,0) ):
                break
            if not self.data[ (row,0) ]:
                break
            _row_data = []
            for heading in self._headings:
                key = (row,heading[1])
                if self.data.has_key(key):
                    _row_data.append( self.data[(row,heading[1])] )
                else:
                    _row_data.append( '' )
            pos = self.get_heading_index('entry_pos')
            _row_data.insert(pos, entry_pos )
            #
            # Add variable label back as data if required
            #
            if self.variexpr:
                pos = self.get_heading_index( self.varilabel )
                grouppos = self._key_rows.index( keyrow )
                _row_data.insert( pos, self.groupheadings[grouppos] )
            entry_pos += 1
            row += 1
            if self.controlcol > -1 and self.controlexpr:
                control = _row_data[ self._headings[self.controlcol][1] ]
                if not re.match(self.controlexpr, control):
                    continue
            self._csv_data.append( _row_data )

    def get_heading_index(self, search_term):
        for heading in self._headings:
            if heading[0] == search_term:
                pos = heading[1]
                break
        return pos

    def set_key_rows(self):        
        self._key_rows = []
        for key in self.data.keys():
            if self.headingcol > -1 and not self.headingcol == key[1]:
                continue
            if re.match( unicode( self.variexpr ), unicode(str( self.data[key] ) ) ):
                self._key_rows.append(key[0])
        self._key_rows.sort()

    def set_headings(self):
        self._headings = []
        for key in self.data.keys():
            #
            # Headings are derived from the _first_ key row
            #
            if key[0] == self._key_rows[0]:
                self._headings.append( (self.data[key],key[1]) )
        self._headings.append( ('entry_pos', len(self._headings)) )
        self._headings.sort( self.sort_headings )
        #
        # Adjust if one column varies by group
        #
        
        if self.variexpr:
            self.groupheadings = []
            for pos in range(len(self._headings)-1,-1,-1):
                heading = self._headings[pos]
                if re.match( self.variexpr, heading[0] ):
                    varicol = heading[1]
                    self._headings[pos] = (self.varisub, heading[1])
                    self._headings.append( (self.varilabel, len(self._headings) ) )
            for keyrow in self._key_rows:
                self.groupheadings.append( self.data[ (keyrow, varicol) ] )
        l = []
        for h in self._headings:
            l.append( h[0] )
        self._csv_data.append( l )
            
    def sort_headings(self,a,b):
        if a[1] > b[1]:
            return 1
        elif a[1] == b[1]:
            return 0
        else:
            return -1
            
