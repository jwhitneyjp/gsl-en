#!/usr/bin/env python
"""filedate.py pyblosxom plugin.

For entry source files that begin with a yyyy-mm-dd string,
set the date of the post from the filename, overriding
the mtime value.

This works out nicely for keeping posts organized in a
filesystem view, and requires less overhead than extracting
the date from metadata recorded in the source file header.


"""

__author__ = 'Frank Bennett'
__homepage__ = 'http://github.com/fbennett/PyBlosxom-filedate'
__email__ = 'biercenator@gmail.com'
__version__ = "1"
__description__ = "Optionally set the date of posts from filename prefix instead of file mtimes."

import os,re,time

# The regex for a filename date
filerex = re.compile("^([0-9]{4})-([0-9]{2})-([0-9]{2})")

# The plugin callback
# -------------------

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
