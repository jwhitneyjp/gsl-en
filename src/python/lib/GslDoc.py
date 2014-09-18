#!/usr/bin/env python

from PIL import Image
import os,sys,re,urllib
from os.path import basename, isdir
from pathtool import gslpath
p = gslpath()

import pexif
from markdown import markdown

class gslDocDir:

    def __init__(self, po ):

        os.path.walk( po.src(''), self.move, po )
        
    def move(self, po, dirname, fnames ):
        if '.svn' in fnames:
            fnames.remove('.svn')
        dirname = dirname + '/'
        releasepath = dirname[len(po.src('')):]
        releasepath = po.release('') + releasepath
        try:
            os.makedirs(releasepath)
        except:
            pass
        ## Evil in the obscure!
        #try:
        #    index = open( releasepath + 'index.html').read()
        #    index = re.sub("indexpage-pagecontent","infopage",index)
        #    open( releasepath + 'index.html','w').write(index)
        #except:
        #    print 'Warning: no index.html in %s' %releasepath
        for filename in fnames:
            # fix up index file
            ext = filename.lower()[-4:]
            if ext in ['.doc','.pdf','.xls','.ppt', '.zip'] and not isdir( dirname + filename ):
                open( releasepath + filename, 'w' ).write( open( dirname + filename ).read())
        
