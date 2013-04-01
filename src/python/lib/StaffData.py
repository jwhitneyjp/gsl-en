'''
  Utility module to generate a staff index page
'''

import sys,os,re,os.path

from pathtool import gslpath
gp = gslpath()

#from myExcelerator import *
import re

def getStaffData(c,taughtby,imagedir):
    staffdata = []
    count = 0
    
    for data in c:
        
        if count % 3 == 0:
            packetofthree = []
        
        member = {}
    
        affiliations = {}
        affiliations['AW'] = 'Academic Writing Support'
        affiliations['LS'] = 'Law School'
        affiliations['GSL'] = 'Graduate School'
        affiliations['Leading'] = 'Leading Program'
        affiliations['G30'] = 'Global 30 Program'
        x = data['affiliation'].strip()
        x = [y.strip() for y in x.split('+')]
        member['affiliations_raw'] = x[:]
        
        for pos in range(len(x)-1,-1,-1):
            affiliation = x[pos]
            if affiliations.has_key(affiliation):
                x[pos] = affiliations[affiliation]
        member['affiliations'] = ' &amp; '.join(x)

        member['uid'] = data['uid']
        member['birthdate'] = data['birthdate']
        member['sabbatical'] = data['sabbatical']
        member['supervision'] = data['supervision']
        member['proper_name'] = data['proper_name']
        member['status'] = data['status']
        member['profession'] = data['profession']
        member['departure'] = data['departure']
        member['profile_url'] = gp.faculty.url( 'gsli%s.html' % (data['uid'],) )
        member['profile_url_cached'] = gp.facultycache.url( 'gsli%s.html' % (data['uid'],) )
        member['photo_web_ok'] = data['photo_web_ok']
        member['tutorial_link'] = data['tutorial_link']

        have_photo = False
        photo_filename = data['uid'] + '.jpg'
        for i in os.listdir(imagedir):
            if i == photo_filename:
                have_photo = True
                break
        photo_filename =  "%s_small.jpg" %data['uid']

        member['photo_url'] =  gp.facultycache.url( photo_filename )

        member['full_name'] = '%s %s' % (data['given_name'],data['family_name'])
        member['field'] = data['field']
        
        if taughtby.has_key(data['uid']):
            member['isinstructor'] = True
        else:
            member['isinstructor'] = False
        
        staffdata.append(member)
        
    return staffdata
