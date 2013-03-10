#!/usr/bin/python
#-*- encoding: utf8 -*-

''' Module
'''

import sys, re, os
from nugsl.tagtool import tagfix

class Base:

    def __init__(self, html, filename, info={}, **kw ):
        self.filename = filename
        self.info = info
        self.tablecount = 0
        html = self.pre_html( html )
        html = tagfix('table', html, info=self.info, matchfunc=self.process_tables)
        html = self.post_html( html )
        self.html = html

    def pre_html(self, html):
        return html
    
    def post_html(self, html):
        return html
        
    def process_tables(self, table, info=None):
        self.rowcount = 0
        table = self.pre_table( table )
        table = tagfix('tr', table, info=info, matchfunc=self.process_rows)
        table = self.post_table( table )
        self.tablecount += 1
        return table
    
    def pre_table(self, table):
        return table
    
    def post_table(self, table):
        return table
        
    def process_rows(self, row, info=None):
        self.cellcount = 0
        row = self.pre_row( row )
        row = tagfix('td', row, info=info, matchfunc=self.process_cells)
        row = self.post_row( row )
        self.rowcount += 1
        return row

    def pre_row(self, row):
        return row
    
    def post_row(self, row):
        return row

    def process_cells(self, cell, info=None):
        cell = self.do_cell( cell )
        self.cellcount += 1
        return cell
    
    def do_cell(self, cell):
        return cell

    def strip_cell(self, cell):
        cell_stripped = re.sub('<[^>]*>',' ', cell)
        cell_stripped = re.sub('\n',' ', cell_stripped)
        cell_stripped = re.sub('  *',' ', cell_stripped).strip()
        cell_stripped = re.sub('  *',' ', cell_stripped)
        return cell_stripped

class Splice(Base):

    def pre_html(self, html):
        self.RE_SPLICE = '(?i)(?m)(?s)</table>.*?{SPLICE}'
        self.last_table_row_length = 0
        return html
        
    def post_html(self, html):
        r = re.match('.*(%s).*' % self.RE_SPLICE, html)
        if r:
            html_list = re.split( self.RE_SPLICE, html)
            html = ''.join( html_list )
        html = re.sub('{SPLICE}','',html)
        return html

    def post_table(self, table):
        self.last_table_row_length = self.row_length
        return table
    
    def pre_row(self, row):
        self.row_length = row.lower().count('<td[> ]')
        self.splice_request = False
        return row

    def post_row(self, row):
        self.last_row_length = self.row_length
        if self.last_table_row_length == self.row_length \
           and self.splice_request:
               row = '{SPLICE}' + row
        return row
               
    def do_cell(self, cell):
        cell_stripped = self.strip_cell( cell )
        if self.rowcount == 0\
           and self.cellcount == 0 \
           and cell_stripped \
           and cell_stripped != 'MPV' and cell_stripped != 'M.P.':
               self.splice_request = True
        if self.cellcount == 0:
            if cell_stripped:
                self.has_first_field = True
            else:
                self.has_first_field = False
        if self.has_first_field \
           and self.cellcount == self.row_length - 1 \
           and not cell_stripped \
           and self.row_length != self.last_row_length:
            self.row_length -= 1
            cell = ''
        return cell

class Merge(Base):

    def pre_html(self, html):
        self.RE_MERGE = '(?i)(?m)(?s)</td>{MERGE}[ \n]*<td [^>]*>'
        return html
    
    def post_html(self, html):
        r = re.match('.*(%s).*' % self.RE_MERGE, html)
        if r:
            html_list = re.split( self.RE_MERGE, html)
            html = ''.join( html_list )
        html = re.sub('{MERGE}','',html)
        return html
        
    def pre_table(self, table):
        self.mergeables = []
        return table

    def pre_row(self, row):
        self.row_length = row.lower().count('<td[> ]')
        return row
    
    def do_cell(self, cell):
        if self.rowcount == 0:
            self.headers_length = self.row_length
            r = re.match('(?i)(?s)(?m)<td [^>]*colspan="([1-9])"[^>]*>.*',cell)
            if r:
                #print 'Appending to mergeables'
                self.mergeables.append( self.cellcount )
        else:
            if self.cellcount in self.mergeables:
                #print 'cellcount is in mergeables'
                #print self.row_length
                #print self.headers_length
                if self.row_length == self.headers_length + 1:
                    #print 'marking as mergeable'
                    cell = cell + "{MERGE}"
            elif self.cellcount == self.headers_length and not self.strip_cell( cell ):
                cell = ''
        return cell

class FixHeadings(Base):

    def pre_table(self, table):
        self.empty_headings = []
        self.insert_heading = ''
        return table
    
    def pre_row(self, row):
        self.delete_row_request = False
        return row

    def post_row(self, row):
        if self.rowcount == 0:
            row = self.insert_heading + row
        if self.delete_row_request:
            row = ''
        return row
    
    def do_cell(self, cell):
        cell_stripped = self.strip_cell( cell )
        if self.rowcount == 0:
            short_filename = os.path.split( self.filename )[-1]
            patch_key = short_filename + ':%d' % self.tablecount
            if cell_stripped \
               and self.cellcount == 0 \
               and cell_stripped != 'M.P.' and cell_stripped != 'MPV':
                   if info['PATCH'].has_key( patch_key ):
                       self.insert_heading = '<tr><td>%s</td></tr>' % '</td><td>'.join( info['PATCH'][ patch_key ])
            if not cell_stripped:
                if info['PATCH'].has_key( patch_key ):
                    cell_stripped = info['PATCH'][ patch_key ][self.cellcount]
                    cell = '<td>%s</td>' % cell_stripped
            if not cell_stripped:
                self.empty_headings.append( self.cellcount )
        else: 
            if self.cellcount == 0 \
               and ( cell_stripped == 'M.P.' or cell_stripped == 'MPV' ):
                   self.delete_row_request = True
            if self.cellcount in self.empty_headings and cell_stripped:
                print '\nContent under empty heading?'
                print '%s in col %d' % (self.filename, self.cellcount)
                print cell
                sys.exit()
        return cell

class ValidateHeadings(Base):
    
    def pre_row(self, row):
        if self.rowcount == 0:
            self.row_length = row.lower().count('<td[> ]')
        elif  row.lower().count('<td[ >]') != self.row_length:
            print 'Unexpected variation in row length'
            print self.filename
            print self.tablecount
            print self.rowcount
            print row
            sys.exit()
        return row

    def do_cell(self, cell):
        cell_stripped = self.strip_cell( cell )
        if self.rowcount == 0 and self.cellcount == 0:
            cell_stripped = self.strip_cell( cell )
            if cell_stripped != 'M.P.' and cell_stripped != 'MPV':
                print '\nMissing or bad header'
                print self.filename
                print cell
                sys.exit()
        if self.rowcount > 0 and self.cellcount == 0 \
           and ( cell_stripped == 'M.P.' or cell_stripped == 'MPV' ):
               self.delete_row_request = True
        return cell

class AnalyzeStuff(Base):

    def pre_table(self, table):
        self.info['local_headings'] = []
        return table
    
    def post_table(self, table):
        headings = self.info['local_headings'][:]
        heading_type = 'preamendment'
        for heading in headings:
            if 'URGÊNCIA'.decode('utf8').lower() in heading.decode('utf8').lower():
                heading_type = 'postamendment'
                break
        for heading in headings:
            if not heading in self.info[ heading_type ]:
                self.info[ heading_type].append( heading )
                
        return table
    
    def do_cell(self, cell):
        if self.rowcount == 0:
            self.info['local_headings'].append( self.strip_cell( cell ) )
        else:
            if self.cellcount == 0:
                cell_stripped = self.strip_cell( cell )
                if not cell_stripped in self.info['keys']:
                    self.info['keys'].append( cell_stripped )
        return cell
            
