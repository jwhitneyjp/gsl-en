#!/usr/bin/python2.7
#-*- encoding: utf-8 -*-

import sys,os,os.path
sys.path.append('%s' % (os.path.dirname(sys.argv[0]),))
base = '%s/../../../' % (os.path.dirname(sys.argv[0]),)
pythonlib = base + '/src/python/lib'
sys.path.append(pythonlib)

from pathtool import gslpath
gp = gslpath()
from pagetool import gslCsv
from pagetool import CourseReports

from okuda import fetch
from GetJseInfo import getJseUrls,normalizeJseName,getJseUpdate
from myExcelerator import WrappedWorkbook,Workbook
import re
from Excellist import formatter
import Timetabler

from optparse import OptionParser

parser = OptionParser()

parser.add_option("-w", "--web-update", dest="web_update", action="store_true",
                  help="Update staff info from Japanese website")
parser.add_option("-y", "--syllabus-update", dest="syllabus_update", action="store_true",
                  help="Update syllabus spreadsheet from online Syllabus System")
parser.add_option("-r", "--reports", dest="report_update", action="store_true",
                  help="Update zipped report of courses under appendix/reports")

(options, args) = parser.parse_args()

web_update = options.web_update
syllabus_update = options.syllabus_update
report_update = options.report_update

rex1 = re.compile(u'^([-0-9]*) *(.*)$',re.M)
rex2 = re.compile(u'^(.*)\s*--\s*(.*)$')
rex4 = re.compile(u'^.*\[Subject:(.*?)\](.*)$',re.M|re.S)
rex5 = re.compile(u'^(.*)\[([0-9]+)\].*$',re.M|re.S)

currentdir = os.getcwd()

#staffinfodir = '%s/StaffInfo' % (currentdir,)

files = os.listdir( gp.staffinfo.src('') )
try:
    files.remove('.svn')
except:
    pass

try:
    files.remove('.git')
except:
    pass

if len(files) > 0 or web_update:
    
    print ""
    print "Update staff info (from forms and Japanese website)"

    delfiles = []
    
    # File for reading
    old = WrappedWorkbook( gp.xls.src('instructors.xls') )
    c = old.get_sheet()
    keys_and_labels = c.extract_keys_and_labels()
    
    os.chdir( gp.staffinfo.src('') )
    
    # File for writing
    new = Workbook()
    ws = new.add_sheet('Staff Profiles')
    s = formatter(ws)
    s.setup_instructors_worksheet(keys_and_labels)

    # Fetch Japanese website url map
    url = 'http://www.law.nagoya-u.ac.jp/teacher/index.html'
    webdoc = fetch(url,'UTF-8')
    prof_urls = getJseUrls(webdoc)
    
    while 1:
        try:
            data = c.nextmap().copy()
        except:
            break
        #
        # Update from any submitted personal profile spreadsheets
        filename = '%s.xls' % (data['uid'],)
        if filename in [f.strip() for f in files]:
            w2 = WrappedWorkbook(filename)
            e =  w2.get_entrysheet()
            u = e.get_update()
            data.update(u)
            delfiles.append(filename)
        #
        # Update from Japanese website data
        if data['proper_name'].strip():
            proper_names = [x.strip() for x in data['proper_name'].split('\n')]
            u = None
            for proper_name in proper_names:
                try:
                    url = prof_urls[normalizeJseName(proper_name)]
                    url = 'http://www.law.nagoya-u.ac.jp/teacher/%s' %url
                    #print url
                    doc = fetch(url,'UTF-8')
                    #
                    # Warning: map keys are hardwired in this function
                    print data['proper_name']
                    u = getJseUpdate(doc)
                    data.update(u)
                    print "  done"
                    break
                except:
                    pass
            if not u:
                print "  Warning: no Japanese site data for %s" %data['uid']
        else:
            print 'Warning: no proper name in spreadsheet for %s' %data['uid']
        s.writemap(data)
        
    ws.col(1).level = 5
    ws.col(2).level = 5
    ws.col(3).level = 5
    ws.col(4).level = 5
    ws.col(5).level = 5
    ws.col(6).level = 5
    ws.col(7).level = 5
    ws.col(8).level = 5
    ws.col(9).level = 5
    ws.col(10).level = 5

    ws.col(11).level = 4
    ws.col(12).level = 4
    ws.col(13).level = 4
    ws.col(14).level = 4
    ws.col(15).level = 4

    ws.col(16).level = 3
    ws.col(17).level = 3
    ws.col(18).level = 3

    ws.col(19).level = 2
    ws.col(20).level = 2
    ws.col(21).level = 2
    ws.col(22).level = 2

    ws.col(23).level = 1
    ws.col(24).level = 1

    ws.panes_frozen = True
    ws.horz_split_pos = 1
    
    ws.rows[1].hidden = 1

    os.chdir(currentdir)
    
    new.save( gp.xls.src('instructors.xls') )
    
    os.chdir( gp.staffinfo.src('') )
    
    for file in delfiles:
        os.unlink(file)
    
    os.chdir(currentdir)
    
    print "Done"

print ""
print "Generating instructors.csv"
trial = WrappedWorkbook( gp.xls.src('instructors.xls'))
trial.dump_csv( gp.csv.src('instructors.csv') ,rowoffset=1, plaintext=['proper_name'])
    
###### end staff spreadsheet update ######


###### course info update (start) ######
    
if syllabus_update:
    print ""
    print "Download Syllabus System content"

    w = Workbook()
    ws = w.add_sheet('Courses')
    
    s = formatter(ws)
    s.setup_courses_worksheet()
    
    stubs = ['30g14/list_all','gs14/list_all']
    for stub in stubs:
        url = "http://infosv.law.nagoya-u.ac.jp/english/syllabus/as/v/%s" % (stub,)
        print "  Fetching page index"

        idoc = fetch(url,'EUC-JP')
        
        res = idoc.xpathEval('//table[2]/tbody/tr/td[1]/a[@href]')
        print "  Analyzing"
        urls = [x.prop('href') for x in res]
        
        # normalize url
        root = '/'.join(url.split('/')[0:-1])
    
        print "  Processing pages and creating Excel spreadsheet"
        sys.stdout.write("  ")
        sys.stdout.flush()
        
        for u in urls:
            url_root = '%s/%s' % (root,u)
            ss_code = u.split('/')[1]
    
            pdat = {}
        
            url1 = '%s/setup_form' % (url_root,)
            idoc = fetch(url1,'EUC-JP')
            # Get page as string
            pageA = idoc.serialize()
            # Extract content
            res = idoc.xpathEval('//input[@type = "text"]')
            for r in res:
                pdat[r.prop('name')] = r.prop('value').decode('utf8')
    
            url2 = '%s/edit_abst_form' % (url_root,)
            print url2
            idoc = fetch(url2,'EUC-JP')
            # Get page as string
            pageB = idoc.serialize()
            # Extract content
            res = idoc.xpathEval('//textarea')
            for r in res:
                pdat[r.prop('name')] = r.content.decode('utf8')
            
            url3 = '%s/edit_plan_form' % (url_root,)
            idoc = fetch(url3,'EUC-JP')
            res = idoc.xpathEval('//textarea')
            sessions = []
            for r in res:
                if r.prop('name').endswith('_theme_text'):
                    sessions.append(r.content.decode('utf8'))
            session_html = ''
            session_count = 1
            for session_text in sessions:
                session_html += '<tr><td><div>%d</div></td><td><div>%s</div></td></tr>' % (session_count,session_text)
                session_count += 1
            pdat['sessions'] = session_html

            updat = {}
            r = rex1.match(pdat['lec_title_data'])
            if not r:
                print 'Missing course number at %s' % (url1,)
                sys.exit()
            updat['course_number'] = r.group(1).strip()
            updat['course_title'] = r.group(2).strip()
            #
            # Workaround to cope with the fact that courses
            # added to the Syllabus System by mistake apparently
            # cannot be removed gracefully.
            #
            if not updat['course_title']:
                continue
    
            r = rex4.match(pdat['mycomment'])
            if not r:
                print 'Missing subject at %s' % (url2,)
                sys.exit()
            
            if r.group(1).strip() == 'placeholder':
                continue
    
            updat['course_subject'] = r.group(1).strip()
            updat['notes'] = r.group(2).strip()
    
            term_data = pdat['term_data']
            term_data = re.sub('(?i)(fall)',' 2 ',term_data)
            term_data = re.sub('(?i)(spring)',' 1 ',term_data)
            term_data = re.sub('[^ 0-9]',' ',term_data)
            term_data = re.sub('\s+',' ',term_data).strip()
            r = rex5.match(term_data)
            if not r:
                term = term_data
                updat['year_offered'] = ''
            else:
                term = r.group(1).strip()
                updat['year_offered'] = r.group(2)
            updat['offered_this_year'] = ''
            if term == '1':
                term = 'Spring'
            elif term == '2':
                term = 'Fall'
            else:
                pass
            updat['term'] = term
            updat['instructor'] = pdat['teacher_data'].strip()
            updat['other_instructors'] = pdat['teachers_data'].strip()
            updat['format'] = pdat['lec_type_data'].strip()
            updat['open_to'] = pdat['target_data'].strip()
            updat['day_and_time'] = pdat['period_data'].strip()
            updat['credit'] = pdat['credit_data'].strip()
    
            if pdat['compulsory_data']:
                updat['compulsory'] = 'Yes'
            else:
                updat['compulsory'] = ''
    
            r = rex2.match(pdat['room_data'])
            if not r:
                updat['room'] = pdat['room_data']
                updat['start_date'] = ''
            else:
                updat['room'] = r.group(1).strip()
                updat['start_date'] = r.group(2).strip()
    
            updat['course_outline'] = pdat['myabst'].strip()
            updat['course_objective'] = pdat['myaim'].strip()
            updat['textbooks'] = pdat['mytextbooks'].strip()
            updat['references'] = pdat['myref_books'].strip()
            updat['evaluation'] = pdat['myeval'].strip()
            updat['prerequisites'] = pdat['mycond'].strip()
            updat['ss_code'] = ss_code.strip()

            updat['sessions'] = pdat['sessions']
    
            # Ical output
            if updat['offered_this_year'] and updat['day_and_time']:
                ical_nameroot = updat['course_title'].replace(' ','_')
                if False and cal:
                    cfh = open( gp.calendar.src('teaching/%s.ics' % ical_nameroot), 'wb')
                    cal.one_course_schedule(updat)
                    cfh.write(cal.juniorcal.as_string())
                    cfh.close()
    
            s.writemap(updat)

            sys.stdout.write(".")
            sys.stdout.flush()
    
        print ""
    print "  Add timetable spreadsheets"

    w.save( gp.xls.src('courses.xls') )

    #Timetabler.write_timetable(w,'Spring','Spring Term 2008 Timetable')
    #Timetabler.write_timetable(w,'Fall','Fall Term 2008 Timetable')

    #f = file('courses.xls', 'wb')
    #f.write(w.get_biff_data())
    #f.close()
    w.save( gp.xls.src('courses.xls') )

    trial= WrappedWorkbook( gp.xls.src("courses.xls") )
    trial.dump_csv( gp.csv.src("courses.csv"), sheetoffset=0,sheets=1,rowoffset=1)

if report_update:
    reports = CourseReports()
    course_fh = gp.csv.src("courses.csv")
    course_c = gslCsv(course_fh,offset=0)
    instructor_fh = gp.csv.src("instructors.csv")
    instructor_c = gslCsv(instructor_fh,offset=0)
    instructors = {}
    for instructordata in instructor_c:
        instructors[instructordata['uid']] = instructordata
    for coursedata in course_c:
        reports.set(coursedata,instructors)
        reports.save()
        
print ""
print "Done"


    
