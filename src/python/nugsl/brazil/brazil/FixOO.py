''' Module
'''
import re
from StringIO import StringIO
import tidy
from htmlentitydefs import name2codepoint as n2cp

def substitute_entity(match):
    ent = match.group(2)
    if match.group(1) == "#":
        return unichr(int(ent))
    else:
        cp = n2cp.get(ent)

        if cp:
            return unichr(cp)
        else:
            return match.group()

def decode_htmlentities(string):
    entity_re = re.compile("&(#?)(\d{1,5}|\w{1,8});")
    return entity_re.subn(substitute_entity, string)[0]


class fixOO:
    
    def __init__(self, s):
        txt = s.decode('utf-8','replace')
        txt = decode_htmlentities( txt )

        txt = re.sub('(?i)<form [^>]*>','',txt)
        txt = re.sub('(?i)</form>','',txt)

        txt = re.sub('(?i)<sdfield [^>]*>','',txt)
        txt = re.sub('(?i)</sdfield>','',txt)
        
        txt = re.sub('(?i) id="[^"]*"',' ',txt)

        io = StringIO()
        options = dict(char_encoding='utf8')
        txt = txt.encode('utf8')

        tdoc = tidy.parseString( txt, **options)

        tdoc.write( io )
        io.seek(0)
        s = io.read()
        self.html = s

