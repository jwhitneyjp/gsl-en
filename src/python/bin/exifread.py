#!/usr/bin/env python
'''
  Write description data to a file, creating an empty file
  if the data cannot be read.
'''

import pexif
import sys
from os.path import basename

usage = "Usage: %s <jpeg_file>" % basename(sys.argv[0])

if not len(sys.argv) == 2:
  print usage
  sys.exit(1)

file_jpg = sys.argv[1]
file_txt = file_jpg + '..txt'

try:
    exif = pexif.JpegFile.fromFile( file_jpg ).get_exif()
    description = exif.get_primary()[pexif.ImageDescription]
    open( file_txt, 'w').write(description)
except:
    open( file_txt, 'w').write('')
    sys.exit(0)
