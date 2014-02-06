'''
  Utility function for staff pages
'''

import sys

from pathtool import gslpath
gp = gslpath()

import sys,os,re

from csvtool import gslCsv

class staffIndexes:
    def __init__(self):        
        self.si_body = open( gp.docroot.src('si-body.html') ).read()
        self.si_row = open( gp.docroot.src('util-block.html') ).read().strip()
        self.si_profession = open( gp.docroot.src('util-profession.html') ).read()
        self.si_field = open( gp.docroot.src('util-field.html') ).read()
        self.si_tutorial_link = open( gp.docroot.src('si-tutorial-link.html') ).read()
        
        self.si_section = open( gp.docroot.src('util-section.html') ).read()
        
    def stafflist_init(self,faculty, byteaching=False, strict=False):
        if faculty == 'LS':
            self.page_title='Law School'
        elif faculty == 'G30':
            self.page_title='Global 30 Program'
        elif faculty == 'Leading':
            self.page_title='Leading Graduate School'
        else:
            self.page_title='Comparative Law'

        self.professors = []
        self.adjunct = []
        self.associate_professors = []
        self.assistant_professors = []
        for data in self.staffdata:
            if not byteaching:
                if not faculty in data['affiliations_raw']:
                    continue
            elif strict:
                if not self.coursesbystaffuid.has_key(data['uid']) or not self.coursesbystaffuid[data['uid']][faculty]:
                    continue
            else:
                if not faculty in data['affiliations_raw'] and (not self.coursesbystaffuid.has_key(data['uid']) or not self.coursesbystaffuid[data['uid']][faculty]):
                    continue
            data['other_affil'] = ''
            for a in data['affiliations_raw']:
                if a != faculty:
                    data['other_affil'] = 'Joint appointment with %s' %a      
            if data['profession']:
                self.adjunct.append(data)
            elif data['status'] == 'Professor':
                self.professors.append(data)
            elif data['status'] == 'Designated Professor':
                self.professors.append(data)
            elif data['status'] == 'Associate Professor':
                self.associate_professors.append(data)
            elif data['status'] == 'Designated Associate Professor':
                self.associate_professors.append(data)
            elif data['status'] == 'Assistant Professor':
                self.assistant_professors.append(data)
            elif data['status'] == 'Designated Assistant Professor':
                self.assistant_professors.append(data)

        
    def staffindexes(self):
        self.mkindex('GSL', byteaching=True, strict=True)
        self.mkindex('LS')
        self.mkindex('Leading', byteaching=True)
        self.mkindex('AW', byteaching=True)
        self.mkindex('G30')
        self.staffindex()
        
    def makerow(self,data):
        row = self.si_row
        row = row.replace('@@photo-url@@', data['photo_url'])        
        row = row.replace('@@profile-url@@', data['profile_url'])
        row = row.replace('@@profile-url-cached@@', data['profile_url_cached'])
        row = row.replace('@@full-name@@', data['full_name'])
        row = row.replace('@@status@@', data['status'])
        row = row.replace('@@affiliations@@', data['affiliations'])
        if data['tutorial_link']:
            tutorial_button = self.si_tutorial_link.replace('@@tutorial-link@@', data['tutorial_link'])
        else:
            tutorial_button = ''
        row = row.replace('@@tutorial-button@@', tutorial_button)
        
        if data['profession']:
            profession = self.si_profession
            profession = profession.replace('@@profession@@', data['profession'])
        else:
            profession = ''
        row = row.replace('@@profession@@', profession)

        if not data['profession'] and data['field']:
            field = self.si_field
            data_field = data['field'].replace('(','[')
            data_field = data_field.replace(')',']')
            data_field = "(%s)" % (data_field.strip(),)
            field = field.replace('@@field@@', data_field)
        else:
            field = ''
        row = row.replace('@@field@@', field)
        return row
        

    def staffindex(self):
        row_content = ''
        for data in self.staffdata:
            row = self.makerow(data)
            row_content += row
        body = self.si_body
        body = body.replace('@@rows@@', row_content)
        
        page = open( gp.faculty_index.release('index.html') ).read()
        page = re.sub('<p>.*?%%content%%.*?</p>','%%content%%',page)
        page = page.replace('%%content%%', body)
        open( gp.faculty_index.release('index.html'), 'w+' ).write(page)

    def stafflist_section(self,title,data):
        row_content = ''
        if data:
            section = self.si_section
            for d in data:
                row = self.makerow(d)
                row_content += row
            section = section.replace('@@blocks@@', row_content)
            section = section.replace('@@title@@',title)
        else:
            section = ''
        return section
        
    def mkindex(self, program, byteaching=False, strict=False):
        self.stafflist_init(program, byteaching=byteaching, strict=strict)
        section_content = ''
        section_content += self.stafflist_section('Professors',self.professors)
        section_content += self.stafflist_section('Adjunct Professors',self.adjunct)                
        section_content += self.stafflist_section('Associate Professors',self.associate_professors)
        section_content += self.stafflist_section('Assistant Professors',self.assistant_professors)
        
        body = self.si_body
        body = body.replace('@@rows@@',section_content)
        
        page = open( gp.faculty_index.release('staffof%s/index.html' % program.lower()) ).read()
        page = re.sub('<p>.*?%%content%%.*?</p>','%%content%%',page)
        page = page.replace('%%content%%', body)
        open( gp.faculty_index.release('staffof%s/index.html' % program.lower()), 'w+' ).write(page)
    
