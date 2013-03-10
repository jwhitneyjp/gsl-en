#!/usr/bin/python

import os,sys,csv

files = os.listdir('alldata')

grandtotalticks = 0
grandtotalentries = 0

ticknumbers = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
totalticknumbers = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

for file in files:
    print file[3:-4]
    ifh = open('alldata/' + file )
    creader = csv.reader( ifh )
    headers = creader.next()
    ifh.seek(0)
    start = headers.index('1')
    end = headers.index('17')

    totalticks = 0
    totalentries = 0
    
    first = True
    for line in creader:
        if first: 
            first = False
            continue
        line = line[start:end+1]
        ticks = []
    
        for pos in range(0,len(line),1):
            item = line[pos]
            if item == 'TRUE':
                ticks.append(1)
                totalticks += 1
            else:
                ticks.append(0)

        for pos in range(0,len(line),1):
            if ticks[pos]:
                ticknumbers[pos] += 1
            totalticknumbers[pos] += sum( ticks )
        
        totalentries += 1
    print '  avg: %0.2F' % (float(totalticks)/totalentries,)
    grandtotalticks += totalticks
    grandtotalentries += totalentries
    ifh.close()

print 'Grand total'
print '  avg: %0.2F' % (float(grandtotalticks)/grandtotalentries,)

print grandtotalentries

for pos in range(0,17,1):
    number = ticknumbers[pos]
    total = totalticknumbers[pos]
    percent = float(number)/total
    print '%0.4F' % percent
