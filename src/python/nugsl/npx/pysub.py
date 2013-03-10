#!/usr/bin/python

import sys,re

glyphs = open('samp.glyphs').read().decode('utf8').strip().split('\n')

lines = open( sys.argv[1] + '.box' ).read().decode('utf8').strip().split('\n')

if len(lines) != len(glyphs):
    print 'Error in %s, chars not equal in number, aborting' % sys.argv[1]

for pos in range(len(lines)-1,-1,-1):
    line = lines[pos]
    r = re.match( '^.*?( .*)', line )
    lines[pos] = glyphs[pos] + r.group(1)

open( sys.argv[1] + '.box', 'w+').write( '\n'.join( lines ) + '\n' )
