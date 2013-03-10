''' Module
'''

import re
from ConfigParser import ConfigParser
from nugsl.homedir import homeDir
import os,sys
from datetime import date
from PIL import Image
import ImageTk
from types import DictType, StringType
from exceptions import Exception
from nugsl.datetool import dateDelta
from cPickle import Unpickler, Pickler
from paramiko import SSHClient, AutoAddPolicy, RSAKey
from StringIO import StringIO

class monthConfig:

    def __init__(self, weekdays):
        self.weekdays = weekdays

    def set_month(self, date):
        self.firstweekday = dateDelta( date ).get_first_day().weekday()
        self.last_day = dateDelta( date ).get_last_day().day
        self.last_day_previous_month = dateDelta( dateDelta( date ).get_last_month() ).get_last_day().day
        self.last_day_next_month = dateDelta( dateDelta( date ).get_next_month() ).get_last_day().day
        self.key_engine = keyEngine( date )
        self.key_engine_prev = keyEngine( dateDelta( date ).get_last_month() )

    def get_keyinfo(self, pos):
        keyinfo = self.key_engine( pos, self.firstweekday )
        return keyinfo

    def get_wkeyinfo(self, pos):
        wkey_info = self.key_engine.wkey( pos )
        return wkey_info

    def get_hideme(self, pos, keyinfo):
        if pos < self.firstweekday:
            hideme = True
        elif pos  > self.firstweekday + self.last_day - 1:
            hideme = True
        elif  not self.weekdays.has_key( keyinfo.weekday ):
            hideme = True
        else:
            hideme = False
        return hideme

class keyEngine:
    def __init__(self, date):
        year = date.year
        month = date.month

        prev = dateDelta( date ).get_last_month()
        year_prev = prev.year
        month_prev = prev.month
        self.base_template = '%0.4d-%0.2d' % (year,month)
        self.prev_template = '%0.4d-%0.2d' % (year_prev,month_prev)

    def __call__(self, pos, firstweekday):
        day = pos - firstweekday
        dow = pos % 7
        key_base = self.base_template + '-%d-%0.2d'
        key_base = key_base % (dow,day)
        return keyInfo( key_base )

    def wkey(self, pos):
        """ Factory function to create a wkey generator for a weekday button
        """
        return wkeyInfo( self.base_template, self.prev_template, pos )

class wkeyInfo:
    def __init__(self, base_template, prev_template, pos):
        this_month_base = base_template + '-%d'
        last_month_base = prev_template + '-%d'
        self.last_month_wkey = last_month_base % pos
        self.this_month_wkey = this_month_base % pos
        self.day = pos

    def prev_time_key(self, daynum, time):
        template = self.last_month_wkey + '-%0.2d-%d'
        return template % (daynum, time)

    def current_time_key(self, daynum, time):
        template = self.this_month_wkey + '-%0.2d-%d'
        return template % (daynum, time)

    def last_month_first_weekday(self):
        year = int(self.last_month_wkey[:4])
        month = int(self.last_month_wkey[5:7])
        for day in range(1,8,1):
            d = date(year, month, day)
            if d.weekday() == self.day:
                return day - 1

class keyInfo:
    def __init__(self, key_base):
        self.key_base = key_base
        self.day = int(key_base[10:12])
        self.weekday = int(key_base[8:9])

    def get_time_key(self, pos):
        key = self.key_base + '-%d'
        return key % pos

class FreetimeKeyError(Exception):
    def __init__(self, key):
        self.msg = 'Key %s does not match pattern nnnn-nn-n-nn-n' % key

class myConfigParser(ConfigParser):
    
    def paranoid_read(self, filename):
        io = StringIO()
        text = open( filename ).read()
        try:
            text = text.decode('utf8')
        except:
            text = text.decode('shift_jis')
            print 'Barfed on file %s, using shift-jis encoding' % filename
        io.write( text )
        io.seek(0)
        self.readfp( io )

class freetimeConfig(myConfigParser):

    def __init__(self):
        self.error = None
        self.groups_pos = 0
        defaults_dir = os.path.join( sys.prefix, 'share', 'nugsl-freetime')
        path = homeDir( topdir='FreeTime' )
        path = os.path.join( path, 'FreeTime')
        if not os.path.exists( path ):
            os.makedirs( path )
        config_path = os.path.join( path, 'Config')
        if not os.path.exists( config_path ):
            os.makedirs( config_path )
        data_path = os.path.join( path, 'Calendars')
        if not os.path.exists( data_path ):
            os.makedirs( data_path )
        self.data_path = data_path
        self.category_path = {}
        p = os.path.join( data_path, 'Staff')
        if not os.path.exists( p ):
            os.makedirs( p )
        self.category_path[ 'Staff' ] = p
        p = os.path.join( data_path, 'Student')
        if not os.path.exists( p ):
            os.makedirs( p )
        self.category_path[ 'Student' ] = p
        config_file = os.path.join( config_path, 'profile.txt' )
        if not os.path.exists( config_file ):
            default_file = os.path.join( defaults_dir, 'profile-default.txt')
            default = open( default_file ).read()
            open( config_file, 'w+' ).write( default )
            self.error = 'Please edit your profile at %s.' % config_file
            return
        myConfigParser.__init__(self, {'language': 'en'})
        self.paranoid_read( config_file )

        if not 'User' in self.sections():
            self.error = 'Missing section [User] in config file %s' % config_file
            return
        elif not self.has_option('User','name'):
            self.error = 'Missing option "name:" in section [User] of config file %s' % config_file
            return
        elif not self.has_option('User','email'):
            self.error = 'Missing option "email:" in section [User] of config file %s' % config_file
            return
        elif not self.has_option('User','telephone'):
            self.error = 'Missing option "telephone:" in section [User] of config file %s' % config_file
            return

        lang = self.get('User','language')

        self.name = self.get('User', 'name')
        if self.name == 'Unknown User':
            self.error = 'Please edit your profile at %s.' % config_file
            return
        self.email = self.get('User', 'email')
        self.telephone = self.get('User', 'telephone')

        repeat_icon_file = os.path.join( defaults_dir, 'repeat.png')
        img = Image.open( repeat_icon_file, 'r' )
        self.repeat_icon = ImageTk.PhotoImage( img )

        empty_icon_file = os.path.join( defaults_dir, 'empty.png')
        img = Image.open( empty_icon_file, 'r' )
        self.empty_icon = ImageTk.PhotoImage( img )

        right_file =  os.path.join( defaults_dir, 'right.png')
        img = Image.open( right_file, 'r' )
        self.right = ImageTk.PhotoImage( img )

        left_file =  os.path.join( defaults_dir, 'left.png')
        img = Image.open( left_file, 'r' )
        self.left = ImageTk.PhotoImage( img )

        self.times = freetimeTimes( defaults_dir, lang=lang ).times
        self.weekdays = freetimeWeekdays( defaults_dir, lang=lang ).weekdays

        self.month = monthConfig( self.weekdays )

        userkey = userkeyConfig( defaults_dir, config_path )
        self.error = userkey.error
        if self.error:
            self.error = 'Please add your Freetime key to use the calendar.'
            return
        self.userkey = userkey.get('UserKey', 'userkey')
        if self.userkey == 'UnknownUser':
            self.error = 'Please add your Freetime key to use the calendar.'
            return
        self.category = userkey.get('UserKey', 'category')
        pkey = StringIO()
        pkey.write( userkey.get('UserKey','rsa').lstrip() )
        pkey.seek(0)
        self.pkey = RSAKey.from_private_key( pkey )
        self.server = userkey.get('UserKey', 'server')
        self.server_account = userkey.get('UserKey','account')

        groups_file = os.path.join( config_path, 'groups.txt' )
        if os.path.exists( groups_file ):
            text = open( groups_file ).read()
            try:
                text = text.decode('utf8')
            except:
                text = text.decode('shift_jis')
                print 'Barfed on groups file, using shift-jis encoding'
            self.groups = [x[1:-1] for x in re.findall('\[[^]]+\]'.decode('utf8'), text )]
        else:
            self.groups = []
        if self.groups:
            self.groups.insert(0, 'Personal')
        ##print self.groups
        #
        # Reconcile old group data and current groups configuration
        self.groups_data_file = os.path.join( config_path, 'groups.pkl' )
        if os.path.exists( self.groups_data_file ):
            ph = open( self.groups_data_file )
            self.groups_data = Unpickler( ph ).load()
            ph.close()
        else:
            self.groups_data = {}
        for key in self.groups_data.keys():
            if not key in self.groups:
                self.groups_data.pop(key)
        for group in self.groups:
            if not self.groups_data.has_key( group ):
                self.groups_data[ group ] = []

        self.build_user_info()

        self.known_hosts_file = os.path.join( defaults_dir, 'known_hosts')
        self.user_data_file = os.path.join( data_path, self.category, self.userkey )
        self.freetime = freeTime()


    def build_user_info(self):
        self.users = {'Staff': [], 'Student': []}
        today = date.today()
        self.user_index = {}
        for category in ['Staff','Student']:
            ids = os.listdir( self.category_path[ category ] )
            for userid in ids:
                userfile = os.path.join( self.category_path[ category ], userid )
                ph = open( userfile )
                try:
                    userdata = Unpickler( ph ).load()
                    doit = True
                except EOFError:
                    ph.close()
                    os.unlink( userfile )
                    doit = False
                if doit:
                    ph.close()
                    fullname = userdata[1].strip()
                    email = userdata[2].strip()
                    telephone = userdata[3].strip()
                    mtime = os.stat( userfile ).st_mtime
                    filedate = date.fromtimestamp( mtime )
                    delta = today - filedate
                    age = delta.days
                    self.users[ category ].append( (userid, fullname, email, telephone, age) )
            self.users[ category ].sort( self.sort_ids )
            for pos in range(0, len(self.users[ category ]),1):
                #
                # Ugly but effective.  We'll need a wrapper function to keep the
                # usage of this unified key straight.
                self.user_index[ category + '::' + self.users[ category][pos][0] ] = pos



    def sort_ids(self, a, b):
        a = a[0].split('_')[-1]
        b = b[0].split('_')[-1]
        if a > b:
            return 1
        elif a == b:
            return 0
        else:
            return -1

    def network_setup(self):
        dict = {}
        self.net_mtime = self.network_connect()
        if self.net_mtime != None:
            if os.path.exists( self.user_data_file ):
                self.network_update()
                local_mtime = int(os.stat( self.user_data_file ).st_mtime)
                if local_mtime > self.net_mtime:
                    self.network_upload()
                elif local_mtime < self.net_mtime:
                    self.network_download()
            else:
                self.network_download()
        if os.path.exists( self.user_data_file ):
            ph = open( self.user_data_file )
            dict = Unpickler( ph ).load()[-1]
        if not os.path.exists( self.user_data_file ) and self.net_mtime == None:
            ph = open( self.user_data_file, 'w+' )
            Pickler( ph ).dump( dict )
            ph.close()
            os.utime( self.user_data_file, (0,0) )
        last_month = dateDelta( date.today() ).get_last_month()
        keys = dict.keys()
        keys.sort()
        for key in keys:
            if key[:7] < '%0.4d-%0.2d' % (last_month.year,last_month.month):
                dict.pop( key )
            else:
                break
        self.freetime.update( dict )

    def groups_save(self):
        ph = open(self.groups_data_file, 'w+' )
        Pickler( ph ).dump( self.groups_data )
        ph.close()

    def network_connect(self):
        self.sshclient = SSHClient()
        self.sshclient.set_missing_host_key_policy(AutoAddPolicy)
        self.sshclient.load_host_keys( self.known_hosts_file  )
        try:
            self.sshclient.connect( self.server, username=self.server_account, pkey=self.pkey, timeout=20 )
        except:
            # Should have logging for this.
            self.sshclient.close()
            self.sshclient = None
            return None
        self.sftp = self.sshclient.open_sftp()
        if self.userkey in self.sftp.listdir( self.category ):
            return self.sftp.stat( self.category + '/' + self.userkey ).st_mtime
        else:
            return 0

    def network_close(self):
        if self.sshclient:
            self.sftp.close()
            self.sshclient.close()
        else:
            #
            # Setting the mtime to zero will force a merge, rather
            # than an overwrite, when the Net is next accessed.
            os.utime( self.user_data_file, (0,0))

    def network_upload(self):
        #if self.sshclient and self.userkey in self.sftp.listdir( self.category ):
        if self.sshclient and self.userkey in os.listdir( os.path.join( self.data_path, self.category ) ):
            self.sftp.put( self.user_data_file, self.category + '/' + self.userkey )
            mtime = self.sftp.stat( self.category + '/' + self.userkey ).st_mtime
            os.utime( self.user_data_file, (mtime,mtime) )

    def network_download(self):
        if self.sshclient and self.userkey in self.sftp.listdir( self.category ):
            self.sftp.get( self.category + '/' + self.userkey, self.user_data_file )
            mtime = self.sftp.stat( self.category + '/' + self.userkey ).st_mtime
            os.utime( self.user_data_file, (mtime,mtime) )
    #
    # The mtime of the local file is held at zero until
    # the first network connection from this instance.
    # If the local mtime is zero when network is available,
    # update from the server rather than overwriting, to
    # avoid losing data.
    def network_update(self):
        #
        # We have network, we have local file, we may not have
        # remote file.
        if self.userkey in self.sftp.listdir( self.category ):
            local_mtime = os.stat( self.user_data_file ).st_mtime
            if int(local_mtime) == 0:
                self.sftp.get( self.category + '/' + self.userkey, self.user_data_file + '.tmp' )
                ph = open( self.user_data_file + '.tmp' )
                net_data = Unpickler( ph ).load()[-1]
                ph.close()
                os.unlink( self.user_data_file + '.tmp' )

                ph = open( self.user_data_file )
                local_data = Unpickler( ph ).load()[-1]
                ph.close()

                local_data.update( net_data )
                self.freetime = freeTime( dict=local_data )

                ph = open( self.user_data_file, 'w+' )
                Pickler( ph ).dump( self.bundle_data() )
                ph.close()
        else:
            self.sftp.put( self.user_data_file, self.category + '/' + self.userkey )
            mtime = self.sftp.stat( self.category + '/' + self.userkey ).st_mtime
            os.utime( self.user_data_file, (mtime,mtime) )

    def network_update_others(self, category):
        """ Download files of other users for use in coordinating group schedules
        """
        for file in self.sftp.listdir( category ):
            if category == self.category and file == self.userkey:
                continue
            self.sftp.get( category + '/' + file, os.path.join( self.data_path, category, file ) )
            mtime = self.sftp.stat( category + '/' + file ).st_mtime
            os.utime( os.path.join( self.data_path, category, file ), (mtime,mtime) )
            self.build_user_info()

    def bundle_data(self):
        bundle = []
        bundle.append( self.userkey )
        bundle.append( self.name )
        bundle.append( self.email )
        bundle.append( self.telephone )
        bundle.append( self.freetime.copy() )
        return bundle

class userkeyConfig(myConfigParser):
    def __init__(self, defaults_dir, config_path ):
        myConfigParser.__init__(self)
        self.error = None
        config_file = os.path.join( config_path, 'userkey.cnf' )
        if not os.path.exists( config_file ):
            self.error = 'Please add your Freetime key to use the calendar.'
            return
        self.paranoid_read( config_file )
        if not 'UserKey' in self.sections():
            self.error ='Missing section [UserKey] in config file %s' % config_file
            return
        elif not self.has_option('UserKey','userkey'):
            self.error = 'Missing option "userkey:" in section [UserKey] of config file %s' % config_file
            return
        elif not self.has_option('UserKey','server'):
            self.error = 'Missing option "server:" in section [UserKey] of config file %s' % config_file
            return
        elif not self.has_option('UserKey','account'):
            self.error = 'Missing option "account:" in section [UserKey] of config file %s' % config_file
            return
        elif not self.has_option('UserKey','category'):
            self.error = 'Missing option "category:" in section [UserKey] of config file %s' % config_file
            return
        elif not self.get('UserKey','category') in ['Staff','Student']:
            self.error = 'Option "category:" in section [UserKey] of config file %s must be either Student or Staff' % config_file
            return
        elif not self.has_option('UserKey','rsa'):
            self.error = 'Missing option "rsa:" in section [UserKey] of config file %s' % config_file
            return

class WeekdaysConfigError(Exception):
    pass

class freetimeWeekdays(myConfigParser):

    def __init__(self, path, lang=None):
        myConfigParser.__init__(self, {'padx': '2' } )
        weekdays_file = os.path.join( path, 'weekdays-%s.txt' % lang )
        if not os.path.exists( weekdays_file ):
            weekdays_file = os.path.join( path, 'weekdays-c.txt' )
        if not os.path.exists( weekdays_file ):
            raise WeekdaysConfigError
        self.paranoid_read( weekdays_file )
        weekdays = {}
        sections = [x[1:-1] for x in re.findall('\[[^]]+\]', open( weekdays_file ).read())]
        for section in sections:
            if not section.isdigit():
                raise WeekdaysConfigError
            if not 'name' in self.options( section ):
                raise WeekdaysConfigError
            weekdays[int(section)]= self.get(section, 'name')
        self.weekdays = weekdays

class TimesConfigError(Exception):
    pass

class freetimeTimes(myConfigParser):

    def __init__(self, path, lang=None):
        myConfigParser.__init__(self, {'columnspan': '1'} )
        times_file = os.path.join( path, 'times-%s.txt' % lang )
        if not os.path.exists( times_file ):
            times_file = os.path.join( path, 'times-c.txt' )
        if not os.path.exists( times_file ):
            crash
        self.paranoid_read( times_file )
        times = []
        sections = [x[1:-1] for x in re.findall('\[[^]]+\]', open( times_file ).read())]
        for section in sections:
            if not 'row' in self.options( section ):
                raise TimesConfigError
            if not 'column' in self.options( section ):
                raise TimesConfigError
            times.append( (section, self.get(section,'row'), self.get(section,'column'), self.get(section,'columnspan') ) )
        self.times = times

class freeTime(DictType):

    def __init__(self, dict={}):
        ##
        ## XXXX To get better compatibility across systems and versions, this should
        ## export a standard dict type for pickling.
        ##
        self.update( dict )

    def __getitem__(self, key):
        if self.has_key( key ):
            return DictType.__getitem__(self, key)
        elif len(key) == 9:
            return ([],[])
        else:
            return None

    def clone_write(self, keys, setting):
        for key in keys:
            self.__setitem__(key, setting, sync=False)

    def clone_unwrite(self, weekday_key, keys ):
        for key in keys:
            if self.has_key( key ):
                self.__delitem__( key, sync=False )
        for key in self.__getitem__(weekday_key)[0]:
            self.__setitem__(key, 0 )

    def __setitem__(self, key, value, sync=True):
        if not len(key) == 14:
            raise FreetimeKeyError(key)
        if not key[0:4].isdigit():
            raise FreetimeKeyError(key)
        if not key[5:7].isdigit():
            raise FreetimeKeyError(key)
        if not key[8:9].isdigit():
            raise FreetimeKeyError(key)
        if not key[10:12].isdigit():
            raise FreetimeKeyError(key)
        if not key[13:14].isdigit():
            raise FreetimeKeyError(key)
        #
        # Maintain a list of all repeatable entries for a particular year, month
        # and weekday
        daykey = key[:9]
        if not self.has_key( daykey ):
            DictType.__setitem__( self, daykey, ([],[]) )
        daykeys = self.__getitem__( daykey )
        keyvals = [0,1]
        for keyval in keyvals:
            if value == keyval:
                if not key in daykeys[keyval]:
                    daykeys[keyval].append( key )
            elif sync:
                if key in daykeys[keyval]:
                    daykeys[keyval].remove( key )
        #print daykeys
        return DictType.__setitem__(self, key, value)

    def __delitem__(self, key, sync=True):
        daykey = key[:9]
        daykeys= self.__getitem__( daykey )
        if sync:
            if key in daykeys[0]:
                daykeys[0].remove( key )
        if key in daykeys[1]:
            daykeys[1].remove( key )
        #print daykeys
        return DictType.__delitem__( self, key )

    def pop(self, key, *defaults):
        if len(defaults) > 1:
            raise TypeError, "pop expected at most 2 arguments, got %d" % (1 + len(defaults))
        try:
            v = DictType.__getitem__(self, key)
            self.__delitem__(key)
        except KeyError, e:
            if defaults:
                return defaults[0]
            else:
                raise e
        return v
