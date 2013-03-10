#!/usr/bin/python

import sys

ifh = open( sys.argv[1])

import csv
name = {}
csvreader = csv.reader( ifh )

for line in csvreader:
    if name.has_key( line[0] ):
        name[ line[0] ] += 1
    else:
        name[ line[0] ] = 1

for key in name.keys():
    if name[key] > 1:
        print 'Dupe: %s' % key

ifh.seek(0)
for line in csvreader:
    if not line[0]:
        print 'Empty'
    print line[25]