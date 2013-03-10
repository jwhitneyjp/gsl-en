#!/usr/bin/python

import os,sys,csv,re

files = os.listdir('.')

for pos in range(len(files)-1,-1,-1):
    file = files[pos]
    if not file.endswith('.csv') or not re.match('^[0-9]{2}-',file):
        files.pop(pos)

for file in files:
    print file
    base = os.path.splitext(file)[0]
    ifhselections = open( file )
    creader = csv.reader( ifhselections )
    data = {}
    for line in creader:
        if line[0] == 'name':
            continue
        key = np.sanitize( line[0] )
        data[ key ] = []
        for i in range(8,25,1):
            data[ key ].append( line[i] )
    ifhselections.close()
    
    ofh = open(file + '.NEW','w+')
    ifhdata = open('final/%s' % file)
    creader = csv.reader( ifhdata )
    cwriter = csv.writer( ofh )
    count = 0
    for line in creader:
        key = np.sanitize( line[0] )
        if data.has_key( key ):
            for i in range(8,25,1):
                line[i] = data[ key ][i-8]
            cwriter.writerow( line )
        else:
            print "Dropping entry for %s" % key
    ifhdata.close()
    ofh.close()
        
print 'Done!'