'''
  Utility function for a course index
'''

import re
from pathtool import gslpath
gp = gslpath()

import sys,os

from csvtool import gslCsv

# instructorlist
# courses

# py:strip="not reqd"

def fixnum(s):
    m = re.match('^([0-9]+).*',str(s))
    if m:
        n = int(m.group(1))
    else :
        n = 0
    return n

class courseIndex:
    def __init__(self):
        self.ci_body = open( gp.docroot.src('ci-body.html') ).read()
        self.ci_row = open( gp.docroot.src('ci-row.html') ).read()
        self.ci_instructor = open( gp.docroot.src('util-instructor.html') ).read()
        self.ci_button = open( gp.docroot.src('course-ical-button.html') ).read()

        
    def tag_instructor(self,name,external_flag=None):
        uid = name.replace(' ','_')
        displayname = name.replace(' ','&#160;',1)
        if uid in self.instructorlist:
            instructor = self.ci_instructor
            profile_url = gp.faculty.url(  'gsli%s.html' %uid )
            profile_url_cached = gp.facultycache.url(  'gsli%s.html' %uid )
            instructor = instructor.replace('@@name@@',displayname.replace(" ","&#160;"))
            instructor = instructor.replace('@@profile-url@@',profile_url)
            instructor = instructor.replace('@@profile-url-cached@@',profile_url_cached)
            instructor = instructor.replace('@@instructor-url@@', gp.faculty.url('gsli%s.html' % uid))
        else:
            if (name.find('advisor') > -1 or name.find('staff') > -1):
                instructor = displayname
            elif external_flag:
                instructor = displayname + ' (external)'
            else:
                instructor = displayname
        return instructor.strip()

    def rowclass(self, num, classes):
        rem = num % 2
        if rem:
            return '%s %s' % ('row-odd',classes)
        else:
            return '%s %s' % ('row-even',classes)
            
    def courseindex(self,coursenickname,start,end):
        rowcount = 1
        row_content = ''
        for course in self.courses:
            if fixnum(course['course_number']) < start or fixnum(course['course_number']) > end:
                continue
            instructor = self.tag_instructor( course['instructor'] )
            other_instructors = [ self.tag_instructor(x) for x in course['other_instructors_raw'] ]
            instructors = [instructor] + other_instructors                    

            instructors = ', '.join(instructors)

            row = self.ci_row
            if course['compulsory']:
                row = row.replace('@@required@@', 'required')
            else:
                row = row.replace('@@required@@', 'none')
            row = row.replace('@@class@@', self.rowclass(rowcount,''))
            rowcount += 1
            
            button_url = "%s.ics" % os.path.splitext(course['course_url_cached'])[0]
            button_filename = os.path.split(button_url)[1]
            if os.path.exists(gp.coursescache.release(button_filename)):
                button = self.ci_button.replace("@@NUMBER@@", course['course_number'])
                button = button.replace("@@URL@@", button_url)
            else:
                button = "<span class=\"course-number\">%s</span>" % course['course_number']
            row = row.replace('@@course-button@@', button)
            row = row.replace('@@course-subject@@', course['course_subject'])
            row = row.replace('@@course-url@@', course['course_url'])
            row = row.replace('@@course-url-cached@@', course['course_url_cached'])
            row = row.replace('@@course-title@@', course['course_title'])
            row = row.replace('@@credit@@', course['credit'])
            row = row.replace('@@instructors@@', instructors)
            row = row.replace('@@format@@', course['format'])
            row = row.replace('@@open-to@@', course['open_to'])
            row = row.replace('@@term@@', course['term'])
            row = row.replace('@@course-number@@', course['course_number'])
            row_content += row
        
        body = self.ci_body
        body = body.replace('@@rows@@', row_content)
            
        page = open( gp.courses_index.release('%s/index.html' % coursenickname) ).read()

        page = re.sub('<p>.*?%%content%%.*?</p>','%%content%%',page)
        page = page.replace('%%content%%',body)
        
        open( gp.courses_index.release('%s/index.html' % coursenickname), 'w+').write(page)
