#!/usr/bin/python
#-*- encoding: utf8 -*-

import sys,os,re
sys.path.append('%s' % (os.path.dirname(sys.argv[0]),))
base = '%s/../../../' % (os.path.dirname(sys.argv[0]),)
pythonlib = base + '/src/python/lib'
sys.path.append(pythonlib)

from pathtool import gslpath
gp = gslpath()

from datetime import datetime
from icalendar import Calendar, Event, LocalTimezone
from myExcelerator import *
from CourseIcal import master_course_schedule_factory
from csvtool import gslCsv

tzinfo = LocalTimezone()

rex1 = re.compile('.*（([0-9]{2}):([0-9]{2}).*'.decode('utf8'))

ws = WrappedWorkbook(sys.argv[1])
ws.dump_csv( gp.csv.src('faculty_meetings_raw.csv') ,sheetoffset=0, sheets=12, rowoffset=3)
base_year = int(re.sub('^([0-9]*).*','\\1',ws.data[0][1][(0,0)]))

cal = master_course_schedule_factory('Faculty meetings')

count = 1
oldday = 1

fh = open( gp.csv.src('faculty_meetings_raw.csv') )
c = gslCsv( fh, offset=0 )
for entry in c:
    #print sheet.encode('utf8')
    
    month = int(re.sub('^([0-9]*).*','\\1',entry['sheetname']))
    year = base_year
    if month < 4:
        year = base_year + 1
        
    if entry['法学研究科'].count('教授会'.decode('utf8')):
        if entry['日']:
            day = int(float(entry['日']))
        else:
            day = oldday
        
        oldday = day
        
        hour = 13
        minute = 0
                
        if not entry['法学研究科'].strip() == '教授会'.decode('utf8'):
            date = datetime(year,month,day).strftime('%Y/%m/%d')
            print 'Adjustment needed? %s %s' % (entry['法学研究科'].strip(),date)
            r1 = rex1.match(entry['法学研究科'])
            if r1:
                print '  Adjustment attempted'
                hour = int(r1.group(1))
                minute = int(r1.group(2))
                
        #print '%d/%d/%d' % (year,month,day)
        mtg_start = datetime(year,month,day,hour,minute,0,tzinfo=tzinfo)
        mtg_end = datetime(year,month,day,18,0,0,tzinfo=tzinfo)
        
        cal.one_faculty_meeting(mtg_start,mtg_end)
                
        #event = Event()
        #event.add('summary', 'Faculty meeting')
        #event.add('dtstart', mtg_start)
        #event.add('dtend', mtg_end)
        #event.add('dtstamp', datetime.now())
        #stamptime = datetime.now().strftime('%Y%m%dT%H%M%S')
        #event['uid'] = '%s/%0.4d@gsl-nagoya-u.net' % (stamptime,count)
        #event.add('priority', 5)
        
        #cal.add_component(event)
        #count = count + 1

f = open( gp.ics.src('Faculty_Meetings.ics'), 'wb')
f.write(cal.mastercal.as_string())
f.close()


#c1 = '・'.decode('utf8')
#print ord(c1)
#c1 = '～'.decode('utf8')
#print ord(c1)
