''' Make a module of me
'''

year = '2013'

affiliation_table = {
    "GSL":"Graduate School of Law",
    "LS":"Law School",
    "Leading":"Leading Graduate School",
    "G30":"Global 30 Program"
}

from pathtool import gslpath
gp = gslpath()
import re,sys,os
from zipfile import ZipFile
from markdown import markdown

report_template = open(gp.docroot.src('course-report.html')).read()

class CourseReports:
    def __init__(self):
        for filename in os.listdir(gp.reports.src('')):
            if filename.endswith('.doc') or filename.endswith('.zip'):
                os.unlink(gp.reports.src(filename))

    def set(self,data,instructors):
        self.data = data
        self.report = report_template
        self.report = self.report.replace('@@course-title@@',self.data['course_title'])
        self.report = self.report.replace('@@open-to@@',self.data['open_to'])
        self.report = self.report.replace('@@credit@@',self.data['credit'])
        if str(data['term']) == "1":
            self.report = self.report.replace('@@term@@','Spring')
        elif str(data['term']) == "2":
            self.report = self.report.replace('@@term@@','Spring')
        else:
            self.report = self.report.replace('@@term@@','?????')
        self.report = self.report.replace('@@year@@',year)
        dtstr = self.data['day_and_time']
        dtlst = dtstr.split("(Mon|Tue|Wed|Thu|Fri)")
        lst = []
        for i in range(1,len(dtlst),2):
            lst.append(dtlst[i])
        days = ", ".join(lst)
        lst = []
        for i in range(2,len(dtlst),2):
            lst.append(dtlst[i])
        times = ", ".join(lst)
        self.report = self.report.replace('@@days@@',days)
        self.report = self.report.replace('@@times@@',times)
        self.report = self.report.replace('@@course-subject@@',data['course_subject'])
        self.report = self.report.replace('@@instructor@@',data['instructor'])
        if not data['instructor'] or data['instructor'].find('advisor') > -1 or data['instructor'].find('staff') > -1:
            affiliation = ''
        else:
            uid = data['instructor'].strip().replace(" ","_")
            if instructors.has_key(uid):
                affiliation = instructors[uid]['affiliation']
                if affiliation:
                    if affiliation in affiliation_table.keys():
                        affiliation = affiliation_table[affiliation]
                    affiliation = "(%s)" % affiliation
                else:
                    affiliation = '(external)'
            else:
                affiliation = '(external)'
        self.report = self.report.replace('@@affiliation@@',affiliation)

        course_objective = markdown(data['course_objective'])
        self.report = self.report.replace('@@course-objective@@',course_objective)
        
        evaluation = markdown(data['evaluation'])
        self.report = self.report.replace('@@evaluation@@',evaluation)

        prerequisites = markdown(data['prerequisites'])
        self.report = self.report.replace('@@prerequisites@@',prerequisites)

        textbooks = markdown(data['textbooks'])
        self.report = self.report.replace('@@textbooks@@',textbooks)

        notes = data['notes']
        notes = notes.replace("(?:sm)-- DO NOT EDIT BELOW THIS LINE --.*","")
        notes = markdown(notes)
        self.report = self.report.replace('@@notes@@',notes)

        self.report = self.report.replace('@@sessions@@',data['sessions'])

    def save(self):
        filename_html = 'rpt%s.html' % self.data['course_number']
        print "Saving: %s" % filename_html
        open(gp.reports.src(filename_html), 'w+').write(self.report)
        ofh = os.popen('lowriter --headless -convert-to doc -outdir %s %s' % (gp.reports.src(''),gp.reports.src(filename_html)))
        ofh.close()
        os.unlink(gp.reports.src(filename_html))

    def aggregate(self):
        zf = ZipFile(gp.reports.src('course-reports-%s.zip' % year), 'a')
        for filename in os.listdir(gp.reports.src('')):
            if filename.endswith('.doc'):
                print "Moving %s to zip archive" % filename
                zf.writestr(filename,open(gp.reports.src(filename)).read())
                os.unlink(gp.reports.src(filename))
        zf.close()

