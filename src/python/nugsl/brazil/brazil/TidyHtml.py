''' Module
'''

import tidy
import cStringIO

class tidyHtml:
    
    def __init__(self, s):

        options = dict(char_encoding='latin1',wrap=0,indent='auto')

        io = cStringIO.StringIO()
        
        tidier = tidy.parseString( s, **options)
        
        tidier.write(io)
        
        io.seek(0)
        
        self.html = io.read()
