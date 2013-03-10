#!/usr/bin/python

import sys,csv

file = sys.argv[1]

ifh = open( file )
ofh = open( file + '.FINAL', 'w+' )
ofhnon = open( file + '.NONREPORTING', 'w+')
ofhstoplisted = open( file + '.STOPLISTED', 'w+' )

orig = csv.reader( ifh )
final = csv.writer( ofh )
nonreporting = csv.writer( ofhnon )
stoplisted = csv.writer( ofhstoplisted )

for line in orig:
    if line[25].strip() == '':
        nonreporting.writerow( line )
    elif line[25].strip() == '-1':
        stoplisted.writerow( line )
    else:
        final.writerow( line )
