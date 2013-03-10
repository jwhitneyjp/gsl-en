#!/usr/bin/env python
"""datedcategories.py pyblosxom plugin.

"""

__author__ = 'Frank Bennett'
__homepage__ = 'http://citationstylist.com/'
__email__ = 'biercenator@gmail.com'
__version__ = "1"
__description__ = "Suppress files that do not begin with a yyyy-mm-dd date."

import os,re,datetime,time,sys,getopt

# The regex for a filename date
filerex = re.compile("^([0-9]{4})-([0-9]{2})-([0-9]{2})")

# The plugin callback
# -------------------

def cb_truncatelist(args):
    """For each entry under a named category, parse the entry filename
       looking for a date pattern. If the pattern does not match,
       delete the file from the list.
    """
    from Pyblosxom import tools
    logger = tools.getLogger()
    request = args['request']
    config = request.getConfiguration()
    categories = config['datedcategories']
    pagesdir = config['pagesdir']
    data = request.get_data()
    entry_list = args['entry_list']
    for i in range(len(entry_list) - 1, -1, -1):
        entry = entry_list[i]
        #print entry.keys()
        filepath = entry['file_path']
        # Check for path
        if filepath:
            # Split file path
            filelst = filepath.split(os.path.sep)
            # Check for index
            if filelst[-1] == "index":
                continue
            # Check for pages trigger
            if pagesdir and entry['filename'].startswith(pagesdir):
                continue
            # Check for dated config
            if categories:
                # Check for date pattern
                logger.debug("%s" % filelst[-1])
                if not filerex.match(filelst[-1]):
                    args['entry_list'].pop(i)
    return args['entry_list']
