''' Module
'''
import re

def documentChop( category_hinter, data ):
    
    re_start = category_hinter.re_start
    re_end = category_hinter.re_end
    #data.reverse()
    #aggressive_delete = True
    #for pos in range(len(data)-1,-1,-1):
    #    if aggressive_delete:
    #        if re.match('.*%s.*' % re_start.decode('utf8'), data[pos]):
    #            aggressive_delete = False
    #        else:
    #            data.pop(pos)
    #data.reverse()
    aggressive_delete = False
    poppers = []
    for pos in range(0,len(data),1):
        if not aggressive_delete and re.match('.*%s.*' % re_end, data[pos]):
            aggressive_delete = True
            continue
        if aggressive_delete:
            poppers.append(pos)
    poppers.reverse()
    for popper in poppers:
        data.pop( popper )
    #for line in data:
    #    print line
    return data
