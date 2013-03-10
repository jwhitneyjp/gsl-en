#!/usr/bin/python
#-*- encoding: utf8 -*-

import sys,os,re
sys.path.append('%s' % (os.path.dirname(sys.argv[0]),))
base = '%s/../../../' % (os.path.dirname(sys.argv[0]),)
pythonlib = base + '/release/lib/python'
sys.path.append(pythonlib)

from pathtool import gslpath
gp = gslpath()

from datetime import datetime,date

from icalendar import Calendar, Event, LocalTimezone
from myExcelerator import *

from cPickle import Pickler

from CourseIcal import master_course_schedule_factory

pickler = Pickler(open( gp.pickle.src('dates.pickle'), 'wb'))

tzinfo = LocalTimezone()

ws = WrappedWorkbook(sys.argv[1])

sheet_names = ws.sheet_names()

#ofh = open('binran_translations.txt','w')
ifh = open( gp.pickle.src('binran_translations.txt'), 'r')
tx = ifh.read()
ifh.close()

pickledates = {}

translations = {}
tx = re.split("\n",tx)
for pos in range(len(tx)-1,-1,-1):
    if tx[pos].startswith('  '):
        key = tx[pos-1].decode('utf8')
        translation = tx[pos].strip()
        translations[key] = translation
    

cal = Calendar()
cal.add('prodid', '-//Faculty calendar//gsl-nagoya-u.net//')
cal.add('version', '2.0')

count = 1

data = ws.get_sheet(sheet_names[0],keyrow=None)

#print sheet.encode('utf8')
year = int(re.sub('^([0-9]*).*','\\1',data[(0,0)]))

cal = master_course_schedule_factory('Postgraduate calendar',dates=False)

#if month < 4:
#        year = year + 1

for d in data.keys():
        print '%d:%d %s' % (d[0],d[1],data[d])
        if d[1] == 2:
            s = data[d].strip()
            r = re.match('(?:([0-9]*)月([0-9]*)日)（(?:月|火|水|木|金)）(?:[・～](?:([0-9]+)月)*([0-9]+)日)*(?:.*)'.decode('utf8'),s)
            if r:
                key = data[(d[0],1)]
                title = translations[key]
                if title.startswith('*'):
                    fulltitle = title
                    title = title[title.find('*',1):]
                else:
                    fulltitle = title
                #ofh.write(title+'\n')
                #event = Event()
                #event.add('summary', title)
                #event.add('class', 'PUBLIC')
                #event.add('dtstamp', datetime.now())
                #stamptime = datetime.now().strftime('%Y%m%dT%H%M%S')
                #event['uid'] = '%s/%0.4d@gsl-handbook-schedule' % (stamptime,count)
                #event.add('priority', 5)
                l = len(r.groups())
                if l == 2 or r.group(3) == None:
                    sday = int(r.group(2))
                    eday = int(r.group(2))
                    
                    smonth = int(r.group(1))
                    emonth = int(r.group(1))
                    
                elif l == 3 or r.group(4) == None:
                    sday = int(r.group(2))
                    eday = int(r.group(3))
                    
                    smonth = int(r.group(1))
                    emonth = int(r.group(1))
                    
                else:
                    sday = int(r.group(2))
                    eday = int(r.group(4))
                    
                    smonth = int(r.group(1))
                    emonth = int(r.group(3))
                    
                syear = year
                eyear = year
                if smonth < 4:
                    syear = year + 1
                if emonth < 4:
                    eyear = year + 1
                mtg_start = date(syear,smonth,sday)
                mtg_end = date(eyear,emonth,eday)
                #event.add('dtstart', mtg_start)
                #event.add('dtend', mtg_end)

                # Make a note of the three significant dates for
                # the course schedule
                r2 = re.match('^\*([^*]+)\*.*',fulltitle)
                if r2:
                    label = r2.group(1)
                    if label == 'Winter return':
                        pickledates[r2.group(1)] = mtg_end
                    else:
                        pickledates[r2.group(1)] = mtg_start
                
                if title == 'Oral examinations for the Masters degree (October entry)':
                    print 'OK!'
                    print mtg_start.strftime('%Y-%m-%d')
                    print mtg_end.strftime('%Y-%m-%d')
                cal.one_postgraduate_event(title,mtg_start,mtg_end)


f = open( gp.ics.src('Postgraduate_Calendar.ics'), 'wb')
f.write(cal.mastercal.as_string())
f.close()

pickler.dump(pickledates)

print 'Done.'
