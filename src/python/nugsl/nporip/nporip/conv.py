#!/usr/bin/python

import re

text = open('Prefectures.csv').read()

rex = re.compile(' *<[^>]*>',re.M|re.S)
rex2 = re.compile('\n\n',re.M|re.S)

text = re.sub(rex,'',text)
text = re.sub(rex2,'\n',text)

print text
