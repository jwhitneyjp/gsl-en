'''
  Simple utility for merging OpenOffice writer documents
'''

import sys,re,os
from zipfile import ZipFile

rex1 = re.compile('(.*</text:sequence-decls>)(.*)(</office:text>.*)',re.M|re.S)
rex2 = re.compile('(.*)<text:p [^<>]*/>$')


class mergeTool:
    
    def __init__(self,name):
        ''' Instantiates an ordinary OOWriter file as a merge
            template.  File <name>_template.odt must exist
            under share/nugsl-mergetool/templates.
        '''
        self.name = name
        user_dir = os.path.expanduser('~')
        template_dir = os.path.join( user_dir, '.nugsl-mergetool' )
        template = name + '_template.odt'
        self.template_path = os.path.join( template_dir, template )
        if not os.path.exists( template_dir ):
            os.makedirs( template_dir )
        if not os.path.exists( self.template_path ):
            master_template = os.path.join( '%s', 'share', 'nugsl-mergetool', 'templates', '%s_template.odt' )
            master_template = master_template % ( sys.prefix, self.name )
            t = open( master_template ).read()
            open( self.template_path, 'w+' ).write( t )

    def merge(self,data):
        ''' Accepts a list of maps as DATA, performs substitutions
            in the OOWriter file given as template, and writes the 
            result to the base filename of the instantiated template.
            Substitution texts should correspond to keys in DATA,
            and be delimited with @@...@@.  For example, the value
            of the key "name" will replace the text "@@name@@"
            in the OOWriter file used as the template.  Templates
            are written to an .nugsl-mergetool/ subdirectory in the
            user home directory if they do not exist.  Customize
            the user copy of the template to customize the output.
        '''
        self.data = data
        self._get_template()
        self._generate_body()
        self._write_file()

    def _get_template(self):
        z = ZipFile( self.template_path )
        text = z.read('content.xml')
        z.close()
        r = rex1.match( text )
        if not r:
            print 'No go'
            sys.exit()
        self.head = r.group(1).strip()
        self.body = r.group(2).strip()
        r2 = rex2.match( self.body )
        if r2:
            self.body = r2.group(1).strip()
        self.foot = r.group(3).strip()

    def _generate_body(self):
        fullbody = ''
        for d in self.data:
            newbody = self.body
            for key in d.keys():
                placeholder = '{%s}' % key
                newbody = newbody.replace(placeholder, str(d[key]).replace('&','&amp;'))
            fullbody += newbody
        self.body = fullbody

    def _write_file(self):
        filename = '%s.odt' % self.name
        content = self.head + self.body + self.foot
        odt = open( self.template_path ).read()
        open(filename,'w').write(odt)
        z = ZipFile(filename,'a')
        z.writestr('content.xml', content)
        z.close()

