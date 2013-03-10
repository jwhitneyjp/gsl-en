#!/usr/bin/python
#-*- encoding: utf8 -*-

import os,sys,re

files = os.listdir('.')

for pos in range(len(files)-1,-1,-1):
    if not files[pos].endswith('.box'):
        files.pop(pos)

for file in files:
    print file
    content = open(file).read().decode('utf8')
    content = content.replace('０','0')
    content = content.replace('１','1')
    content = content.replace('２','2')
    content = content.replace('３','3')
    content = content.replace('４','4')
    content = content.replace('５','5')
    content = content.replace('６','6')
    content = content.replace('７','7')
    content = content.replace('８','8')
    content = content.replace('９','9')
    open(file,'w+').write(content)


    