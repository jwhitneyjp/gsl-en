"""
Utility suite for managing information on Nagoya University
Faculty of Law websites.
"""

import urllib
import cookielib
import urllib2
import popen2
import cStringIO
import tidylib
import libxml2
import sys
import codecs
import re
import os

import httplib, mimetypes, mimetools

auth = {}

a = {}
a['id'] = 'bennett'
a['pwd'] = 'Lnosiatl'
a['realm'] = 'Zope'
a['logintype'] = 'basic'
auth['infosv.law.nagoya-u.ac.jp'] = a

a = {}
a['id'] = 'meidai-law'
a['pwd'] = 'htd05if2'
a['realm'] = 'Please enter username and password'
a['logintype'] = 'basic'
auth['www.gsl-nagoya-u.net'] = a

a = {}
a['loginparams'] = []
a['loginparams'].append(('Email','biercenator'))
a['loginparams'].append(('Passwd','Lnosiatl'))
a['loginurl'] = 'https://www.google.com/accounts/LoginAuth?continue=http%3A%2F%2Fwww.google.co.jp%2F&hl=en'
a['logintype'] = 'cookie'
auth['www.google.com'] = a


u2s = codecs.getencoder('shift_jis')
s2u = codecs.getdecoder('shift_jis')
u2u8 = codecs.getencoder('utf8')
u82u = codecs.getdecoder('utf8')
u2e = codecs.getencoder('euc_jp')
e2u = codecs.getdecoder('euc_jp')

def fetch (url,coding,field=[],file=[],debug=None,skipauth=None):
    '''
    file is a tuple (name, filename, value)
    '''
    u = url.split('/')
    host = u[2]

    if coding.lower() == 'binary':
        try:
            ifh = urllib2.urlopen(url)
            ret = ifh.read()
        except urllib2.HTTPError:
            ret = ''
        return ret
    elif auth.has_key(host) and not skipauth:
        if auth[host]['logintype'] == 'cookie':
            urlopen = urllib2.urlopen
            cj = cookielib.LWPCookieJar()
            Request = urllib2.Request
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
            urllib2.install_opener(opener)
            
            txheaders =  {'User-agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
            
            params = []
            for p in auth[host]['loginparams']:
                params.append((p[0], p[1]))

            urlparams = urllib.urlencode(params)
            theurl = auth[host]['loginurl']
            req = Request(theurl, urlparams, txheaders)
            
            ifh = urlopen(req)   
            
        else:
            selector = '/' + '/'.join(u[3:])
    
            auth_handler = urllib2.HTTPBasicAuthHandler()
            auth_handler.add_password(auth[host]['realm'],
                                  'http://%s' % (host,), 
                                  auth[host]['id'], 
                                  auth[host]['pwd'])
            opener = urllib2.build_opener(auth_handler)
            urllib2.install_opener(opener)

            ifh = post_multipart(host, selector, field, file)
    else:
        ifh = urllib2.urlopen(url)
    text = ifh.read()

    if coding.replace('-','').replace('_','').lower() == 'shiftjis':
          text = text.decode('shift_jis','replace')
          text = text.encode('utf8','replace')
    elif coding.replace('-','').replace('_','').lower() == 'eucjp':
          text = text.decode('euc_jp','replace')
          text = text.encode('utf8','replace')
    else:
          text = text.decode('utf8','replace')
          text = text.encode('utf8','replace')
          
    options = dict(char_encoding='utf8',wrap=0,indent='auto')
    text = tidylib.tidy_document(text, options)[0]
    # Check if there are http:// strings in the string
    # anywhere, and grab the range that consists of
    # the following characters only.  Wrap it in 
    # a pair of <a> tags with the same string as
    # a link attribute.  This should best be done
    # on individual chunks as they come down
    # the pike, before page building.
    #
    # Hmm, but that would mean running a function
    # out in the script.  Clutter.  Bad.  How about
    # in Excellist, when the text gets written
    # to the XLS file in discrete pieces?  That would
    # be safer than bashing about here, which could
    # go terribly wrong.
    xxx = """
    [a-z][A-Z][0-9]$-_.+!*'(),;/?:@=&
    """
    if debug:
          ofh = open('debug.txt','w+')
          ofh.write(text)
          ofh.close()
          sys.exit()
          
    # Clean up a bit of HTML drool
    text = re.sub(r'id="([^#])',r'id="#\1',text)
          
    ret = libxml2.htmlParseDoc(text,'UTF-8')
    return ret

def post_multipart(host, selector, fields, files):
    """
    Post fields and files to an http host as multipart/form-data.
    fields is a sequence of (name, value) elements for regular form fields.
    files is a sequence of (name, filename, value) elements for data to be uploaded as files
    Return the server's response page.
    """
    content_type, body = encode_multipart_formdata(fields, files)
    headers = {'Content-Type': content_type,
                 'Content-Length': str(len(body))}
    r = urllib2.Request("http://%s%s" % (host, selector), body, headers)
    return urllib2.urlopen(r)

def encode_multipart_formdata(fields, files):
    """
    fields is a sequence of (name, value) elements for regular form fields.
    files is a sequence of (name, filename, value) elements for data to be uploaded as files
    Return (content_type, body) ready for httplib.HTTP instance
    """
    BOUNDARY = mimetools.choose_boundary()
    CRLF = '\r\n'
    L = []
    io = cStringIO.StringIO()
    for (key, value) in fields:
        io.write('--' + BOUNDARY)
        io.write(CRLF)
        io.write('Content-Disposition: form-data; name="%s"' % key)
        io.write(CRLF)
        io.write(CRLF)
        io.write(value)
        io.write(CRLF)
    for (key, filename, value) in files:
        io.write('--' + BOUNDARY)
        io.write(CRLF)
        io.write('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
        io.write(CRLF)
        io.write('Content-Type: application/octet-stream')
        io.write(CRLF)
        io.write(CRLF)
        io.write(value)
        io.write(CRLF)
    io.write('--' + BOUNDARY + '--')
    io.write(CRLF)
    io.write(CRLF)
    io.seek(0)
    body = io.read()
    
    content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
    return content_type, body

def get_content_type(filename):
    return mimetypes.guess_type(filename)[0] or 'application/octet-stream'



