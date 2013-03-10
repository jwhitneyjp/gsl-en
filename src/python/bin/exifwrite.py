#!/usr/bin/env python
'''
  Write description from text file to jpg image exif segment.
'''

import pexif, sys, os
from os.path import basename

usage = "Usage: %s <file>..txt <file>.jpg" % basename(sys.argv[0])

if not len(sys.argv) == 3 or not sys.argv[1].endswith('..txt'):
  print usage
  sys.exit(1)
  
file_jpg = sys.argv[2]
file_tmp = file_jpg + '..jpg'
description = open(file_jpg + '..txt').read()

img = pexif.JpegFile.fromFile( file_jpg )
exif = img.get_exif(create=True)
exif.get_primary(create=True)[pexif.ImageDescription] = description
img.writeFile( file_tmp )
os.rename(file_tmp, file_jpg)
