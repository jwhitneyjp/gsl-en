#-*- encoding: utf8 -*-
''' Module

    Should use a pyconfig file to store category names and the strings 
    associated with each.
'''

from types import StringType
import os, re, sys
from ConfigParser import ConfigParser
from exceptions import Exception

class MissingStartException(Exception):
    pass

class MissingEndException(Exception):
    pass

class MissingPhraseException(Exception):
    def __init__(self, section):
        self.args = [section]

class MissingCategoryException(Exception):
    pass

class categoryHinter(ConfigParser):
    ''' Class to identify hints as to a category of expenditure.
    
        A single instance of this class is passed to each
	AmbiguousLine during processing, and stores the current hint
	for injection into individual AmbiguousCluster instances. The
	re attribute of this class provides a combined regexp that can
	be used to identify words for processing.  Use the addHint
	method to add categories and hints.  Categories are scanned in
	the order or storage, and can be augmented with additional
	strings for fine tuning.
    '''

    def __init__(self, *args):
        #
        # This  module works, but it's ugly, ugly, ugly
        #
        ConfigParser.__init__(self)
        self.initialize_vars()
        self.configInstall( args )
        self.read( self.file )
        self.validate()
        self.compile()

    def initialize_vars(self):
        self.hints_raw = []
        self.start_raw = []
        self.end_raw = []
        self.hints = []
        self.re = None
        self.re_start = None
        self.re_end = None
        self.current = 'Unknown'
        self.nontotal = 'Unknown'
        self.file = ''        

    def configInstall(self, args):
        user_dir = os.path.expanduser('~')
        user_config_dir = os.path.join( user_dir, '.nugsl-renumerate' )
        system_dir = os.path.join( sys.prefix, 'share', 'nugsl-renumerate', 'config' )
        if not os.path.exists( user_config_dir ):
            os.makedirs( user_config_dir )
        for file in os.listdir( system_dir ):
            user_config_file = os.path.join( user_config_dir, file )
            system_config_file = os.path.join( system_dir, file ) 
            if not os.path.exists( user_config_file ) \
               or ( file == 'finish.png' and os.stat(user_config_file).st_mtime < os.stat(system_config_file).st_mtime):
                system_config = open( system_config_file, 'rb', 0 ).read()
                open( user_config_file, 'wb+', 0 ).write( system_config )

        if args and os.path.exists( args[0] ):
            self.file = args[0]
        else:
            user_file = os.path.split( args[0] )[-1]
            if os.path.exists( os.path.join( user_config_dir, user_file ) ):
                self.file = os.path.join( user_config_dir, user_file )
            else:
                print '  ERROR: Category config file not found'
                sys.exit()

    def ordered_sections(self):
        config = open( self.file ).read()
        ret = [x for x in re.findall('(?m)(?s)^\[([^]]+)\]$', config) ]
        ret.remove('Start')
        ret.remove('End')
        ret.remove('Total')
        return ret + ['Unknown']

        
    def line_reset(self):
        self.current = self.nontotal
            
    def compile(self):
        for section in self.sections():
            options = self.options(section)
            options.sort()
            for option in options:
                if option.startswith('phrase'):
                    val = self.get(section, option).decode('utf8').strip()
                    self.addHint( section, val )
        self.re_start = '(?i)(%s)' % '|'.join( self.start_raw )
        self.re_end = '(?i)(%s)' % '|'.join( self.end_raw )

    def validate(self):
        sections = self.sections()
        if not 'Start' in sections:
            raise MissingStartException
        if not 'End' in sections:
            raise MissingEndException
        if len(sections) < 3:
            raise MissingCategoryException
        for section in sections:
            options = self.options( section )
            ok = False
            for option in options:
                if option.startswith('phrase'):
                    ok = True
            if not ok:
                raise MissingPhraseException(section)

    def addHint(self, category, r):
        if category == 'Start':
            self.start_raw.append( r )
        elif category == 'End':
            self.end_raw.append( r )
        elif category in [x[0] for x in self.hints_raw]:
            for hint in self.hints_raw:
                if hint[0] == category:
                    hint[1].append( r )
        else:
            self.hints_raw.append( [category, [r]] )
        self._setHints()

    def make_re(self, l):
        return '(?i)(?:%s)' % '|'.join( ['|'.join(x[1]) for x in l] )
        
    def _setHints(self):
        self.re = self.make_re( self.hints_raw )
        self.hints = []
        for hint in self.hints_raw:
            self.hints.append({'name': hint[0],'re': '(%s)' % '|'.join(hint[1]) })

    def classify(self, s ):
        for hint in self.hints:
            category = hint['name']
            if re.match( '(?i).*%s.*' % hint['re'], s ):
                self.current = category
                if category != 'Total':
                    self.nontotal = category
                return category
