'''
    One sheet, multiple groups delimited by a
    header row at the top of each group.  One
    header is moved into row content, with a view
    to discriminating between groups in CSV export
    data.
'''

import re
from nugsl.parsetool.ParseSheet import parseSheet

class parseOneSheetGroups (parseSheet):
    def __init__(self, filename,
                     headingcol=-1,
                     controlexpr=None,
                     controlcol=-1,
                     varisub=None,
                     variexpr=None,
                     varilabel=None):
        
        parseSheet.__init__(self, filename,
                     headingcol=headingcol,
                     controlexpr=controlexpr,
                     controlcol=controlcol,
                     varisub=varisub,
                     variexpr=variexpr,
                     varilabel=varilabel)

    def count_groups(self):
        team = '_'
        groupcount = 0
        for d in self._csv_data[1:]:
            if d[0] != team:
                team = d[0]
                groupcount += 1
        return groupcount
        
    def get_maps(self,copies=None,perpage=10):
        groupcount = -1
        team = '_'
        template = 'e%dc%d'
        template2 = 'e%dprimary-name'
        entrycount = 1
        ret = []
        m = {}
        for line in self._csv_data[1:]:
            if team != line[0]:
                team = line[0]
                groupcount += 1
            copynumber = copies[groupcount]
            for x in range(0,copynumber,1):
                columncount = 1
                for columndata in line:
                    m[template % (entrycount,columncount)] = columndata
                    columncount += 1
                if m[template % (entrycount, 3)]:
                    m[template2 % entrycount] = m[template % (entrycount, 3)]
                else:
                    m[template2 % entrycount] = m[template % (entrycount, 4)]
                if divmod(entrycount, perpage)[1] == 0:
                    ret.append(m)
                    m = {}
                    entrycount = 1
                    continue
                entrycount += 1
        ret.append(m)
        return ret
        
