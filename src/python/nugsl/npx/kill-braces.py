#!/usr/bin/python
#-*- encoding: utf8 -*-

import os,sys,re

files = os.listdir('.')

for pos in range(len(files)-1,-1,-1):
    if not files[pos].endswith('.box'):
        files.pop(pos)

bad1 = '」'.decode('utf8')
bad2 = '』'.decode('utf8')

for file in files:
    print file
    ifh = open(file)
    ofh = open(file+'NEW','w+')
    while 1:
        line = ifh.readline()
        if not line: break
        line = line.decode('utf8')
        if line.startswith(bad1):
            line = ',' + line[1:]
        if line.startswith(bad2):
            line = ',' + line[1:]
        ofh.write(line)
    ofh.close()
    ifh.close()
    os.unlink(file)
    os.rename(file+'NEW',file)
    