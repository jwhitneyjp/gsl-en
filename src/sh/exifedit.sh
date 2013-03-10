#!/bin/bash
# Put this script in the task bar under Linux to provide
# drag-and-drop editing of jpeg comments.
#
# Requires python and, third-party module pexif, and
# our own little scripts exifread.py and exifwrite.py
#
# Frank Bennett
# Nagoya, Japan

# variable paranoia, and quit immediately on error
set -u
set -e

# convert url to simple filename
FILE=`echo "$@" | sed s~^file://~~`
FILE=`python -c "import sys,urllib; print urllib.unquote(sys.argv[1])" "$FILE"`

# clean up on exit
trap "rm -f \"$FILE..txt\" \"$FILE..txt~\" \"$FILE..jpg\"; exit" INT TERM EXIT

# attempt to extract comment to file
exifread.py "$FILE"

jed "$FILE..txt"

# place commented text in file
exifwrite.py "$FILE..txt" "$FILE"
