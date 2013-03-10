#!/usr/bin/env python

import os,sys,re,urllib,Image
from os.path import basename
from pathtool import gslpath
p = gslpath()

import pexif
from markdown import markdown

class gslPhotoDir:

    def __init__(self, po ):

        self.po = po
        
        files = os.listdir( self.po.src('') )
        
        files.sort()
        
        for filename in files:
            ext = os.path.splitext(filename)[1].lower()
            if ext in ['.png', '.jpg']:
                if ext == '.jpg':
                    img = processImage( filename, self.po )
                else:
                    img = processImage( filename, self.po, jpeg=False )

class processImage:
    def __init__(self, filename, po, maxwidth=400, jpeg=True ):
        self.po = po
        self.maxwidth = maxwidth
        self.filename = filename
        self.subtext = {}
        self.shrink_and_release()

    def shrink_and_release(self):
        filepath = self.po.src(self.filename)
        targetpath = self.po.release( self.filename )
        img = Image.open( filepath )
        width, height = img.size
        if width > self.maxwidth:
            height = int(height * (float(self.maxwidth) / float(width)))
            out = img.resize( ( self.maxwidth, height ) )
        else:
            out = img
        if os.path.exists( targetpath ):
            os.unlink( targetpath )
        out.save( targetpath )

