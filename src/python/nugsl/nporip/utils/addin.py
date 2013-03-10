#!/usr/bin/python
#-*- encoding: utf8 -*-

from nugsl.nporip import npoRip

np = npoRip()

ifhorig = open('kyoto.csv.ORIG')
ifhadd = open('kyoto.csv.ADD')

ofhnew = open('kyoto.csv.NEW','w+')

import csv, sys

csvorig = csv.reader( ifhorig )
csvadd = csv.reader( ifhadd )

csvnew = csv.writer( ofhnew )

addmap = {}

ofhaddnames = open('addin.ADDKEYS','w+')
for item in csvadd:
    mykey = np.sanitize( item[0] )
    ofhaddnames.write( mykey + '\n')
    addmap[ mykey ] = item[1]

first = True
ofhorignames = open('addin.ORIGKEYS','w+')
for line in csvorig:
    if first:
        first = False
        continue
    name = np.sanitize( line[0] )
    ofhorignames.write( name + '\n')
    if addmap.has_key( name ):
        line.append( addmap[ name ] )
        addmap.pop( name )
        csvnew.writerow( line )
        sys.stdout.write('+')
        sys.stdout.flush()
    else:
        #print 'key: %s' % name
        #print 'orig: %s' % line[0]
        #print ''
        line.append( '' )
        csvnew.writerow( line )
        sys.stdout.write('.')
        sys.stdout.flush()

print 'Logging leftovers'
        

ofhlog = open('addin.LEFTOVERS','w+')
for item in addmap.keys():
    ofhlog.write( item + '\n' )
print len(addmap.keys() )
