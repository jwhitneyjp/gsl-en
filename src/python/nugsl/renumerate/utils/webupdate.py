#!/usr/bin/python

import re,os

product = 'renumerate'

directory_path = '/home/bennett/Desktop/Web/src/docroot/info/appendix/software/'

def cmp_ver(dist_version, directory_version):
    for pos in range(0,len(dist_version),1):
        if dist_version[pos] > directory_version[pos]:
            print '%s > %s ?' % (dist_version[pos],directory_version[pos])
            return 1
        elif dist_version[pos] < directory_version[pos]:
            return -1
    return 0

if not os.path.exists(directory_path + product + '/obsolete'):
    os.makedirs(directory_path + product + '/obsolete')

directory_files = []
for filename in os.listdir(directory_path + product):    
    if not filename.endswith('.tgz'):
        continue
    f = filename.split('-') 
    if not product in f:
        raise ValueError
    directory_files.append(filename)

if len(directory_files) > 1:
    raise ValueError
else:
    rfilename_old = directory_files[0]
    
# get file with highest version number from dist
for sfilename in os.listdir('dist'):
    if not sfilename.endswith('.tar.gz'):
        continue
    f = sfilename.split('-')
    if not product in f:
        raise ValueError
    sversion = f[2][:-7].split('.')
    rversion = rfilename_old.split('-')[2][:-4].split('.')

    if cmp_ver(sversion, rversion) == 1:
        print 'Moving new file into place'
        rfilename_new = sfilename[:-7]+'.tgz'
        os.rename(directory_path+product+'/'+rfilename_old,directory_path+product+'/obsolete/'+rfilename_old)
        os.rename('dist/'+sfilename,directory_path+product+'/'+rfilename_new)
    elif cmp_ver(sversion, rversion) == 0:
        print 'WARNING: Refreshing existing version'
        rfilename_new = sfilename[:-7]+'.tgz'
        os.rename('dist/'+sfilename,directory_path+product+'/'+rfilename_new)
        