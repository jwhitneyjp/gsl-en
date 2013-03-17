'''
Hello
'''

from pathtool import gslpath
gp = gslpath()
import re,sys

sys.path.append(gp.pyblosxom.src(''))
sys.path.append(gp.info.src(''))

from term_dates import term_dates
from newslists import DateEngine
from csvtool import gslCsv
from CourseReports import CourseReports

def fixnum(x):
    return int(str(x)[:3])

class coursePages:
    def __init__(self):
        ## Instructor codes
        self.instructorcodes('instructors.csv')

        ## Templates
        ### Popups
        self.popup_template = open( gp.docroot.src( 'popup-template.html') ).read()
        self.course_template = open( gp.docroot.src('course-body.html') ).read()
        self.course_row_template = open( gp.docroot.src('course-row-item.html') ).read()

        ## Static
        self.course_compulsory_note = open( gp.docroot.src('course-compulsory-note.html') ).read()
        self.course_instructor_link = open( gp.docroot.src('course-instructor-link.html') ).read()
        self.course_instructor_nolink = open( gp.docroot.src('course-instructor-nolink.html') ).read()
        self.course_external_link = open( gp.docroot.src('course-external-link.html') ).read()
        self.course_internal_link = open( gp.docroot.src('course-internal-link.html') ).read()

        self.course_headers = []
        self.course_headers.append(('other_instructors','Other<br />instructors'))
        self.course_headers.append(('format','Format'))
        self.course_headers.append(('term','Term offered'))
        self.course_headers.append(('open_to','Open to years'))
        self.course_headers.append(('credit','Credit'))
        # Important: start_date must be placed AFTER day_and_time!
        self.course_headers.append(('day_and_time','Schedule'))
        self.course_headers.append(('start_date','Start date'))
        self.course_headers.append(('room','Room'))
        self.course_headers.append(('course_outline','Course<br />outline'))
        self.course_headers.append(('course_objective','Course<br />objective'))
        self.course_headers.append(('textbooks','Textbooks'))
        self.course_headers.append(('references','Additional<br />references'))
        self.course_headers.append(('evaluation','Evaluation'))
        self.course_headers.append(('prerequisites','Prerequisites'))
        self.course_headers.append(('notes','Remarks'))

    def instructorcodes(self, csv):
        self.instructor_codes = {}
        fh = open( gp.csv.src(csv))
        c = gslCsv( fh, offset=0 )
        for data in c:
            self.instructor_codes[data['uid']] = data

    def coursepages(self,csv):
        fh = open( gp.csv.src(csv) )
        c = gslCsv( fh, offset=0 )

        for data in c:
            instructor = re.sub('\(.*','',data['instructor']).strip()
            data['instructor'] = instructor
        
            i = data['instructor']
            instructor_key = re.sub('  *',' ',i).replace(' ','_')
            instructor_url =  gp.faculty.url('gsli%s.html' % instructor_key )
    
            if not self.taughtby.has_key(instructor_key):
                self.taughtby[instructor_key] = []
            self.taughtby[instructor_key].append(data['course_number'])
        
            if data['other_instructors']:
                other = data['other_instructors'].replace(';',',')
                other = [x.strip() for x in other.split(',')]
            else:
                other = []
            data['other_instructors_raw'] = other[:]
            for opos in range(0, len(other), 1):
                o = other[opos]
                o_key = re.sub('  *',' ',o.strip()).replace(' ','_')
                if not self.taughtby.has_key(o_key):
                    self.taughtby[o_key] = []
                self.taughtby[o_key].append(data['course_number'])
                # Am I a valid instructor key?
                if self.instructor_codes.has_key(o_key):
                    other[opos] = self.course_instructor_link.replace("@@instructor-url@@",gp.faculty.url('gsli%s.html' % o_key)).replace("@@instructor-name@@", self.instructor_names[o_key])
                    data['other_instructors_raw'][opos] = o_key.replace("_"," ")

            self.coursename[data['course_number']] = data['course_title']
    
            data['other_instructors'] = ", ".join(other)
            data['course_url'] = gp.courses.url( 'gslc%s.html' % (data['course_number'],) )
            data['course_url_cached'] = gp.coursescache.url( 'gslc%s.html' % (data['course_number'],) )

            self.courses.append(data)
    
            ## Course information page
            #XXX
            filename = 'gslc%s.html' % data['course_number']
            icsname = 'gslc%s.ics' % data['course_number']
            docname = 'gslc%s.rtf' % data['course_number']
            row_content = ''
            dateEngine = None
            for item in self.course_headers:
                if data[item[0]]:
                    row = self.course_row_template.replace('@@label@@',item[1])
                    val = str(data[item[0]])
                    if item[0] == "start_date":
                        if dateEngine and dateEngine.ics_type == "repeating":
                            val = dateEngine.getStartDate()
                        else:
                            val = ''
                    if item[0] == 'day_and_time':
                        dateData = {}
                        dateData['date-and-time'] = data[item[0]]
                        dateData['title'] = "%s %s" % (data['course_number'],data['course_title'])
                        dateData['organizer'] = data['instructor']
                        dateData['email'] = 'see website for contact details'
                        if self.instructor_codes.has_key(instructor_key):
                            email_disclose_ok = self.instructor_codes[instructor_key]['email_disclose_ok']
                            email =  self.instructor_codes[instructor_key]['email']
                            if email and email_disclose_ok:
                                if email_disclose_ok[0].lower() == "y":
                                    if email.find("@") > -1:
                                        dateData['email'] = email
                                    else:
                                        dateData['email'] = "%s@law.nagoya-u.ac.jp" % email
                        dateData['place'] = data['room']
                        dateData['start_date'] = data['start_date']
                        term = data['term']
                        term = re.sub('(?i)spring','1',term)
                        term = re.sub('(?i)fall','2',term)
                        m = re.match("^([12I]).*",term)
                        if m:
                            dateData['term'] = m.group(1)
                        else:
                            print "** WARNING: missing term for course %s, setting to 1 (Fall)" % data['course_number']
                            dateData['term'] = "1"
                        dateEngine = DateEngine('Asia/Tokyo', gp.docroot.src(''), '/curriculum/cache/%s' % filename, dateData, term_dates=term_dates)
                        if dateEngine.valid:
                            val = dateEngine.humanDates()
                            open(gp.coursescache.release(icsname), "w+").write(dateEngine.getIcs())
                    row = row.replace('@@data@@', val )
                    row_content += row

            course = self.course_template.replace('@@course-number@@',data['course_number'])
            course = course.replace('@@course-subject@@',data['course_subject'])
            course = course.replace('@@course-title@@',data['course_title'])
            if data['compulsory']:
                course = course.replace('@@compulsory-subject@@',self.course_compulsory_note)
            else:
                course = course.replace('@@compulsory-subject@@','')
            if data['offered_this_year'].lower().startswith('n'):
                course = course.replace('@@offered@@','No')
            else:
                course = course.replace('@@offered@@','Yes')
            if instructor_key in self.instructorlist:
                course = course.replace('@@instructor-block@@',self.course_instructor_link)
                course = course.replace('@@instructor-url@@',instructor_url)
                course = course.replace('@@instructor-name@@', self.instructor_names[instructor_key] )
            else:
                course = course.replace('@@instructor-block@@',self.course_instructor_nolink)
                course = course.replace('@@instructor-name@@', instructor)
            course = course.replace('@@rows@@',row_content)
        
            popup = self.popup_template.replace('@@content@@', course)
            popup = popup.replace('@@name@@',data['course_title'])
            link = self.course_internal_link.replace('@@course-link@@',filename)
            syllabus_popup = popup.replace('@@popup-content-external-link@@',link)
            open( gp.courses.release(filename), 'w+' ).write(syllabus_popup)

            if fixnum(data['course_number']) > 899 and fixnum(data['course_number']) < 1000:
                category = 'econ'
            elif fixnum(data['course_number']) > 599 and fixnum(data['course_number']) < 700:
                category = 'leading'
            elif fixnum(data['course_number']) > 99 and fixnum(data['course_number']) < 200:
                category = 'g30'
            else:
                category = 'gslenglish'
            link = self.course_external_link.replace('@@category@@',category)
            cache_popup = popup.replace('@@popup-content-external-link@@',link)
            open( gp.coursescache.release(filename), 'w+' ).write(cache_popup)

            # Move office file into place while we're at it
            rtf = open(gp.doc.src(docname)).read()
            open( gp.coursescache.release(docname), 'w+').write(rtf)

        fh.close()
        
