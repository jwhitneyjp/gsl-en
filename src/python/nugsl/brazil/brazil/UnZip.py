''' Module
'''

from zipfile import ZipFile, BadZipfile
from types import StringType

class unZip(StringType):
    
    def __new__(self, filename):
        rtf_name = filename[:-4] + '.rtf'
        try:
            z = ZipFile( filename )
            files = z.namelist()
            content = z.read( files[0] )
            z.close()
        except BadZipfile:
            return None
        return StringType.__new__(self, content )
