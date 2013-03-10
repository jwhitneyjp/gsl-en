# -*- coding: utf-8 -*-
# =================================================================
# This is the config file for Pyblosxom.  You should go through 
# this file and fill in values for the various properties.  This 
# affects the behavior of your blog.
#
# This is a Python code file and as such must be written in
# Python.
#
# There are configuration properties that are not detailed in
# this file.  These are the properties that are most often used.
# To see a full list of configuration properties as well as
# additional documentation, see the Pyblosxom documentation on
# the web-site for your version of Pyblosxom.
# =================================================================

# Don't touch this next line.
py = {}


# Codebase configuration
# ======================

import os,sys

# If you did not install Pyblosxom as a library (i.e. python setup.py install)
# then uncomment this next line and point it to your Pyblosxom installation
# directory.
# 
# Note, this should be the parent directory of the "Pyblosxom" directory
# (note the case--uppercase P lowercase b!).
#py["codebase"] = "/home/frontpage/pyblosxom"

repodir = os.environ["PWD"]
repoparent = os.path.split(repodir)[0]

blogdir = os.path.join(repodir, "src", "pyblosxom", "content")

py["codebase"] = os.path.join(repodir, "src", "pyblosxom")


# Blog configuration
# ==================

# What is the title of this blog?
py["blog_title"] = "Nagoya University, Graduate School of Law"

# What is the description of this blog?
py["blog_description"] = "News and Events"

# Who are the author(s) of this blog?
py["blog_author"] = "International Exchange Committee"

# What is the email address through which readers of the blog may contact
# the authors?
py["blog_email"] = "bennett@law.nagoya-u.net"

# These are the rights you give to others in regards to the content
# on your blog.  Generally, this is the copyright information.
# This is used in the Atom feeds.  Leaving this blank or not filling
# it in correctly could result in a feed that doesn't validate.
py["blog_rights"] = "Copyright 2012 Faculty of Law, Nagoya University"

# What is this blog's primary language (for outgoing RSS feed)?
py["blog_language"] = "en"

# Encoding for output.  This defaults to utf-8.
py["blog_encoding"] = "utf-8"

# What is the locale for this blog?  This is used when formatting dates
# and other locale-sensitive things.  Make sure the locale is valid for
# your system.  See the configuration chapter in the Pyblosxom documentation
# for details.
#py["locale"] = "en_US.iso-8859-1"

# Where are this blog's entries kept?
py["datadir"] = os.path.join(repoparent, "gsl-frontpage-master")

# For newslists ico hack
py["appdir"] = os.path.join(repodir, "src", "docroot")

# Where are this blog's flavours kept?
py["flavourdir"] = os.path.join(blogdir, "flavours")

# List of strings with directories that should be ignored (e.g. "CVS")
# ex: py['ignore_directories'] = ["CVS", "temp"]
py["ignore_directories"] = []

# Should I stick only to the datadir for items or travel down the directory
# hierarchy looking for items?  If so, to what depth?
# 0 = infinite depth (aka grab everything)
# 1 = datadir only
# n = n levels down
py["depth"] = 0

# How many entries should I show on the home page and category pages?
# If you put 0 here, then I will show all pages.
# Note: this doesn't affect date-based archive pages.
py["num_entries"] = 15 

# What is the default flavour you want to use when the user doesn't
# specify a flavour in the request?
py["default_flavour"] = "html"

# Logging configuration
# =====================

# Where should Pyblosxom write logged messages to?
# If set to "NONE" log messages are silently ignored.
# Falls back to sys.stderr if the file can't be opened for writing.
py["log_file"] = os.path.join(repodir, "pyblosxom.log")

# At what level should we log to log_file?
# One of: "critical", "error", "warning", "info", "debug"
# For production, "warning" or "error' is recommended.
py["log_level"] = "info"

# This lets you specify which channels should be logged.
# If specified, only messages from the listed channels are logged.
# Each plugin logs to it's own channel, therefor channelname == pluginname.
# Application level messages are logged to a channel named "root".
# If you use log_filter and ommit the "root" channel here, app level messages 
# are not logged! log_filter is mainly interesting to debug a specific plugin.
#py["log_filter"] = ["root", "plugin1", "plugin2"]



# Plugin configuration
# ====================

# Plugin directories:
# This allows you to specify which directories have plugins that you
# want to load.  You can list as many plugin directories as you
# want.
# Example: py['plugin_dirs'] = ["/home/joe/blog/plugins",
#                               "/var/lib/pyblosxom/plugins"]



py["plugin_dirs"] = [os.path.join(blogdir, "plugins")]

# There are two ways for Pyblosxom to load plugins:
# 
# The first is the default way where Pyblosxom loads all plugins it
# finds in the directories specified by "plugins_dir" in alphanumeric
# order by filename.
# 
# The second is by specifying a "load_plugins" key here.  Specifying
# "load_plugins" will cause Pyblosxom to load only the plugins you name 
# and in in the order you name them.
# 
# The "load_plugins" key is a list of strings where each string is
# the name of a plugin module (i.e. the filename without the .py at
# the end).
# 
# If you specify an empty list, then this will load no plugins.
# ex: py["load_plugins"] = ["pycalendar", "pyfortune", "pyarchives"]
py["load_plugins"] = ["markdown_parser","newslists","pages"]
#py["load_plugins"] = ["markdown_parser","metadate","newslists"]

py["pagesdir"] = os.path.join(blogdir, "pages")
py["pages_frontpage"] = True

py["newslists-preview"] = "preview"
py["newslists"] = {
    "Alert": {
        "itemCount": 1,
        "useDate": False,
        "useLink": False
    },
    "News": {
        "itemCount": 6,
        "useDate": False,
        "useLink": True
    },
    "Events": {
        "itemCount": 6,
        "useDate": True,
        "useLink": 6
    }
}


# ======================
# Optional Configuration
# ======================

# What should this blog use as its base url?
py["base_url"] = ""

# Default parser/preformatter. Defaults to plain (does nothing)
py["parser"] = "markdown"



# Static rendering
# ================

# Doing static rendering?  Static rendering essentially "compiles" your
# blog into a series of static html pages.  For more details, see the
# documentation.
# 
# What directory do you want your static html pages to go into?
py["static_dir"] = os.path.join(repoparent, "gsl-prerendered")

# What flavours should get generated?
py["static_flavours"] = ["html"]

# What other paths should we statically render?
# This is for additional urls handled by other plugins like the booklist
# and plugin_info plugins.  If there are multiple flavours you want
# to capture, specify each:
# ex: py["static_urls"] = ["/booklist.rss", "/booklist.html"]
py["static_urls"] = ["/index.atom", "/index.rss"]

# Whether (True) or not (False) you want to generate date indexes with month
# names?  (ex. /2004/Apr/01)  Defaults to True.
py["static_monthnames"] = False

# Whether (True) or not (False) you want to generate date indexes
# using month numbers?  (ex. /2004/04/01)  Defaults to False.
py["static_monthnumbers"] = False

# Whether (True) or not (False) you want to generate year indexes?
# (ex. /2004)  Defaults to True.
py["static_yearindexes"] = False

