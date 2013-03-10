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
How many NPOs are registered in aggregate in each of the categories?

  Nationwide
  Under each licensing authority

How many NPOs register in a single category only (excepting category 17)?

  For each category in all data
  For each category at licensing authority level

What is the average number of categories for which an NPO registers?

  Nationwide
  Under each licensing authority

What is the distribution of "income" among NPOs per category?

  Under each licensing authority
  Nationwide

Fields:
  Category number
  Total applicants ticking this category
  Percent of applicants ticking this category
  Total applicants ticking this category and only one other
  Percent of applicants ticking this category and only one other
  Degree of dilution by multiple purposes (1.00 = no dilution)
  Percentage of "income" attributable to this category.
  Average "income" of applicants ticking this category
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
    day,month,year = [int(x) for x in data['founding'].split('/')]
    if year == 99:
        year = 1999
    else:
        year = year + 2000
    year = date(year,month,day).strftime('%Y')
    spec.append( year )
    ret.append( spec )
    ret.append( int(data['income']) )
    return  ret

def formatmoney( figure ):
    inc = list( str( int( figure ) ) )
    inc.reverse()
    inc = ''.join( inc )
    inc = re.sub('([0-9]{3})','\\1,',inc)
    inc = inc.strip(',')
    inc = list(inc)
    inc.reverse()
    inc = ''.join( inc )
    return inc

def report( title, status ):
    global io
    tots = []
    mytots = []
    solos = []
    binaries = []
    dilution = []
    incomes = []
    weightedincomes = []
    lines = 0
    incometotal = 0
    allticked=0
    for fieldnum in range(0,17,1):
        mytots.append(0)
        tots.append(0)
        solos.append(0)
        binaries.append(0)
        dilution.append( float(0) )
        incomes.append(0)
        weightedincomes.append(0)
    for entry in status:
        line = entry[0][0]
        income = entry[1]
        for pos in range(0,17,1):
            tots[pos] += line[pos]
            if line[pos] and sum( line ) == 1:
                solos[pos] += 1
            if line[pos] and sum( line ) == 2:
                binaries[pos] += 1
            if line[pos]:
                mytots[pos] += 1
                dilution[pos] += sum( line )
            if income and line[pos]:
                weightedincomes[pos] += int( income )/sum( line )
                incomes[pos] += int( income )
        if income:
            incometotal += int( income )
        if sum(line) == 17:
            allticked += 1
            
        lines += 1
    io.write('\n====\n')
    io.write('%s (%d orgs, %d mytots, %0.3F tick avg):\n' % (title, lines, sum(mytots), float(sum(mytots))/float(lines)))
    io.write('====\n')
    
    for  pos in range(0,17,1):
        incpercent = float(incomes[pos]*100)/sum(incomes)
        averagesize = (incpercent/100)*incometotal/tots[pos]
        if tots[pos] > 0:
            partnertot = tots[pos]/dilution[pos]
            solotot = float(solos[pos] + binaries[pos])*100/tots[pos]
        else:
            partnertot = 0
            solotot =0
        # Line item
        io.write('  %4d %4d %7.2F%% %4d %7.2F%% %7.2F %7.2F  %10s\n' \
          % (pos+1,tots[pos], \
             float(tots[pos]*100)/lines, \
             solos[pos] + binaries[pos], \
             solotot, \
             partnertot, \
             incpercent, \
             formatmoney( incomes[pos]/tots[pos] )))
    for  pos in range(0,17,1):
        partnertot = float(dilution[pos])/mytots[pos]
        io.write('%0.3F)\n' % (partnertot,))
    io.write( 'Total "income": %s\n' % formatmoney( incometotal )  )
    io.write( 'All categories ticked in: %d entries\n' % allticked )
    io.write( 'Average size: %s\n' % formatmoney( incometotal/lines ) )

print process( report, marshal )

question2 = '''
What is the distribution of NPOs across "income" bands?

  By licensing authority
  By incorporation year
  By number of boxes ticked
'''

def medians( vals, chunks=4 ):
    vals = [int(x) for x in vals]
    vals.sort()
    chunk = len(vals)/chunks
    wchunk = sum( vals )/chunks
    #
    simple = [0]
    for i in range(1,chunks,1):
        simple.append( vals[chunk*i] )
    simple.append( vals[-1]+1 )
    #
    tot = 0
    weighted = [0]
    start = 0
    for i in range(1,chunks,1):
        for pos in range(start,len(vals),1):
            tot += vals[pos]
            if tot > wchunk*i:
                start = pos
                weighted.append( vals[pos] )
                break
    weighted.append( vals[-1]+1 )
    return (simple, weighted)

print question2



print '''Distribution of "income" by year of incorporation

(Percentage of total NPO "income" represented by in each year
cohort, banded by size of NPO.  Bands are a standard distribution 
of total current NPO "income")
'''

def distribute( val, bands ):
    val = int(val)
    for pos in range(0,len(bands)-1,1):
        if bands[pos] <= val < bands[pos+1]:
            return pos
    return None

def report2( title, status ):
    global io
    io.write( '\n' +title + '\n')
    
    bands,wbands = medians( [x[1] for x in status], chunks=4 )
    
    years = {}
    totalincome = 0
    totalorgs = {}
    for line in status:
        yr = line[0][1]
        income = line[1]
        if yr == '2008':
            continue
        if not years.has_key( yr ):
            years[ yr ] = [0,0,0,0]
        if not totalorgs.has_key( yr ):
            totalorgs[ yr ] = 0        
        band = distribute( income, wbands )
        years[ yr ][ band ] += income
        totalorgs[ yr ] += 1
        totalincome += income
            
    io.write('Median values: 0') 
    for val in wbands[1:-1]:
        io.write(' <x< %d' % val)
    io.write(' <x\n')
    
    yrs = years.keys()
    yrs.sort()
    for yr in yrs:
        year = years[yr]
        percents = [0,0,0,0]
        for pos in range(0,4,1):
            percents[pos] = float(year[pos]*100)/totalincome
        io.write('%4s %6.2F %6.2F %6.2F %6.2F [%2.2F] (%4d) <%0.0F>\n' % tuple([yr] + percents + [sum( percents ), totalorgs[ yr ], float(sum( year ))/totalorgs[ yr ]]) )
print process( report2, marshal )

print '''Distributions of "income" by number of categories ticked

(Percentage of total NPO income represented by filings 
with a given number of ticks, banded by size of NPO.
Bands are a standard distribution of total NPO "income".)
'''

def report3( title, status ):
    global io
    io.write( '\n' +title + '\n')
    bands,wbands = medians( [x[1] for x in status], chunks=4 )

    ticks = {}
    totalincome = 0
    ticksincome = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    tickscount = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    
    for line in status:
        income = line[1]
        tickcount = sum( line[0][0][0:16] )
        if tickcount == 4:
            tickcount = 3
        elif tickcount > 4:
            tickcount = 4
        #if sum( line[0][0][0:16] ) == 0:
        #    continue
        if not ticks.has_key( tickcount ):
            ticks[ tickcount ] = [0,0,0,0]
        band = distribute( income, wbands )
        ticks[ tickcount ][ band ] += income
        ticksincome[ tickcount-1 ] += income
        tickscount[ tickcount-1 ] += 1
        totalincome += income

    io.write('Median values: 0') 
    for val in wbands[1:-1]:
        io.write(' <x< %d' % val)
    io.write(' <x\n')
    
    tks = ticks.keys()
    tks.sort()
    for tk in tks:
        #if tk == 12:
        #    print tickscount[tk-1]
        #    tickscount[tk-1] += -1
        #    ticksincome[tk-1] += -278907392
        #    if not tickscount[tk-1]:
        #        tickscount[tk-1] = -1
        tick = ticks[tk]
        percents = [0,0,0,0]
        for pos in range(0,4,1):
                percents[pos] = float(tick[pos]*100)/totalincome
        io.write('%2s %6.2F %6.2F %6.2F %6.2F  [%6.2F] %10.0F %4d\n' % tuple([tk] + percents + [sum(percents)] +[float(ticksincome[tk-1])/tickscount[tk-1], tickscount[tk-1]]))
print process( report3, marshal )

print '''Distributions of "income" by number of categories ticked

(Percentage of total NPO income attributable to categories,
banded by size of NPO.  Bands are a standard distribution of
total NPO "income".)
'''

def report4( title, status ):
    global io
    io.write( '\n' +title + '\n')
    bands,wbands = medians( [x[1] for x in status], chunks=4 )

    categories = {}
    totalincome = 0
    
    for line in status:
        income = line[1]
        categoryset = line[0][0]
        tickcount = sum( categoryset )
        band = distribute( income, wbands )
        totalincome += income
        for category in range(1,len(categoryset)+1,1):
            if not categories.has_key( category ):
                categories[ category ] = [0,0,0,0]
            if categoryset[category-1]:
                categories[ category ][ band ] += income/tickcount

    io.write('Median values: 0') 
    for val in wbands[1:-1]:
        io.write(' <x< %d' % val)
    io.write(' <x\n')
    
    cats = categories.keys()
    cats.sort()
    for cat in cats:
        category = categories[cat]
        percents = [0,0,0,0]
        for pos in range(0,4,1):
            percents[pos] = float(category[pos]*100)/totalincome
        io.write('%2s %6.2F %6.2F %6.2F %6.2F [%6.2F]\n' % tuple([cat] + percents + [sum(percents)]))
print 'Hello'
print process( report4, marshal )
