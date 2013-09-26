'''
  Utility function for staff pages
'''

from pathtool import gslpath
gp = gslpath()

import sys,os,re

from csvtool import gslCsv

def fixnum(x):
    return int(str(x)[:3])

class staffPages:
    def __init__(self):

        self.coursesbystaffuid = {}
        
        self.staffinfo_template = open( gp.docroot.src('staffmember-body.html') ).read()
        self.staffinfo_row_template = open( gp.docroot.src("staffmember-table-row.html") ).read()
        self.photo_template = open( gp.docroot.src('staffmember-photo.html') ).read()
        self.staffinfo_external_link = open( gp.docroot.src('staffmember-external-link.html') ).read()
        self.staffinfo_internal_link = open( gp.docroot.src('staffmember-internal-link.html') ).read()

        self.staff_headers = []
        self.staff_headers.append(('profession','Profession'))
        self.staff_headers.append(('status','Academic post'))
        self.staff_headers.append(('affiliation','Faculty of appointment'))
        self.staff_headers.append(('office','Office'))
        self.staff_headers.append(('phone','Phone'))
        self.staff_headers.append(('degrees','Degrees'))
        self.staff_headers.append(('office_hours','Office hours'))
        self.staff_headers.append(('website','Website'))
        self.staff_headers.append(('email','Email'))
        self.staff_headers.append(('courses','Teaching'))
        self.staff_headers.append(('publications','Publications'))
        self.staff_headers.append(('research_interests','Research interests'))
        self.staff_headers.append(('career_history','Career'))
        self.staff_headers.append(('visitorships','Guest professor'))
        self.staff_headers.append(('memberships','Memberships'))
        self.staff_headers.append(('recommended_readings','Readings recommended to prospective applicants'))
        self.staff_headers.append(('preparation_suggestions','Preparation suggestions for prospective applicants'))


    def staffpages(self):
        self.fh.seek(0)
        for data in self.instructor_data:
            ## Extra var values
            filename = 'gsli%s.html' % data['uid']
            have_photo = False
            data['photo_url'] = ""
            photo_filename = data['uid'] + '.jpg'
            rowspan = 0
            tops = ['full_name','profession','status','affiliation','office','phone']

            ## Extra array values
            data['full_name'] = '%s %s' % (data['given_name'],data['family_name'])
    
            if os.path.exists( gp.facultycache.release( photo_filename ) ):
                data['photo_url'] = gp.facultycache.url(photo_filename)
                if data['photo_web_ok'].lower().startswith('y'):
                    have_photo = True
    
            if not data['email_disclose_ok'].lower().startswith('y'):
                data['email'] = ''

            data['courses'] = ''
            if self.taughtby.has_key( data['uid'] ):
                for x in self.taughtby[ data['uid'] ]:
                    url = gp.courses.url('gslc%s.html' %x )
                    if not self.coursesbystaffuid.has_key(data['uid']):
                        self.coursesbystaffuid[data['uid']] = {'GSL': False, 'Leading': False, 'G30': False, 'AW': False}
                    uid = fixnum(x)
                    if uid > 899 and uid < 1000:
                        course_index_url = '/curriculum/econ'
                    elif uid > 799 and uid < 900:
                        course_index_url = '/curriculum/aw'
                        self.coursesbystaffuid[data['uid']]['AW'] = True
                    elif uid > 599 and uid < 700:
                        course_index_url = '/curriculum/leading'
                        self.coursesbystaffuid[data['uid']]['Leading'] = True
                    elif uid > 99 and uid < 200:
                        course_index_url = '/curriculum/g30'
                        self.coursesbystaffuid[data['uid']]['G30'] = True
                    else:
                        course_index_url = '/curriculum/gslenglish'
                        self.coursesbystaffuid[data['uid']]['GSL'] = True

                    course = open( gp.docroot.src('staffmember-onecourse.html') ).read()
                    course = course.replace('@@course-url@@',url)
                    course = course.replace('@@course-index-url@@',course_index_url)
                    course = course.replace('@@course-title@@',self.coursename[x])
                    course = course.replace('@@course-number@@',x)
                    data['courses'] += course

            if not data['publications']:
                data['publications'] = data['Jpublications']

            if have_photo:
                photo = self.photo_template.replace('@@rowspan@@',str(rowspan))
                photo = photo.replace('@@photo-url@@',"/en%s" % data['photo_url'])
                for key in [x[0] for x in self.staff_headers]:
                    if data[key] and key in tops:
                        rowspan = rowspan + 1
                colspan = 2
            else:
                photo = ''
                colspan = 1
            
            row_content = ''
            for item in self.staff_headers:
                rowtext = ''
                if data[item[0]]:
                    mydata = data[item[0]]
                    if item[0] == 'website':
                        m = re.match(".*href=.*", mydata, re.S|re.M)
                        if m:
                            print "** NOTICE: pre-wrapped URL in instructor website field of %s" % data['uid']
                            mydata = re.sub("href=", "target=\"_blank\" href=", mydata)
                        else:
                            splits = re.split("(http:[^\"\'< ]+)",mydata,re.S|re.M)
                            for i in range(1, len(splits), 2):

                                splits[i] = '<a onClick="opener.open(\'%s\', \'_blank\');window.close();" target="_blank" href="%s">%s</a>' % (splits[i],splits[i],splits[i])
                            mydata = ''.join(splits)
                    rowtext = self.staffinfo_row_template.replace('@@data@@',mydata)
                    rowtext = rowtext.replace('@@label@@',item[1])
                    if not item[0] in tops:
                        rowtext = rowtext.replace('@@colspan@@',str(colspan))
                    else:
                        rowtext = rowtext.replace('@@colspan@@','1')
                    row_content += rowtext
    
            staffinfo = self.staffinfo_template.replace('@@popup-content-image@@',photo)
    
            staffinfo = staffinfo.replace('@@full-name@@',data['full_name'])
            staffinfo = staffinfo.replace('@@rows@@',row_content)
    
            popup = self.popup_template.replace('@@name@@',data['full_name'])
            popup = popup.replace('@@content@@',staffinfo)

            link = self.staffinfo_internal_link.replace('@@staff-link@@', filename);
            page = popup.replace('@@popup-content-external-link@@',link)
            open( gp.faculty.release(filename), 'w+' ).write(page)

            page = popup.replace('@@popup-content-external-link@@',self.staffinfo_external_link)
            open( gp.facultycache.release(filename), 'w+' ).write(page)

