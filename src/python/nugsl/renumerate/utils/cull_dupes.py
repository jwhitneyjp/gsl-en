#!/usr/bin/python

import csv,sys,dbm,StringIO

database = dbm.open('names','c')
ifh = open('demo.csv')

i = csv.reader( ifh )
for row in i:
    name = row[1]
    if row[2] == '':
        row[2] = '0'
    if row[3] == '':
        row[3] = '0'
    if database.has_key(name+':val'):
        if int(database[name+':val']) < int(row[2]):
            database[name+':max'] = row[3]
            database[name+':val'] = row[2]
    else:
        database[name+':max'] = row[3]
        database[name+':val'] = row[2]
ifh.close()
        
ofh = open('demo-clean.csv','w+')
o = csv.writer( ofh )
for key in database.keys():
    if key.endswith(':max'):
        continue
    o.writerow( [key,database[key],database[key[:-4]+':max']] )
