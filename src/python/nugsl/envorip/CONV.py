#!/usr/bin/python

import libxml2

from cStringIO import StringIO

text = open('ERRORS.html').read()

text = text.decode('Shift-JIS')
text = text.encode('UTF8')

io = StringIO()

io.write( text )
io.seek(0)
text = io.read()
io.close()

doc = libxml2.htmlParseDoc(text,'UTF-8')
