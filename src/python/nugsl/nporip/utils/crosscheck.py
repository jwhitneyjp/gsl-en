#!/usr/bin/python
#-*- encoding: utf8 -*-

import sys,csv,os
from signal import SIGTERM
import re
from nugsl.nporip import npoRip

np = npoRip()

path = '/home/bennett/Desktop/Web/src/python/nugsl/nporip/financials/pdf/%s/'
path = path % sys.argv[1]

ifh = open( sys.argv[1] + '.csv')
ofh = open( sys.argv[1] + '-cleaned.csv','w+')
csvreader = csv.reader(ifh)
csvwriter = csv.writer(ofh)


killme = False
count = 0
for line in csvreader:
    okay = True
    count += 1
    if killme or (len(line) > 26 and line[26] == 'done'):
        csvwriter.writerow( line )
        continue
    org = line[0]
    try:
        org = org.decode('utf8')
    except:
        print 'Ooops'
        org = org[:-6]+'.pdf'
        org = org.decode('utf8')
    org = np.sanitize( org )
    
    try:
        idx = os.spawnv(os.P_NOWAIT, '/usr/bin/xpdf', ('/usr/bin/xpdf', '%s%s.pdf' % (path,org)))
    except:
        print "File not found! %s" % org
        okay = False
    print ''
    current = list( line[25] )
    current.reverse()
    current = ''.join(current)
    current = re.sub('([0-9]{3})','\\1,',current)
    current = list( current )
    current.reverse()
    current = ''.join( current ).strip(',')
    print 'Current value: %s' % current
    print '  Q) to quit, 0-9+ to modify, any other key to continue ...' 
    print '(line %d)' % count
    if okay:
        print 'okay'
    else:
        print 'not okay'
    hello = raw_input().strip()
    if hello.lower() == 'q':
        killme = True
    elif re.match('^[-0-9]+$',hello):
        line[25] = hello
    else:
        pass
    if not killme:
        if okay:
            if len(line) > 26:
                line[26] = 'done'
            else:
                line.append('done')
    csvwriter.writerow( line )
    os.kill( idx, SIGTERM )

os.rename( sys.argv[1] + '-cleaned.csv',sys.argv[1] + '.csv')