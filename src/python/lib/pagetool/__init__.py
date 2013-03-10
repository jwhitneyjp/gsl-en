'''
hello
'''

from CoursePages import coursePages
from StaffPages import staffPages

from CourseIndex import courseIndex
from StaffIndexes import staffIndexes

from StaffData import getStaffData
from csvtool import gslCsv

from CourseReports import CourseReports

from pathtool import gslpath
gp = gslpath()



class pageEngine(coursePages,staffPages,courseIndex,staffIndexes):
    def __init__(self,instructors_csv):
        
        self.fh = open( gp.csv.src(instructors_csv) )
        self.instructor_data = gslCsv( self.fh, offset=0 )

        coursePages.__init__(self)
        staffPages.__init__(self)

        courseIndex.__init__(self)
        staffIndexes.__init__(self)

        self.popup_template = open( gp.docroot.src( 'popup-template.html') ).read()
        self.taughtby = {}
        self.coursename = {}
        self.courses = []

        self.instructorlist = []
        self.instructor_names = {}
        
        fh = open( gp.csv.src(instructors_csv) )
        c = gslCsv( fh, offset=0 )        
        self.staffdata = getStaffData(c,self.taughtby,gp.faculty.release(""))
        fh.close()
        
        fh = open( gp.csv.src(instructors_csv) )
        c = gslCsv( fh, offset=0 )        
        for data in c:
            self.instructorlist.append( data['uid'] )
            self.instructor_names[ data['uid'] ] = '%s %s' % (data['given_name'], data['family_name'])
        fh.close()

