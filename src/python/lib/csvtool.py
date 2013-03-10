
import os,sys,csv
import _csv

class gslCsv:
    def __init__(self,f,offset=0):
        
        if type(f) == type(sys.stdin):
            self.fh = f
        else:
            self.fh = open(f)        
        
        self.csv_fh = csv.reader( self.fh )        

        while offset:
            self.csv_fh.next()
            offset += -1
        
        self.header_list = self.csv_fh.next()
        self.l2c = {}
        for pos in range(0,len(self.header_list),1):
            self.l2c[ self.header_list[pos] ] = pos
            
    def __iter__(self):
        return self
        
    def next(self):
        data = self.csv_fh.next()
        ret = {}
        for pos in range(0,len(self.header_list),1):
            ret[ self.header_list[pos] ] = data[pos]
        return ret
    