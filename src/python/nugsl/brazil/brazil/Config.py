''' Module
'''

from ConfigParser import ConfigParser
import os, sys

class ConfigBase(ConfigParser):    
    def __init__(self):
        ConfigParser.__init__(self)
        self.initializeConfigDir()
    
    def initializeConfigDir(self):
        home = os.path.expanduser('~')
        config_dir = os.path.join( home, '.nugsl-brazil' )
        if not os.path.exists( config_dir ):
            os.makedirs( config_dir )
        self.config_dir = config_dir
        self.system_dir = os.path.sep + os.path.join( 'usr', 'share', 'nugsl-brazil' )


class headingsConfigBase(ConfigBase):
    def __init__(self, arg):
        ConfigBase.__init__(self)
        config_file = os.path.join( self.config_dir, 'headings-%s.conf' % arg)
        if not os.path.exists( config_file ):
            config = open( os.path.join( self.system_dir, 'headings-%s.conf' % arg) ).read()
            open( os.path.join( config_file ), 'w+' ).write( config )
        self.read( config_file )
        self.headings = {}
        for section in self.sections():
            for option in self.options(section):
                self.headings[ self.get(section, option) ] = section

class preConfig(headingsConfigBase):
    def __init__(self):
        headingsConfigBase.__init__(self, 'pre')

class postConfig(headingsConfigBase):
    def __init__(self):
        headingsConfigBase.__init__(self, 'post')

class brazilConfig(ConfigBase):
    
    def __init__(self):
        ConfigBase.__init__(self)
        config_file = os.path.join( self.config_dir, 'brazil.conf')
        system_file = os.path.join( self.system_dir, 'brazil-dist.conf' )
        if not os.path.exists( config_file ):
            config = open( system_file ).read()
            open( config_file, 'w+').write( config )
        self.read( config_file )
        
        if not self.has_section( 'Paths' ):
            print '  ERROR: No section [Paths] in config file %s' % config_file
            sys.exit()
        if not self.has_option( 'Paths', 'data-path' ):
            print '  ERROR: No option "data-path:" in section [Paths] of config file %s' % config_file
            sys.exit()
        self.data_path = self.get('Paths', 'data-path')
        if not os.path.exists( self.data_path ):
            print '  ERROR: Path %s does not exist.' % self.data_path
            print '  Check the path setting in the config file %s' % config_file
            sys.exit()
