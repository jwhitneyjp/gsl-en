"""
Summary
=======

This plugin implements news item listings for a subset of Pyblosxom
post categories, suitable for display on a landing page. It is
compatible with the pages plugin, and has simple support for
prepublication preview of news content.

There are several elements to the magic.


**Set date from filename** (cb_filestat)

For entry source files that begin with a yyyy-mm-dd string, set the
date of the post from the filename, overriding the mtime value.

This works out nicely for keeping posts organized in a filesystem
view, and requires less overhead than extracting the date from
metadata recorded in the source file header.


**Ignore non-conformant filenames** (cb_truncatelist)

For categories specified in the "newslists" config list, skip files
that do not have a valid date prefix. This allows README files and
pre-release drafts to be set in these categories, which is handy in a
small-scale collaborative environment.


**Provide formatted link lists** (cb_prepare)

The categories specified in the "newslists" config list are mapped as
sorted, formatted link lists in the corresponding (lowercased)
variable names. The lists can be called in a flavor template.

The composition of the link lists (number of items, and whether the
title is linked to an underlying post) is controlled by two values on
the "newslists" config list objects.


**Preview** (cb_pathinfo, cb_truncatelist, cb_prepare)

For collaborative workflows, items placed in the "newslists"
categories that are prefixed with "X" are left out of the default
view, but shown in a preview mode. To access preview pages, prepend
the keyword "preview" to the URL path:

  http://myblog.com/preview/index.html

Preview mode affects only "newslists" lists and items; the prefix
stub is otherwise ignored.

This facility is not particularly tight; the preview items are
available in the clear. In low-security environments where this is
acceptable (like ours), it is sufficient to place the "preview" URL
stub in robots.txt, to prevent search engines from crawling the draft
content. For a very slight improvement in security, the prefix stub
can be defined as some random string. If you need rigorous control
over publication, though, you should be using another workflow or
another tool.


Install
=======

To install, do the following:

1. Add ``newslists`` to the ``load_plugins`` list
   in your ``config.py`` file.

2. Specify a ``newslists`` config variable, like so:

   py["newslists"] = {
        "Alert":{
            "itemCount": 1,
            "useLink": False,
            "useDate": False
         },
         "News":{
            "itemCount": 6,
            "useLink": True,
            "useDate": False
         },
         "Events":{
            "itemCount": 6,
            "useLink": True,
            "useDate": True
         }
   }

3. Be sure that top-level category folders corresponding to the values
   set in the ``newslists`` variable are in place.

4. Set the newslists-preview string in config.py:

     py["newslists-preview"] = "preview"

5. Add the (lowercased) newslist values to your page templates. For
   example:

   <div style="listing">$(news)</div>

The link templates are hard-wired. To change the HTML, just edit the
string templates in the plugin directly.

"""

__author__ = "Frank Bennett"
__email__ = "bennett at nagoya-u ac jp"
__version__ = "$Id$"
__url__ = "http://pyblosxom.github.com/"
__description__ = "Builds headline lists for three categories."
__category__ = "category"
__license__ = "MIT"
__registrytags__ = "1.4, 1.5, core"


from Pyblosxom import tools
from Pyblosxom.tools import pwrap_error
import os, re
import datetime,time
import urllib
import pytz

filerex = re.compile("^([0-9]{4})-([0-9]{2})-([0-9]{2})")

# Templates with placeholders
templates = {}
templates["date"] = {}
templates["nodate"] = {}
templates["date"]["link"] = "<div class='news-link'><i>@@date@@</i> - <a href='en/@@url@@'>@@title@@</a></div>"
templates["date"]["nolink"] = "<div style='background:yellow;text-align:center;'><b>Notice:</b> @@title@@ [@@date@@]</div>"
templates["nodate"]["link"] = "<div class='news-link'><a href='en/@@url@@'>@@title@@</a></div>"
templates["nodate"]["nolink"] = "<div style='background:yellow;text-align:center;'><b>Notice:</b> @@title@@</div>"

# Placeholder name lists for each template
paramsets = {}
paramsets["date"] = {}
paramsets["nodate"] = {}
paramsets["date"]["link"] = ["date","url","title"]
paramsets["date"]["nolink"] = ["date","title"]
paramsets["nodate"]["link"] = ["url","title"]
paramsets["nodate"]["nolink"] = ["title"]

class DateEngine:
    def __init__(self, localZone, srcdir, path_info, data, term_dates=None):
        self.ical_event = open(os.path.join(srcdir, 'icalendar_event.ics')).read()
        self.ical_repeat = open(os.path.join(srcdir, 'icalendar_repeat.ics')).read()
        self.ical_calendar = open(os.path.join(srcdir, 'icalendar.ics')).read()
        self.term_dates = term_dates
        self.localzone = pytz.timezone(localZone)
        self.url = "http://gsl-nagoya-u.net%s" % path_info
        self.icsurl = "%s.ics" % os.path.splitext(path_info)[0]
        if self.icsurl.startswith("/"):
            self.icsurl = self.icsurl[1:]
        self.uid = path_info
        self.valid = False
        self.data = data
        # not yet stored. maybe not needed.
        self.times_to_days = {}
        self.day_to_times = {}
        self.days = {}
        self.interval = 1
        m = re.match("(.*?)\s*\(semi-weekly\)\s*",data['date-and-time'])
        if m:
            self.data['date-and-time'] = m.group(1)
            self.interval = 2
        self.start_date = None
        self.setDate()

    def setDate(self):
        self.valid = True
        self.ics_type = False
        self.repeating = False
        self.dateAsLst = []
        lst = re.split("(?:\s+and\s+|\s*;\s+and\s+|\s*;\s*)", self.data['date-and-time'].strip())
        for i in range(0, len(lst), 1):
            sublst = re.split("(?<=:[0-9]{2})(?:\s+to\s+|\s*-\s*)",lst[i])
            if len(sublst) < 1 or len(sublst) > 2:
                self.valid = False
                return
            # Validation check only
            mStart = re.match("^([0-9]{4}-[0-9]{2}-[0-9]{2})\s+([0-9]{1,2}:[0-9]{2})$",sublst[0])
            if mStart and self.ics_type == "repeating":
                self.valid = False
                return
            elif mStart:
                self.ics_type = "fixed"
            # Check for day spec
            if not self.ics_type or self.ics_type == "repeating":
                self.fixRepeating(sublst)
            mStart = re.match("^([0-9]{4}-[0-9]{2}-[0-9]{2})\s+([0-9]{1,2}:[0-9]{2})$",sublst[0])
            if not mStart:
                self.valid = False
                return
            # Validation only
            mEnd = re.match("^([0-9]{4}-[0-9]{2}-[0-9]{2})\s+([0-9]{1,2}:[0-9]{2})$",sublst[1])
            if mEnd and self.ics_type == "repeating":
                self.valid = False
                return
            elif mEnd:
                self.ics_type = "fixed"
            mEnd = re.match("^(?:([0-9]{4}-[0-9]{2}-[0-9]{2})\s+)*([0-9]{1,2}:[0-9]{2})$",sublst[1])
            if not mEnd:
                self.valid = False
                return
            elif not mEnd.group(1):
                lst[i] = [sublst[0], "%s %s" % (mStart.group(1), mEnd.group(2))]
            else:
                lst[i] = [sublst[0], sublst[1]]
        # If no start_date exists or if validation failed, find the first
        # valid day on or after term_dates start and fill out data
        self.supplementRepeating(lst)
        # For repeating dates in fall semester, extend lst out the back end,
        # using the first valid date after the second start date as start.
        self.appendRepeatingDates(lst)
        #print self.data['title']
        #print "    %s" % lst
        self.dateAsLst = lst

    def appendRepeatingDates(self, lst):
        self.real_length = len(lst)
        if self.ics_type == "repeating":
            # Add limit at position 2
            limit = self.term_dates[self.data['term']][0]['end']
            for i in range(0, len(lst), 1):
                lst[i].append(limit)
        if self.ics_type == "repeating" and len(self.term_dates[self.data['term']]) == 2:
            # Clone the pairs to the 
            for i in range(len(lst)-1,-1,-1):
                pair = lst[i]
                # Get day and time of start and end
                day_start = datetime.datetime.strptime(pair[0], "%Y-%m-%d %H:%M").strftime("%a")
                time_start = datetime.datetime.strptime(pair[0], "%Y-%m-%d %H:%M").strftime("%H:%M")
                day_end = datetime.datetime.strptime(pair[1], "%Y-%m-%d %H:%M").strftime("%a")
                time_end = datetime.datetime.strptime(pair[1], "%Y-%m-%d %H:%M").strftime("%H:%M")
                # Set to start day of term part 2
                dt_start = datetime.datetime.strptime("%s %s" % (self.term_dates[self.data['term']][1]['start'], time_start), "%Y-%m-%d %H:%M")
                # Set start to first-occurring day
                while dt_start.strftime("%a") != day_start:
                    dt_start += datetime.timedelta(days=1)
                # Set end to first-occurring day
                dt_end = datetime.datetime.strptime("%s %s" % (dt_start.strftime("%Y-%m-%d"), time_end), "%Y-%m-%d %H:%M")
                while dt_end.strftime("%a") != day_end:
                    dt_end += datetime.timedelta(days=1)
                # Append to range
                limit = self.term_dates[self.data['term']][1]['end']
                lst.append([dt_start.strftime("%Y-%m-%d %H:%M"), dt_end.strftime("%Y-%m-%d %H:%M"), limit])

    def humanDates(self):
        if not self.valid:
            return self.data['date-and-time']
        else:
            datestr = ''
            lastdate = None
            # Aha! We get repetition of iterative summary dates in Term 2 entries because
            # of the January clone entries.
            #
            # Save of the real length, and truncate here as required
            if self.ics_type == "repeating":
                lst = self.dateAsLst[:self.real_length]
            else:
                lst = self.dateAsLst
            for pair in lst:
                if not lastdate:
                    if self.ics_type == "repeating":
                        datestr += "%s %s" % (self.getHumanDate(pair[0]),self.getHumanTime(pair[0]))
                    else:
                        datestr += "%s, %s" % (self.getHumanDate(pair[0]),self.getHumanTime(pair[0]))
                    lastdate = pair[0][:10]
                    if lastdate == pair[1][:10]:
                        datestr += "-%s" % self.getHumanTime(pair[1])
                    else:
                        datestr += " to %s, %s" % (self.getHumanDate(pair[0]),self.getHumanTime(pair[0]))
                    lastdate = pair[1][:10]
                else:
                    if pair[0][:10] == lastdate:
                        datestr += ", %s" % self.getHumanTime(pair[0])
                    else:
                        if self.ics_type == "repeating":
                            datestr += "; %s %s" % (self.getHumanDate(pair[0]),self.getHumanTime(pair[0]))
                        else:
                            datestr += "; %s, %s" % (self.getHumanDate(pair[0]),self.getHumanTime(pair[0]))
                    lastdate = pair[0][:10]
                    if pair[1][:10] == lastdate:
                        datestr += "-%s" % self.getHumanTime(pair[1])
                    else:
                        datestr += " to %s, %s" % (self.getHumanDate(pair[0]),self.getHumanTime(pair[0]))
            if self.ics_type == "repeating" and self.interval == 2:
                datestr += " (semi-weekly)"
            return datestr

    def getHumanDate(self, s):
        dt = datetime.datetime.strptime(s, "%Y-%m-%d %H:%M")
        dt = self.localzone.localize(dt, is_dst=None)
        if self.ics_type == "repeating":
            return dt.strftime("%a")
        else:
            return dt.strftime("(%a) %e %b %Y")
        
    def getHumanTime(self, s):
        dt = datetime.datetime.strptime(s, "%Y-%m-%d %H:%M")
        dt = self.localzone.localize(dt, is_dst=None)
        return dt.strftime("%k:%M").strip()

    def getIcs(self):
        events = ''
        if self.ics_type == "fixed":
            count = 1
            for pair in self.iter():
                event = self.ical_event
                event = event.replace("@@timestamp@@", self.getNow())
                event = event.replace("@@description@@", "\nDESCRIPTION: %s" % self.url)
                event = event.replace("@@obj_name@@", "%s-%d" % (self.uid, count))
                for key in ["title", "organizer", "email", "place"]:
                    event = event.replace('@@%s@@' % key, self.data[key])
                event = event.replace("@@start@@", self.getDate(pair[0]))
                event = event.replace("@@end@@", self.getDate(pair[1]))
                events += event
                count += 1
            return self.ical_calendar.replace("@@EVENTS@@", events.strip()).replace("\n","\r\n")
        elif self.ics_type == "repeating":
            count = 1
            for pair in self.iter():
                event = self.ical_repeat
                event = event.replace("@@timestamp@@", self.getNow())
                event = event.replace("@@description@@", "\nDESCRIPTION: %s" % self.url)
                event = event.replace("@@obj_name@@", "%s-%d" % (self.uid, count))
                for key in ["title", "organizer", "email", "place"]:
                    event = event.replace('@@%s@@' % key, self.data[key])
                event = event.replace("@@start@@", self.getDate(pair[0]))
                event = event.replace("@@end@@", self.getDate(pair[1]))
                event = event.replace("@@interval@@", str(self.interval))
                until = datetime.datetime.strptime(pair[2], "%Y-%m-%d")
                until = self.localzone.localize(until)
                until = until.astimezone(pytz.utc)
                until = self.calDate(until)
                event = event.replace("@@stop-date@@", until)
                day = datetime.datetime.strptime(pair[0], "%Y-%m-%d %H:%M")
                day = self.localzone.localize(day)
                day = day.astimezone(pytz.utc)
                day = day.strftime("%a")[:2].upper()
                event = event.replace("@@days@@", day)
                events += event
                count += 1
            return self.ical_calendar.replace("@@EVENTS@@", events.strip()).replace("\n","\r\n")

    def getNow(self):
        dt = datetime.datetime.now()
        dt = self.localzone.localize(dt)
        dt = dt.astimezone(pytz.utc)
        return self.calDate(dt)

    def getStartDate(self):
        if self.start_date:
            return datetime.datetime.strptime(self.start_date, "%Y-%m-%d").strftime("(%a) %e %B %Y")
        else:
            return ''

    def calDate(self,dt):
        return dt.strftime("%Y%m%dT%H%M%SZ")

    def supplementRepeating(self, lst):
        if self.ics_type == "repeating":
            # Any proper date is known to be valid, because fixRepeating() is fussy.
            # There will only be one such date.
            # If it exists, set the remainder to a day after that date.
            # If it does not exist, find the first dates for all days
            # in the set, and pick the one that is earliest. Then rinse and repeat.

            # Check for a valid date.
            dt = False
            for pair in lst:
                try:
                    dt = datetime.datetime.strptime(pair[0],"%Y-%m-%d %H:%M")
                    break
                except:
                    pass
            # If no valid date was found, just set all dates to the first
            # qualifying date after term start.
            if not dt:
                term = self.data['term']
                start_date = self.term_dates[term][0]['start']
                dt = datetime.datetime.strptime(start_date, "%Y-%m-%d")
            # Set all recurring dates to a date after the start date.
            for pair in lst:
                try:
                    m = re.match("^(Sun|Mon|Tue|Wed|Thu|Fri|Sat).*",pair[0])
                    if m:
                        day_abbr = m.group(1)
                        while dt.strtime("%a") != day_abbr:
                            dt += datetime.timedelta(days=1)
                        pair[0] = "%s %s" % (dt.strfime("%Y-%m-%d"), re.split("\s+", pair[0])[1])
                        pair[1] = "%s %s" % (dt.strfime("%Y-%m-%d"), re.split("\s+", pair[1])[1])
                except:
                    pass
            epochs = []
            dates = {}
            for pair in lst:
                try:
                    dt = datetime.datetime.strptime(pair[0], "%Y-%m-%d %H:%M")
                    epoch = int(dt.strftime("%s"))
                    epochs.append(epoch)
                    dates[str(epoch)] = dt.strftime("%Y-%m-%d")
                except:
                    pass
            if len(epochs):
                epochs.sort()
                self.start_date = dates[str(epochs[0])]

    def fixRepeating(self, sublst):
        mStart = re.match("^(Sun|Mon|Tue|Wed|Thu|Fri|Sat)\s+([0-9]{1,2}:[0-9]{2})$",sublst[0])
        if mStart and len(sublst) == 2:
            self.ics_type = "repeating"
            time = mStart.group(2)
            # Add day code and time to day key map
            day_code = mStart.group(1).upper()[:2]
            self.days[day_code] = True
            # If a start_date exists, validate it, ignoring if validation fails
            if self.data.has_key('start_date') and self.data['start_date']:
                # Just feed it to datetime in a try/except
                # Adopt blindly for the present if it parses.
                try:
                    dt = datetime.datetime.strptime(self.data['start_date'], "%Y-%m-%d")
                    start_day = dt.strftime("%a")[:2].upper()
                    if start_day == day_code:
                        sublst[0] = "%s %s" % (self.data['start_date'],time)
                except:
                    pass

    def getDate(self, s):
        dt = datetime.datetime.strptime(s, "%Y-%m-%d %H:%M")
        dt = self.localzone.localize(dt, is_dst=None)
        dt = dt.astimezone(pytz.utc)
        return dt.strftime("%Y%m%dT%H%M%SZ")

    def getFirstMonth(self):
        if len(self.dateAsLst):
            dt = datetime.datetime.strptime(self.dateAsLst[0][0], "%Y-%m-%d %H:%M")
            return dt.strftime("%B")
        else:
            return ''

    def getFirstDay(self):
        if len(self.dateAsLst) and len(self.dateAsLst[0]):
            dt = datetime.datetime.strptime(self.dateAsLst[0][0], "%Y-%m-%d %H:%M")
            return dt.strftime("%e")
        else:
            return ''
        
    def iter(self):
        for pair in self.dateAsLst:
            yield [s for s in pair]
    
def verify_installation(request):
    config = request.get_configuration()
    # Check for preview path element def
    if not config.has_key('newslists-preview'):
        pwrap_error("py[\"newslists-preview\"] string is undefined in config.py")
        return False
    # Check for defined categories
    if not config.has_key('newslists'):
        pwrap_error("py[\"newslists\"] is undefined in config.py.")
        return False
    if not type(config["newslists"]) == type({}):
        pwrap_error("py[\"newslists\"] must be %s, found %s" % (type({}), type(config["newslists"])))
        return False
    # Check for at least one category, all with a correspnding directory and a full
    # set of keys
    status = False
    for key in config['newslists']:
        status = True
        if not os.path.exists(os.path.join(config["datadir"],key)):
            pwrap_error("Data directory %s must have category \"%s\" as an immediate subdirectory" % (config["datadir"], key))
            return False
        for subkey in ["itemCount","useLink","useDate"]:
            if not config["newslists"][key].has_key(subkey):
                pwrap_error("py[\"newslists\"] key \"%s\" is missing a value for \"%s\"" % (key,subkey))
                return False
    if status == False:
        pwrap_error("py[\"newslists\"] must define at least one category")
        return False
    return True

def cb_postformat(args):
    config = args['request'].get_configuration()
    # Best sequence
    # (1) Extract keys, if any
    keypairs = []
    for key in ['organizer','email','date-and-time','place','presenter']:
        if args['entry_data'].has_key(key):
            keypairs.append([key,args['entry_data'][key]])
    # (2) If keys exist, validate them, throw exception or issue a warning if required tag missing
    insert_metadata = False
    dates = []
    if len(keypairs):
        path_info = args['request'].get_http()['PATH_INFO']
        for reqkey in ['date-and-time', 'place', 'organizer', 'email']:
            if not args['entry_data'].has_key(reqkey):
                print "WARNING: required key %s is missing from %s" % (reqkey,path_info)
                args['entry_data'][reqkey] = "TBA"
        srcdir = config['appdir']
        data = args['entry_data']
        dater = DateEngine("Asia/Tokyo", srcdir, path_info, data)
        #dater.setDate(args['entry_data']['date-and-time'])
        insert_metadata = dater.valid

    # (3) If keys validate, extract the body and perform substitutions
    body = args['entry_data']['body']
    # Build substitution strings
    ## ical link
    ## details
    details = ''
    keymap = {"title-detail":"Title","presenter":"Presenter","date-and-time":"Date & Time","place":"Place","language":"Language"}
    for key in ["title-detail", "presenter", "date-and-time", "place", "language"]:
        if args['entry_data'].has_key(key):
            if key == 'date-and-time':
                val = dater.humanDates()
            else:
                val = args['entry_data'][key]
            details += '<p><strong>%s:</strong> %s' % (keymap[key], val)
    if details:
        details = '<blockquote>%s</blockquote>' % details
    # Substitute details into body
    args['entry_data']['body'] = args['entry_data']['body'].replace('@@DETAILS@@', details)
    # Substitute calendar link into body
    if insert_metadata:
        http = args['request'].get_http()
        path_info = http['PATH_INFO']
        month = dater.getFirstMonth()
        day = dater.getFirstDay()
        if len(dater.dateAsLst) > 1:
            day = "%s+" % day
        ics_link = "%s.ics" % os.path.splitext(path_info)[0]
        calendar_link = '<a href="/en%s" title="Add to calendar" class="calendar-link"><div class="month">%s</div><div class="day">%s</div></a>' % (ics_link,month,day)
        args['entry_data']['calendar_link'] = calendar_link
    else:
        args['entry_data']['calendar_link'] = ''
    # (4) If this is a non-index object, generate and save the ical file(s).    
    if insert_metadata and not args['request'].get_http()['PATH_INFO'].split("/")[-1].startswith('index'):
        data = args['entry_data']
        static_dir = config['static_dir']
        if dater.valid:
            ical = dater.getIcs()
            # print ical
            open(os.path.join(static_dir, dater.icsurl), 'w+').write(ical)

def cb_pathinfo(args):
    config = args['request'].getConfiguration()
    data = args['request'].get_data()
    pyhttp = args['request'].get_http()
    url = pyhttp['PATH_INFO']
    urltype, urlhost = urllib.splittype(url)
    urlhost, urlpath = urllib.splithost(urlhost)
    if urltype:
        urlstub = "%s://%s" % (urltype,urlhost)
    else:
        urlstub = ''
    pathlst = urlpath.split("/")[1:]
    if len(pathlst) > 0 and pathlst[0] == config["newslists-preview"]:
        pathlst = pathlst[1:]
        config['preview'] = True
    else:
        config['preview'] = False
    url = '/'.join([urlstub] + pathlst)
    pyhttp['PATH_INFO'] = url

def cb_filestat(args):
    """Parse the entry filename looking for a date pattern. If the
    pattern matches and is a valid date, then override the mtime.
    
    """
    from Pyblosxom import tools
    filepath = args['filename']
    filelst = os.path.split(filepath)
    filename = filelst[-1]
    datadir = args['request'].getConfiguration()['datadir']
    logger = tools.getLogger()
    
    # If we find a date pattern in the filename, load it into the args
    # dict and return. If a pattern is not found, or if the values
    # in the yyyy-mm-dd prefix do not constitute a valid date,
    # return args unmolested.
    m = filerex.match(filename)
    if m:
        try:
            year = int(m.group(1))
            month = int(m.group(2))
            day = int(m.group(3))
            # Time values all set to zero in this implementation
            mtime = time.mktime((year,month,day,0,0,0,0,0,-1))
            stattuple = args['mtime']
            args['mtime'] = tuple(list(stattuple[:8]) + [mtime] + list(stattuple[9:]))
        except Exception as e:
            logger.error("%s: %s" % (type(e), e.args))
            return args
    return args

def cb_truncatelist(args):
    """For each entry under a named category, parse the entry filename
       looking for a date pattern. If the pattern does not match,
       delete the file from the list.
    """
    from Pyblosxom import tools
    logger = tools.getLogger()
    request = args['request']
    config = request.getConfiguration()
    category_names = config['newslists'].keys()
    category_configs = config['newslists']
    if config.has_key('pagesdir'):
        pagesdir = config['pagesdir']
    else:
        pagesdir = False
    data = request.get_data()

    # The entry_list segment is a little funny inside
    # Pyblosxom. On most occasions it is double-nested when
    # this callback is invoked, so we don't return args
    # verbatim from this function.

    entry_list = args['entry_list']
    previewing = config['preview']
    for i in range(len(entry_list) - 1, -1, -1):
        entry = entry_list[i]
        filepath = entry['file_path']
        # Check for path
        if filepath:
                # Split file path
            filelst = filepath.split(os.path.sep)
            # Always pass through index pages
            if filelst[-1] == "index":
                continue
            # Always pass through static pages
            if pagesdir and entry['filename'].startswith(pagesdir):
                continue
            # Check for dated config
            if category_configs:
                # Check for date pattern. This doesn't check
                # for date validity, only a looks-like-a-date
                # pattern.
                logger.debug("%s" % filelst[-1])
                if not filerex.match(filelst[-1]):
                    if not previewing or not filelst[-1].startswith('X'):
                        args['entry_list'].pop(i)
                else:
                    if previewing:
                        args['entry_list'].pop(i)
    return args['entry_list']


class GetNewsList:
    def __init__(self, config, categoryName, itemCount=6, useLink=True, useDate=True):
        self._config = config
        self._categoryName = categoryName
        self._count = itemCount
        if useLink:
            self._link = "link"
        else:
            self._link = "nolink"
        if useDate:
            self._date = "date"
        else:
            self._date = "nodate"
        self._news_list = None
        self.gen_news_list()

    def __str__(self):
        if self._news_list == None:
            self.gen_news_list()
        return self._news_list

    def gen_news_list(self):
        gottenStuff = []
        dirpath = os.path.join(self._config['datadir'], self._categoryName)
        files = os.listdir(dirpath)
        files.sort()
        files.reverse()
        count = 0
        stuff = []
        for filename in files:
            # Save some cycles on really common matches
            if filename == "README.txt" or filename.endswith("~"):
                continue
            m = filerex.match(filename)
            dome = True
            previewing = self._config['preview']
            if not m:
                if not previewing or not filename.startswith('X'):
                    dome = False
                else:
                    if previewing:
                        m = filerex.match(filename[1:])
                    else:
                        dome = False
            else:
                if previewing:
                    dome = False
            if dome and m:
                # Snip off date
                year = int(m.group(1))
                month = int(m.group(2))
                day = int(m.group(3))
                # Format date, skipping if date is invalid
                try:
                    date = datetime.date(year, month, day).strftime("%e %b %Y (%a)").strip()
                except Exception as e:
                    continue
                # Open file
                ifh = open(os.path.join(dirpath, filename))
                # Get title
                title = ifh.readline()
                # Compose strings
                if title:
                    # Get template
                    template = templates[self._date][self._link]
                    # Get paramset
                    paramset = paramsets[self._date][self._link]
                    params = {}
                    for key in paramset:
                        if key == "title":
                            params['title'] = title.strip()
                        elif key == "url":
                            filestub = os.path.splitext(filename)[0]
                            filehtml = "%s.html" % filestub
                            base = self._config['base_url']
                            category = self._categoryName
                            params['url'] = os.path.join(base, category, filehtml)
                            # If config['preview'] is True, restore 'preview' to URL
                            if self._config['preview']:
                                url = params['url']
                                urltype, urlhost = urllib.splittype(url)
                                urlhost, urlpath = urllib.splithost(urlhost)
                                if urltype:
                                    urlstub = "%s://%s" % (urltype,urlhost)
                                else:
                                    urlstub = ''
                                pathlst = urlpath.split("/")
                                pathlst = [config["newslists-preview"]] + pathlst
                                params['url'] = "/".join([urlstub] + pathlst)

                            while True:
                                line = ifh.readline()
                                if not line: break
                                if not line.startswith("#"): break
                                if line.startswith("#link ") and len(line) > 6:
                                    params['url'] = line[6:]
                                    break
                        elif key == "date":
                            params['date'] = date
                    for key in params:
                        template = template.replace('@@%s@@' % key, params[key])
                    
                    # Add to list
                    stuff.append(template)
                    count += 1
                    if count == self._count:
                        break
                ifh.close()
        self._news_list = "\n".join(stuff)

def cb_prepare(args):
    request = args['request']
    config = request.get_configuration()
    base_url = config['base_url']
    if not base_url:
        base_url = ''
    data = request.get_data()
    logger = tools.get_logger()
    logger.debug(data['url'])
    if data['url'] == "%s/index.html" % base_url:
        for categoryName in config["newslists"].keys():
            key = categoryName.lower()
            cfg = config["newslists"][categoryName]
            data[key] = GetNewsList(config, categoryName, cfg['itemCount'], cfg['useLink'], cfg['useDate'])
