#!/usr/bin/python

''' Primitive converter for a few plain text markup languages.
'''


text = open('/home/bennett/Desktop/lrmjapan/lrmjapan.txt').read()

delims = '-~+^|:'

import re,sys

for pos in range(0,len(delims),1):
    delim = delims[pos]
    if delim == '^':
        delim = '\^'
    multiplier = pos + 1
    regexp = r'\n(.*)\n['+delim+']+\n'
    text = re.sub(regexp,'\n'+ '#'*multiplier+' \\1\n',text)

print text
