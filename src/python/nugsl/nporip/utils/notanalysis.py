#!/usr/bin/python

import os,sys,csv,re
from cStringIO import StringIO
from datetime import date

# Get dataset names
datasets = os.listdir('final')
for pos in range(len(datasets)-1,-1,-1):
    dataset = datasets[pos].decode('utf8')
    if u'-non' in dataset:
        datasets.pop(pos)
    if u'-stop' in dataset:
        datasets.pop(pos)
datasets.sort()
# Get headings for reference
ifh = open('final/' + datasets[0])
csvreader = csv.reader( ifh )
headings = csvreader.next()
ifh.close()


# Function to get number of dataset
def dataid( s ):
    return s[:2]
        
# Function to get readers
def get_readers():
    readers = []
    for dataset in datasets:
        fh = 'ifh' + dataid( dataset )
        exec fh + " = open('final/" + dataset + "')"
        fhcsv = 'ifhcsv' + dataid( dataset )
        exec "%s = csv.reader( %s )" % (fhcsv, fh)
        exec "readers.append( ('%s',%s,%s) )" % (dataset,fh,fhcsv)
    return readers

# Function to close readers
def close_readers():
    for reader in readers:
        reader[1].close()

# Function to store line content as an array
def get_line( line ):
    ret = {}
    for pos in range(0,len(line),1):
        if pos < len(headings):
            ret[ headings[pos] ] = line[pos]
    return ret

# Dummy function for testing
def nonsense( line ):
    sys.stdout.write('.')
    sys.stdout.flush()
    return 1

def spout( status ):
    total = 0
    for s in status:
        total = total + s
    return "Total is: %d" % total

    
# Function to apply a function to each line in each dataset,
# and use a function to generate output from the result
def process( reporter, fun ):
    global io,readers
    io = StringIO()
    readers = get_readers()
    status = []
    for reader in readers:
        print "Processing %s" % reader[0]
        localstatus = []
        for line in reader[2]:
            if line[0] == 'name':
                continue
            localstatus.append ( fun( line ) )
        reporter( reader[0], localstatus )
        status.extend( localstatus )
    print ''
    reporter( 'Aggregate', status )
    close_readers()
    io.seek(0)
    report = io.read()
    return report

#print process( spout, nonsense )
#sys.exit()

# Answer questions!

question1 = '''
???
'''

print question1

def marshal( line ):
    ret = []
    data = get_line( line )
    ticks = []
    spec = []
    for fieldnum in range(1,18,1):
        if data[ str(fieldnum) ] == 'TRUE':
            ticks.append( 1 )
        else:
            ticks.append( 0 )
    spec.append( ticks )
    try:
        day,month,year = [int(x) for x in data['founding'].split('/')]
    except:
        year,month,day = [int(x) for x in data['founding'].split('-')]
    if year == 99:
        year = 1999
    elif year < 99:
        year = year + 2000
    if day == 0:
        day = 1
    if month == 0:
        month = 1
    year = date(year,month,day).strftime('%Y')
    spec.append( year )
    ret.append( spec )
    ret.append( int(0) )
    return  ret

def report( title, status ):
    global io
    allticks = 0
    allotherticks = 0
    mytots = []
    dilution = []
    entrycount = 0
    lines = 0
    incometotal = 0
    allticked=0
    for fieldnum in range(0,17,1):
        mytots.append(0)
        dilution.append( float(0) )
    for entry in status:
        line = entry[0][0]
        entrycount += 1
        for pos in range(0,17,1):
            if line[pos]:
                allticks += 1
                mytots[pos] += 1
                dilution[pos] += sum( line )
            
                
        lines += 1
    io.write('\n====\n')
    io.write('%s:\n' % (title,) )
    io.write('====\n')
    
    for  pos in range(0,17,1):
        if not mytots[pos]:
            print 'Ignore %d' % (pos+1,)
            partnertot = 0
        else:
            partnertot = float(mytots[pos])/float(dilution[pos])
        io.write('%0.3F\n' % partnertot)
    io.write('Tick average: %0.3F\n' % (float(allticks)/float(entrycount),))
    io.write('Total entries: %d\n' %entrycount)
    io.write('Total ticks: %d\n' %allticks)

print process( report, marshal )
