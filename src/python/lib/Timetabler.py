'''
  Utility function that adds a timetable to a spreadsheet
  and returns HTML for the same timetable.
'''

import sys,os.path
sys.path.append('%s/../modules' % os.path.dirname(sys.argv[0]))
from myExcelerator import *
from Excellist import formatter
from pathtool import gslpath
gp = gslpath()


### Add timetable to worksheet
def write_timetable(w,term,timetable_title):

    if not term in ['Spring', 'Fall']:
        print 'Error: term for write_timetable must be Spring or Fall.'
        sys.exit()
    
    workbook = WrappedWorkbook( gp.xls.src('courses.xls') )
    c = workbook.get_sheet()

    days = ['Mo','Tu','We','Th','Fr']

    schedule = []
    
    c.skip_rows.extend([0,1])

    def daytime (data):
        dts = []
        str = data['day_and_time'].replace(',',' ').replace('&', ' ')
        lst = str.rsplit("\s+")
        day = lst[0]
        day = day.strip()[0:2]
        day = days.index(day)    
        
        times = lst[1:]
        for time in times:
            time = int(time.strip()[0])-1
            dts.append((day,time))
        return dts

    while 1:
        try:
            data = c.nextmap()
        except:
            break

        if not data['format'].lower() in ['lecture','seminar']:
            c.skip()
            continue
        if not data['day_and_time']:
            c.skip()
            continue
        
        classterm = data['term']
        if not term:
            print 'Error: no value for term variable'
            sys.exit()
        if term == 'Spring':
            if classterm[0] != '1' and not classterm.lower().count('year'):
                c.skip()
                continue
        elif term == 'Fall':
            if classterm[0] != '2' and not classterm.lower().count('year'):
                c.skip()
                continue
            
        try:
            data['day_and_time'].split(' ')
        except ValueError:
            c.skip()
            print 'Day/time format error: %s' % (data['course_title'])
            continue
        try:
            dts = daytime(data)
        except ValueError:
            print 'Missed the date (?) %s for %s' % (data['day_and_time'], data['course_title'])
        for dt in dts:
            schedule.append(dt)

    
    maxcells = [0,0,0,0,0]

    total_items = []
    for row in range(0,5,1):
        row_values = []
        for cell in range(0,5,1):
            row_values.append(0)
        total_items.append(row_values)

    current_offset = []
    for row in range(0,5,1):
        row_values = []
        for cell in range(0,5,1):
            row_values.append(0)
        current_offset.append(row_values)

    block_totals = []
    for row in range(0,5,1):
        row_values = []
        for cell in range(0,5,1):
            row_values.append(0)
        block_totals.append(row_values)

    # Get the total number of items in each day/time block
    for s in schedule:
        day,time = s
        total_items[day][time] = total_items[day][time]+1

    # Get the tallest block in each time band
    for time in range(0,5,1):
        maxval = 0
        for day in total_items:
            if maxval < day[time]:
                maxval = day[time]
        maxcells[time] = maxval

    ## Moving everything over four spaces.  Yawn.
        
    total_rows = 0
    for rows in maxcells:
        total_rows = total_rows + rows

    base_offset = []
    t = 0
    for pos in range(0,len(maxcells),1):
        base_offset.append(t)
        t = t + maxcells[pos]

    # Set uniform offsets for each time band
    for time in range(0,5,1):
        for day in block_totals:
            day[time] = maxcells[time]

    # Create empty table with slots for every class
    table = []
    for row in range(0,total_rows,1):
        table.append([{},{},{},{},{}])

    # Read in data again and set maps in table
    c.reset()

    base_offset = base_offset

    iter = 1
    while 1:
        try:
            data = c.nextmap()
        except:
            break

	dts = daytime(data)
        for dt in dts:
            day,time = dt
            # Populate the table
            vstart = base_offset[time]
            offset = current_offset[day][time]
            slot = table[offset + base_offset[time]][day]
            if slot:
                print "Error: data overwrite"
                print 'Iteration: %d' % (iter,)
                print 'Day: %d' %day
                print 'Time: %d' %time
                print 'Offset: %d' %offset
                print 'Vstart: %d' %vstart
                #print slot
                sys.exit()
            slot.update(dt)
            current_offset[day][time] = offset + 1
            iter = iter+1
    
    # Now build whatever you want by dropping this
    # structure into a grinder

    ws = w.add_sheet(timetable_title)
    formatter(ws).setup_timetable_worksheet(timetable_title,
                                            base_offset, maxcells)

    # Without line                                        
    style = XFStyle()
    font = Font()
    font.height = 190
    style.font = font

    align = Alignment()
    align.wrap = Alignment.WRAP_AT_RIGHT
    align.vert = Alignment.VERT_CENTER
    align.horz = Alignment.HORZ_CENTER
    style.alignment = align

    # With line                                        
    lstyle = XFStyle()
    font = Font()
    font.height = 190
    lstyle.font = font

    align = Alignment()
    align.wrap = Alignment.WRAP_AT_RIGHT
    align.vert = Alignment.VERT_CENTER
    align.horz = Alignment.HORZ_CENTER
    lstyle.alignment = align

    borders = Borders()
    borders.bottom = Borders.THIN
    lstyle.borders = borders

                                            
    row = 2
    cell = 1
    for tier in table:
        cell = 1
        if row-2 in [x-1 for x in base_offset] or row-2 == len(table)-1:
            thestyle = lstyle
        else:
            thestyle = style
        for course in tier:
            if course.has_key('course_title'):
                num = course['course_number']
                title = course['course_title']
                staff = course['instructor']
                open_to = course['open_to']
                room = course['room']
                if room:
                    text = '\n#%s %s\n%s\n%s\n[%s]\n' % (num,title,staff,open_to,room)
                else:
                    text = '\n#%s %s\n%s\n%s\n' % (num,title,staff,open_to)
                ws.write(row,cell,text,thestyle)
            else:
                ws.write(row,cell,'',thestyle)
            cell = cell + 1
        row = row+1
