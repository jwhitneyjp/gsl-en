#!/usr/bin/python
#-*- encoding: utf-8 -*-

'''
  Offers a csv-like interface to XLS files
'''

from pyExcelerator import *
import csv,re
from markdown import markdown

def sortkeys(a,b):
    if a[0] > b[0]:
        return 1
    elif a[0] == b[0]:
        if a[1] > b[1]:
            return 1
        elif a[1] == b[1]:
            return 0
        else:
            return -1
    else:
        return -1

class Error:
    pass
    
class _WrappedEntrysheet:
    '''
      Wrapper for entry sheets used to query staff
    '''
    def __init__(self,sheetdata):
        data = sheetdata
        self.maxrow = 0
        self.update = {}
        for x in data[1].keys():
            end = len(x)-1
            if self.maxrow < x[end-1]:
                self.maxrow = x[end-1]
            # yend
        row = 1
        for pos in range(0,self.maxrow+1,1):
            if data[1].has_key((row,1)):
                keyname = data[1][(row,0)]
                if data[0].has_key((row,1)):
                    if type(data[0][(row,1)]) == type(0):
                        self.update[keyname] = str(data[0][(row,1)])
                    else:
                        self.update[keyname] = data[0][(row,1)]
                else:
                    self.update[keyname] = ''
            row = row + 1

    def get_update(self):
        return self.update

class _WrappedWorksheet:
    '''
      Wrapper for the worksheet data structure
    '''
    def __init__(self,sheetdata,keyrow=1):
        self.data = sheetdata
        self.keyrow = keyrow
        self.row = keyrow
        self.maxcol = 0
        self.maxrow = 0
        self.labels = {}
        self.skip_rows = []
        for x in self.data.keys():
            end = len(x)-1
            if self.maxcol < x[end]:
                self.maxcol = x[end]
            if self.maxrow < x[end-1]:
                self.maxrow = x[end-1]
        self.keymap = {}
        self.keylist = []
        
        spoofcount = 0
        for col in range(0,self.maxcol+1,1):
            key = (self.row,col)
            if self.data.has_key(key):
                keyname = self.data[key]
            else:
                keyname = 'col%0.2d' %spoofcount
            
            if self.keyrow > 0:
                try:
                    self.labels[keyname] = self.data[(self.row-1,col)]
                except:
                    self.labels[keyname] = 'Column %d' % (spoofcount+1,)
            else:
                self.labels[keyname] = keyname
            self.keymap[keyname] = col
            self.keylist.append(keyname)
            spoofcount = spoofcount+1
        self.row = self.row + 1

    def reset (self):
        self.row = self.keyrow + 1
        
    def skip (self):
        self.skip_rows.append(self.row-1)
        
    def nextmap(self):
        while self.row in self.skip_rows:
            self.row = self.row + 1
            
        if self.row > self.maxrow:
            raise Error
        ret = {}
        for col in range(0,self.maxcol+1,1):
            if self.data.has_key((self.row,col)):
                key = self.keylist[col]
                ret[key] = self.data[(self.row,col)]
            else:
                key = self.keylist[col]
                ret[key] = ''
        self.row = self.row + 1
        return ret

    def extract_keys_and_labels(self):
        ret = []
        for key in self.keylist:
            ret.append((key,self.labels[key]))
        return ret
    
            
class WrappedWorkbook:
    '''
      Wrapper for the data set that ImportXLS extracts from the
      file.
    '''
    
    def __init__ (self,filename):
        self.xrex10 = re.compile(r'\n([^\n#*|])')
        if filename.lower().endswith('.xls'):
            self.data = ImportXLS.parse_xls(filename)
        else:
            self.data = self.load_csv(filename)

    def dump(self):
        return self.data
    
    def sheet_names(self):
        data = self.data
        ret = []
        for d in data:
            ret.append(d[0])
        return ret
    
    
    def get_sheet(self,sheetname=None,keyrow=1):
        data = self.data
        ret = None
        if not sheetname:
            ret = data[0][1]
        else:
            for d in data:
                if d[0] == sheetname:
                    ret = d[1]
                    break
            if not ret:
                print 'Sheet name %s not found.' %sheetname
                sys.exit()
        if keyrow == None:
            return ret
        else:
            return _WrappedWorksheet(ret,keyrow=keyrow)

    def get_entrysheet(self):
        data = self.data
        ret = (data[0][1],data[1][1])
        return _WrappedEntrysheet(ret)

    def load_csv(self,filename):
        self.data = []
        sheetname = '0'
        celldata = {}
        
        fh = open(filename,'r')
        c = csv.reader(fh)
        lineno = 0
        while 1:
            try:
                linedata = c.next()
            except:
                break
            for pos in range(0,len(linedata),1):
                if linedata[pos].strip():
                    celldata[(lineno,pos)] = linedata[pos]
            lineno = lineno + 1
        self.data.append((sheetname,celldata))

    def fix(self,t,plaintext,fieldname,bigfix=None):
        t = t.replace(unichr(8216),'\'')
        t = t.replace(unichr(8217),'\'')
        t = t.replace(unichr(8220),'\"')
        t = t.replace(unichr(8221),'\"')
        t = t.replace(unichr(8211),'-')
        #t = t.replace(unichr(252),'&#252;')
        t = t.replace(unichr(65374),unichr(12316))
        t = t.replace(unichr(65293),unichr(12540))
        if bigfix:
            t = t.replace('（仮）'.decode('utf8'),u'')
            t = t.replace(unichr(12288),u'')
        t = re.sub(self.xrex10,'\n\n\\1',t)
        if not fieldname in plaintext:
            #t = markdown(t,encoding='utf8')
            t = re.sub("\n[ %s%s]*" % (unichr(12288),unichr(9)),"\n\n",t)
            t = markdown(t)
            t = t.decode('utf8')
        t = t.replace('&#8212;',' -- ')
        if t.count('<p>') == 1:
            t = t.strip()[3:-4]
        return t.strip()
        
    def dump_csv(self,fileroot,bigfix=False,rowoffset=0,sheetoffset=0,sheets=1,plaintext=[],req_col=None):
        #
        # Set filename and open file handle with CSV writer
        #
        if fileroot.endswith('.csv'):
            filename = fileroot
        else:
            filename = fileroot + '.csv'
        #
        # Select a range of sheets if requested (we write
        # a single flat sheet.
        #
        if sheetoffset < 0:
            start = len(self.data) + sheetoffset
        else:
            start = sheetoffset
        data = self.data[start:start+sheets]
        sheetno = 0
        #
        # Get max dimension of all sheets
        #
        self.maxcol = 0
        self.maxrow = []
        for pos in range(0,len(data),1):
            sheet = data[pos]
            maxrow = 0
            for x in sheet[1].keys():
                end = len(x)-1
                if self.maxcol < x[end]:
                    self.maxcol = x[end]
                if maxrow < x[end-1]:
                    maxrow = x[end-1]
            self.maxrow.append(maxrow)
        #
        # Get common field names and column positions
        #
        
        fieldnames = {}
        sheetcount = 0
        for sheet in data:
            for col in range(0,self.maxcol+1,1):
                r = rowoffset 
                fieldname_raw = None
                while not fieldname_raw and r > -1:
                    if sheet[1].has_key((r,col)):
                        fieldname_raw = sheet[1][(r,col)]
                    r += -1
                    
                if fieldname_raw:
                    fieldname = re.sub(u'[（(].*[)）]',u'',fieldname_raw)
                    fieldname = re.sub(u'[※　]',u'',fieldname)
                    fielname = re.sub(unichr(12288),u'',fieldname)
                    fieldname = fieldname.strip()
                    if fieldnames.has_key(fieldname):
                        for x in range(0,sheetcount-len(fieldnames[fieldname]),1):
                            print fieldname
                            print ' added old'
                            fieldnames[fieldname].append(-1)
                        if len(fieldnames[fieldname]) < sheetcount+1:
                            fieldnames[fieldname].append(col)
                    else:
                        fieldnames[fieldname] = []
                        for x in range(0,sheetcount,1):
                            print fieldname
                            print ' added new'
                            fieldnames[fieldname].append(-1)
                        if len(fieldnames[fieldname]) < sheetcount+1:
                            fieldnames[fieldname].append(col)
            sheetcount += 1
                        
        # Fill out partially completed key records
        for key in fieldnames.keys():
            if len(fieldnames[key]) != sheets:
                for x in range(0,sheets-len(fieldnames[key]),1):
                    print key
                    print ' added extra'
                    fieldnames[key].append(-1)
        for key in fieldnames.keys():
            if len(fieldnames[key]) != sheets:
                print len(fieldnames[key])
                print sheets
                print 'Oops'
                sys.exit()
        #        fieldnames.pop(key)
        #
        
        # Convert fieldname array to list
        #
        # (Get a fixed order of items)
        knames = fieldnames.keys()
        fieldlists = []
        for pos in range(0,sheets,1):
            fieldlist = []
            for key in knames:
                fieldlist.append((key, fieldnames[key][pos]))
            fieldlists.append(fieldlist)
        #
        # Write csv file
        #
        ofh = open(filename,'w')
        c = csv.writer(ofh)

        #
        # Field names
        l = []
        for field in fieldlists[0]:
            l.append(field[0])
        l.append('sheetno')
        l.append('sheetname')
        c.writerow(l)
        
        #
        # Data
        for sheetno in range(0,len(fieldlists),1):
            fieldlist = fieldlists[sheetno]
            sheetname = data[sheetno][0]
            for row in range(rowoffset+1,self.maxrow[sheetno]+1,1):
                l = []
                for pos2 in range(0,len(fieldlist),1):
                    col = fieldlist[pos2][1]
                    if data[sheetno][1].has_key((row,col)):
                        d = data[sheetno][1][(row,col)]
                        if type(d) == type(u'') or type(d) == type(''):
                            d = self.fix(d,plaintext,fieldlist[pos2][0])
                        l.append( d )
                    else:
                        l.append('')
                if req_col:
                    pos = [x[0] for x in fieldlist].index(req_col)
                    if not l[pos] or req_col == l[pos].strip():
                        continue
                l.append(sheetno)
                l.append(sheetname)
                c.writerow(l)
            
        ofh.close()
