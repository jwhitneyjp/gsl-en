#!/usr/bin/env python
'''
Path utilities.  Basedir is the lowest-level directory
above 'src' in the specified path that also contains 'qam'.
Path nicknames are objects, with "src", "release" attributes,
and "web" and "fs" methods.  Running this file directly
will display the result of every registered path command.

The "release" method creates directories in its path as
required.

Sample usage
  p = gslpath()
  p.basedir
  p.photo.src
  p.photo.release("MyAmazingPage.html")
  p.photo.web("MyAmazingPage.html")
  p.photo.fs("MyAmazingPage.html")
'''

import sys,os,urllib
from os.path import *

class gslpath:

    def __init__(self):
        #
        # Find base directory
        self._basedir = self._basedir()
        #
        # Set paths
        self._paths = {}

        self._paths['docroot'] = {}
        self._paths['docroot']['src'] = 'src/docroot/'
        self._paths['docroot']['release'] = 'release/docroot/'

        self._paths['docrootdocroot'] = {}
        self._paths['docrootdocroot']['src'] = 'src/docroot/docroot/'
        self._paths['docrootdocroot']['release'] = 'release/docroot/'
        
        self._paths['info'] = {}
        self._paths['info']['src'] = 'src/docroot/info/'
        self._paths['info']['release'] = 'release/docroot/'
        
        self._paths['photo'] = {}
        self._paths['photo']['src'] = 'src/docroot/info/materials/photo/'
        self._paths['photo']['release'] = 'release/docroot/materials/photo/'
        
        self._paths['graphic'] = {}
        self._paths['graphic']['src'] = 'src/docroot/info/materials/graphic/'
        self._paths['graphic']['release'] = 'release/docroot/materials/graphic/'
        
        self._paths['reports'] = {}
        self._paths['reports']['src'] = 'src/docroot/info/appendix/reports/'
        self._paths['reports']['release'] = None
        
        self._paths['calendar'] = {}
        self._paths['calendar']['src'] = 'src/docroot/info/appendix/calendar/'
        self._paths['calendar']['release'] = 'release/docroot/appendix/calendar/'
        
        self._paths['faculty_index'] = {}
        self._paths['faculty_index']['src'] = 'src/docroot/info/faculty/'
        self._paths['faculty_index']['release'] = 'release/docroot/faculty/'
        
        self._paths['faculty'] = {}
        self._paths['faculty']['src'] = 'src/docroot/info/faculty/'
        self._paths['faculty']['release'] = 'release/docroot/faculty/member/'
        
        self._paths['facultycache'] = {}
        self._paths['facultycache']['src'] = 'src/docroot/info/faculty/'
        self._paths['facultycache']['release'] = 'release/docroot/faculty/cache/'
        
        self._paths['courses_index'] = {}
        self._paths['courses_index']['src'] = 'src/docroot/info/curriculum/'
        self._paths['courses_index']['release'] = 'release/docroot/curriculum/'
        
        self._paths['courses'] = {}
        self._paths['courses']['src'] = 'build/gsl/curriculum/syllabus/'
        self._paths['courses']['release'] = 'release/docroot/curriculum/syllabus/'
        
        self._paths['coursescache'] = {}
        self._paths['coursescache']['src'] = 'build/gsl/curriculum/syllabus/'
        self._paths['coursescache']['release'] = 'release/docroot/curriculum/cache/'
        
        self._paths['pylib'] = {}
        self._paths['pylib']['src'] = 'src/python/lib/'
        self._paths['pylib']['release'] = 'release/lib/python/'
        
        self._paths['csv'] = {}
        self._paths['csv']['src'] = 'src/docroot/csv/'
        self._paths['csv']['release'] = None
        
        self._paths['ics'] = {}
        self._paths['ics']['src'] = 'src/docroot/ics/'
        self._paths['ics']['release'] = 'release/docroot/ics/'
        
        self._paths['xls'] = {}
        self._paths['xls']['src'] = 'src/docroot/xls/'
        self._paths['xls']['release'] = None
        
        self._paths['pickle'] = {}
        self._paths['pickle']['src'] = 'src/docroot/pickle/'
        self._paths['pickle']['release'] = None
        
        self._paths['staffinfo'] = {}
        self._paths['staffinfo']['src'] = 'src/docroot/StaffInfo/'
        self._paths['staffinfo']['release'] = None
        
        self._paths['pyblosxom'] = {}
        self._paths['pyblosxom']['src'] = 'src/pyblosxom/content/plugins/'
        self._paths['pyblosxom']['release'] = None
        
        #
        # Instantiate path objects
        for name in self._paths.keys():
            docroot = self._paths['docroot']['release']
            src = self._paths[name]['src']
            release = self._paths[name]['release']
            source = 'self.%s = self._path("%s", "%s", "%s","%s")' % (name, self._basedir, docroot, src, release)
            exec(source)
        
        
    def _basedir (self):
        return self._acquireDir('src','src')
        
    def _acquireDir (self, anchor, companion):
        anchor = '/%s/' % anchor.strip('/')
        companion = companion.strip('/')
        execdir = dirname(realpath(sys.argv[0]))
        pos = len(execdir)
        while 1:
            pos = execdir.rfind(anchor)
            if pos == -1:
                raise "Unable to find base directory!"
            path = normpath(execdir[:pos]) + '/'
            if not companion in os.listdir(path):
                pos = pos - 4
            else:
                return path
            
    class _path:
        def __init__(self, basedir, docroot, src, release):
            self._basedir = basedir
            self.release_docroot = basedir + docroot
            self.srcpath = basedir + src
            if release:
                self.rel = basedir + release
            else:
                self.rel = None
            self.addedpath = ""

        def release(self, suffix):
            if not self.rel:
                return None
            path = self.rel + self.addedpath + suffix
            dirpath = '/'.join(path.split('/')[:-1])
            try:
                os.makedirs( dirpath )
            except:
                pass
            return path
            
        def src(self, suffix):
            path = self.srcpath + self.addedpath + suffix
            dirpath = '/'.join(path.split('/')[:-1])
            try:
                os.makedirs( dirpath )
            except:
                pass
            return path
            
        def url(self, suffix):
            #
            # normalize
            if not self.rel:
                return None
            if suffix.startswith( self.release_docroot ):
                path = suffix
            else:
                path = self.release(suffix)
            return urllib.quote( path[ len(self.release_docroot)-1 :] )
    
        def furl(self, suffix):
            path = urllib.quote(self.srcpath + self.addedpath + suffix)
            return 'file://' + path
        
if __name__ == '__main__':
    p = gslpath()
    keys = p._paths.keys()
    keys.sort()
    print 'Path nicknames for p = gslpath()'
    print ''
    for key in keys:
        exec('src = p.%s.src("")' % key)
        exec('release = p.%s.release("/pathtest/xx.html")' % key)
        exec('url = p.%s.url("xx.html")' % key)
        exec('furl = p.%s.furl("xx.html")' % key)
        print '%s' % key
        print '  p.%s.src("")' % key
        print '    %s' % src
        print '  p.%s.release("/pathtest/xx.html")' % key
        print '    %s' % release
        print '  p.%s.url("xx.html")' % key
        print '    %s' % url
        print '  p.%s.furl("xx.html")' % key
        print '    %s' % furl
        
