#!/usr/bin/python
'''
Several cleanup and validation operations:
    Find double-return broken markdown ref_ids
    Delete ~ backup files
'''

from os.path import walk
import re,os

rex = re.compile(r'.*\[[^]]*\n\n[^]]*\].*',re.M|re.S)


def validatemarkdown(arg,dirname,fnames):
    for filename in fnames:
        path = dirname + '/' + filename

        if path.endswith('~'):
            os.unlink(path)
            continue
        
        if not path.endswith('.txt'):
            continue
        
        try:
            text = open(path).read()
        except:
            continue
        
        r = rex.match(text)
        if r:
            print path
        
walk('.',validatemarkdown,None)
