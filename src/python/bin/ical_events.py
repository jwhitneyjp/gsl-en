#!/usr/bin/python
#-*- encoding: utf8 -*-

import sys,os,re
sys.path.append('%s' % (os.path.dirname(sys.argv[0]),))
base = '%s/../../../' % (os.path.dirname(sys.argv[0]),)
pythonlib = base + '/src/python/lib'
sys.path.append(pythonlib)

from pathtool import gslpath
gp = gslpath()

from datetime import datetime,date
from icalendar import Calendar, Event, LocalTimezone
from myExcelerator import *
from CourseIcal import master_course_schedule_factory
from csvtool import gslCsv

tzinfo = LocalTimezone()

rex1 = re.compile('.*（([0-9]{2}):([0-9]{2}).*'.decode('utf8'))
rex2 = re.compile('.*?([0-9]{4})年([0-9]+)月([0-9]+)日.*?(barf)*(?:([0-9]+)月)(?:([0-9]+)日).*'.decode('utf8'))
rex3 = re.compile('.*?([0-9]{4})年([0-9]+)月([0-9]+)日.*?(barf)*(barf)*(?:([0-9]+)日).*'.decode('utf8'))
rex4 = re.compile('.*?([0-9]{4})年([0-9]+)月([0-9]+)日.*?(barf)*(barf)*(barf)*.*'.decode('utf8'))
# What a float looks like
rex5 = re.compile('[0-9]+\.[0-9]+')
# Four numbers
rex6 = re.compile('.*?([0-9]{1,2})[:：]([0-9]{2}).*?([0-9]{1,2})[:：]([0-9]{2})')
# Two numbers
rex7 = re.compile('.*?([0-9]{1,2})[:：]([0-9]{2})')

ifh = open( gp.pickle.src('binran_translations.txt'), 'r')
tx = ifh.read()
ifh.close()

translations = {}
tx = re.split("\n",tx)
for pos in range(len(tx)-1,-1,-1):
    if tx[pos].startswith('  '):
        key = tx[pos-1].decode('utf8')
        translation = tx[pos].strip()
        translations[key] = translation

ws = WrappedWorkbook(sys.argv[1])
ws.dump_csv( gp.csv.src('events_raw.csv') ,rowoffset=1)

cal = master_course_schedule_factory('Events')

fh = open( gp.csv.src('events_raw.csv') )
c = gslCsv( fh, offset=0 )
for entry in c:
    if translations.has_key(entry['行事の種類'].decode('utf8')):
        e_type =  translations[entry['行事の種類'].decode('utf8')]
    else:
        e_type =  entry['行事の種類']
    
    # Get the time set, if any
    ## Normalize
    if rex5.match(entry['時間']):
        entry['時間'] = '%0.2f' % (24 * float(entry['時間']),)
    entry['時間'] = str(entry['時間']).replace('.',':')
    ## Try for 4 numbers, then try for 2
    rt = rex6.match(entry['時間'])
    if not rt:
        rt = rex7.match(entry['時間'])
    if rt:
        times = list(rt.groups())
        if len(times) == 2:
            times.extend(times)
    if not rt:
        times = [0,0,0,0]
        
    times = [int(x) for x in times]
    
    rd = rex2.match(entry['年月日'].decode('utf8'))
    if not rd:
        rd = rex3.match(entry['年月日'].decode('utf8'))
    if not rd:
        rd = rex4.match(entry['年月日'].decode('utf8'))

    if not rd:
        print 'NOGO'
        continue
    dates = list(rd.groups())
    for pos in range(3,6,1):
        if dates[pos] == None:
            dates[pos] = dates[pos-3]
    dates = [int(x) for x in dates]

    title = entry['英文']
    location = entry['英文会場']

    print times
    if ''.join([str(x) for x in dates[0:3]]) == ''.join([str(x) for x in dates[3:6]]):
        if times[0]:
            start_date = datetime(dates[0],dates[1],dates[2],times[0],times[1],0,tzinfo=tzinfo)
        else:
            start_date = date(dates[0],dates[1],dates[2])
    else:
        start_date = date(dates[0],dates[1],dates[2])

    if ''.join([str(x) for x in dates[0:3]]) == ''.join([str(x) for x in dates[3:6]]):
        if times[0]:
            end_date = datetime(dates[3],dates[4],dates[5],times[2],times[3],0,tzinfo=tzinfo)
        else:
            end_date = date(dates[3],dates[4],dates[5])
    else:
        end_date = date(dates[3],dates[4],dates[5])

    #
    # Okay, we have the date range.  Now we need to do something
    # with the time, which unfortunately can also be a range.
    # Maybe just call multi-day events all day events and
    # leave it at that.  Then no special handling of dates
    # for special cases in a series is required.
    #
    
    cal.one_postgraduate_event(title,start_date,end_date,location=location)
    
f = open( gp.ics.src('Events.ics'), 'wb')
f.write(cal.mastercal.as_string())
f.close()


#c1 = '・'.decode('utf8')
#print ord(c1)
#c1 = '～'.decode('utf8')
#print ord(c1)
