''' Module
'''

from ConfigParser import ConfigParser
import os,sys

class renumerateConfig(ConfigParser):
    
    def __init__(self, argv):
        path = os.path.expanduser('~')
        path = os.path.join( path, '.nugsl-renumerate')
        if not os.path.exists( path ):
            os.makedirs( path )
        file = os.path.join( path, 'renumerate.conf' )
        if not os.path.exists( file ):
            default_file = os.path.join( sys.prefix, 'share', 'nugsl-renumerate', 'config', 'renumerate-default.conf')
            default = open( default_file ).read()
            open( file, 'w+' ).write( default )
        ConfigParser.__init__(self, {'CONFIG': path})
        self.read( file )
        if not 'Renumerate' in self.sections():
            print 'Missing section [Renumerate] in config file %s' % file
            sys.exit()
        elif not self.has_option('Renumerate','data-path'):
            print 'Missing option "data-path:" in section [Renumerate] of config file %s' % file
            sys.exit()
        elif not self.has_option('Renumerate','category-config'):
            print 'Missing option "category-config:" in section [Renumerate] of config file %s' % file
            sys.exit()
        elif not self.has_option('Renumerate','tess-config'):
            print 'Missing option "tess-config:" in section [Renumerate] of config file %s' % file
            sys.exit()

        if len(argv) > 1:
            self.data_path = os.path.join( self.get('Renumerate', 'data-path'), argv[1] )
            if not os.path.exists( self.data_path ):
                print '  ERROR: cannot find jurisdiction path: %s' % self.data_path
                print '  Is the jurisdiction ("%s") spelled correctly?' % argv[1]
                print '  Is the data path set correctly in %s?' % file
                sys.exit()
        else:
            print 'Please specify the jurisdiction directory name containing renumerate data files'
            sys.exit()

        self.category_config = self.get('Renumerate', 'category-config')
        self.tess_config = self.get('Renumerate', 'tess-config')
        self.config_file = file
        self.config_path = path
        self.raw_path = os.path.join( self.data_path, 'raw' )
        self.validated_path = os.path.join( self.data_path, 'validated' )
        self.discarded_path = os.path.join( self.data_path, 'discarded' )
