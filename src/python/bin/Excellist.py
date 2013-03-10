# -*- coding: utf-8 -*-
'''
  Convenience module for writing formatted courses.xls file
'''

from pyExcelerator import XFStyle,Font,Alignment,Borders,Pattern

class formatter:
    
    def __init__(self,worksheet):
        self.field_codes = {}
        self.field_code_count = 0
        self.row = 0
        self.hstyle = None
        self.rstyle = None
        self.cstyle = None
        self.ws = worksheet
        self.field_list = []

    def set_field_codes(self,codes):
        ''' CODES is a tuple of field code string and label,
            or a list of such tuples.
        '''
        if type(codes) == type((0,1)):
            self.field_codes[codes[0]] = (codes[1],self.field_code_count,codes[2])
            self.field_code_count = self.field_code_count + 1
            self.field_list.append(codes[0])
        else:
            for code in codes:
                self.field_codes[code[0]] = (code[1],self.field_code_count,code[2])
                self.field_code_count = self.field_code_count + 1
                self.field_list.append(code[0])
                
    def writemap(self,value_map):
        for v in value_map.keys():
            mycol = self.field_codes[v][1]
            myval = value_map[v]
            self.ws.write(self.row,mycol,myval,self.rstyle)
        self.row = self.row + 1

    def setup_courses_worksheet(self,keys_and_labels=None):
        h = []
        h.append(('course_number','Course no.',3000))
        h.append(('offered_this_year','Offered this year',3000))
        h.append(('course_subject','Course subject',6000))
        h.append(('course_title','Course title',6000))
        h.append(('instructor','Instructor',3000))
        h.append(('other_instructors','Other Instructors',4000))
        h.append(('format','Course format',3000))
        h.append(('term','Term offered',3000))
        h.append(('open_to','Student cohort',3000))
        h.append(('day_and_time','Day and time',3000))
        h.append(('credit','Credit',3000))
        h.append(('compulsory','Compulsory',3000))
        h.append(('room','Room',3000))
        h.append(('start_date','Start date',4000))
        h.append(('course_outline','Course outline',18000))
        h.append(('course_objective','Course objective',9000))
        h.append(('textbooks','Textbooks',6000))
        h.append(('references','Reference materials',6000))
        h.append(('evaluation','Evaluation methods',6000))
        h.append(('prerequisites','Prerequisites',5000))
        h.append(('notes','Notes',5000))
        h.append(('ss_code','SS Code',3000))
        h.append(('year_offered','Year offered',3000))
        h.append(('sessions','Sessions',6000))
        
        self.set_field_codes(h)

        # Set column widths
        for key in self.field_codes.keys():
            pos = self.field_codes[key][1]
            width = self.field_codes[key][2]
            self.ws.col(pos).width = width
            
        # Line wrapping
        align = Alignment()
        align.wrap = Alignment.WRAP_AT_RIGHT
        align.vert = Alignment.VERT_TOP
        
        # A boldface font
        hfont = Font()
        hfont.bold = True
        hfont.colour_index = 141

        # Heading style
        self.hstyle = XFStyle()
        self.hstyle.num_format_str = '@'
        self.hstyle.alignment = align
        self.hstyle.font = hfont
        
        # Write in heading
        for key in self.field_codes.keys():
            mycol = self.field_codes[key][1]
            mydata = self.field_codes[key][0]
            self.ws.write(self.row,mycol,mydata,self.hstyle)
        self.row = self.row + 1
            
        # Code style
        self.cstyle = XFStyle()
        self.cstyle.num_format_str = '@'
        self.hstyle.alignment = align
        
        # Write in codes
        for key in self.field_codes.keys():
            mycol = self.field_codes[key][1]
            self.ws.write(self.row,mycol,key,self.cstyle)
        self.row = self.row + 1

        # Data cell style
        self.rstyle = XFStyle()
        self.rstyle.num_format_str = '@'
        self.rstyle.alignment = align

    def setup_instructors_worksheet(self,keys_and_labels):
        h = []
        h.append(('uid','UID',2500))
        h.append(('status','Status',2500))
        h.append(('profession','Profession',2500))
        h.append(('family_name','Family name',2500))
        h.append(('given_name','Given name',2500))
        h.append(('proper_name','Proper name',2500))
        h.append(('birthdate','Birthdate (未公開)'.decode('utf8'),3000))
        h.append(('field','Field',3000))
        h.append(('affiliation','Affiliation',2500))
        h.append(('phone','Phone',2500))
        h.append(('office','Office',2500))
        h.append(('office_hours','Office hours',6000))
        h.append(('email','email (未公開)'.decode('utf8'),4000))
        h.append(('recommended_readings','Recommended readings',6000))
        h.append(('preparation_suggestions','Preparation suggestions for prospective applicants',6000))
        h.append(('website','Website',3000))
        h.append(('degrees','Degrees',6000))
        h.append(('research_interests','Research interests',6000))
        h.append(('memberships','Memberships',6000))
        h.append(('Jmemberships','所属学会\n(日本語サイトより)'.decode('utf8'),6000))
        h.append(('publications','Publications',12000))
        h.append(('Jpublications','主要著作\n(日本語サイトより)'.decode('utf8'),12000))
        h.append(('subjects','Subject areas',6000))
        h.append(('career_history','Career history',9000))
        h.append(('Jcareer_history','略歴\n(日本語サイトより)'.decode('utf8'),9000))
        h.append(('visitorships','Visitorships',6000))

        # Jesus, what a mess
        for key,label in keys_and_labels:
            width = 3000
            for x in h:
                if x[0] == key:
                    width = x[2]
            self.set_field_codes((key,label,width))
        
        # Set column widths
        for key in self.field_codes.keys():
            pos = self.field_codes[key][1]
            width = self.field_codes[key][2]
            self.ws.col(pos).width = width
            
        # Line wrapping
        align = Alignment()
        align.wrap = Alignment.WRAP_AT_RIGHT
        align.vert = Alignment.VERT_TOP
        
        # A boldface font
        hfont = Font()
        hfont.bold = True
        hfont.colour_index = 140
        hpat = Pattern()
        hpat.pattern_fore_colour = 140
        hpat.pattern = Pattern.SOLID_PATTERN

        # Heading style
        self.hstyle = XFStyle()
        self.hstyle.num_format_str = '@'
        self.hstyle.alignment = align
        self.hstyle.font = hfont
        self.hstyle.pattern = hpat
        
        # Write in heading
        for key in self.field_codes.keys():
            mycol = self.field_codes[key][1]
            mydata = self.field_codes[key][0]
            self.ws.write(self.row,mycol,mydata,self.hstyle)
        self.row = self.row + 1
            
        # Code style
        self.cstyle = XFStyle()
        self.cstyle.num_format_str = '@'
        self.hstyle.alignment = align
        
        # Write in codes
        for key in self.field_codes.keys():
            mycol = self.field_codes[key][1]
            self.ws.write(self.row,mycol,key,self.cstyle)
        self.row = self.row + 1

        # Data cell style
        self.rstyle = XFStyle()
        self.rstyle.num_format_str = '@'
        self.rstyle.alignment = align

    def setup_timetable_worksheet(self,title,base_offsets,maxcells):
        h1 = []
        h2 = []
        h1.append(title)
        h2.extend(['Monday','Tuesday','Wednesday','Thursday','Friday'])
        labels = ['1st period','2nd period','3rd period','4th period','5th period']
        
        times = ['(8:45 - 10:15)','(10:30 - 12:00)','(13:00 - 14:30)','(14:45 - 16:15)','(16:30 - 18:00)']

        h1Style = XFStyle()
        
        font = Font()
        font.height = 300
        font.bold = True
        
        align = Alignment()
        align.horz = Alignment.HORZ_CENTER
        
        h1Style.font = font
        h1Style.alignment = align
        
        h2Style = XFStyle()
        align = Alignment()
        align.rota = 30
        align.horz = Alignment.HORZ_CENTER
        align.vert = Alignment.VERT_CENTER
        h2Style.alignment = align

        borders = Borders()
        borders.bottom = Borders.THIN
        h2Style.borders = borders        
        
        labelStyle = XFStyle()
        borders = Borders()
        borders.bottom = Borders.THIN
        borders.top = Borders.THIN
        borders.left = Borders.THIN
        borders.right = Borders.THIN
        labelStyle.borders = borders
        
        align = Alignment()
        align.rota = 90
        align.horz = Alignment.HORZ_CENTER
        align.vert = Alignment.VERT_CENTER
        labelStyle.alignment = align
            


        self.ws.write_merge(0,0,0,5,title,h1Style)
        
        for pos in range (0,5,1):
            self.ws.write(1,pos+1,h2[pos],h2Style)
        self.ws.write(1,0,'',h2Style)
        for pos in range(0,5,1):
            base_offset = base_offsets[pos]
            offset = maxcells[pos]

            for r in range(2+base_offset,2+base_offset+offset,1):
                row = self.ws.row(r)
                row.height = 5000/offset
                #row.has_default_height = False
            
            text = '%s\n%s' % (labels[pos],times[pos])
            print "base_offset: %d" % (base_offset,)
            print "offset: %d" % (offset,)
            self.ws.write_merge(2+base_offset,2+base_offset+offset-1,0,1,text,labelStyle)
            #self.ws.write_merge(2+base_offset,2+base_offset+offset,0,0,text,labelStyle)

        self.ws.col(0).width = 1200
        for pos in range(1,6,1):    
            self.ws.col(pos).width = 5500

        #self.ws.row(10).has_default_height = False
        self.ws.row(10).height = 400
        
