#!/usr/bin/python
#-*- encoding: utf8 -*-

import csv, sys, re, os

TODOFUKEN = '(.*?[都|道|府|県])(.+)*'.decode('utf8')

CITIES = '(市*[^区市]+?(?:市市|市|島|郡|村|町|区))(?:([^区0-9]+)区)*.*'.decode('utf8')

for file in os.listdir('data'):
    ifh = open('data/' + file)
    csvread = csv.reader(ifh)

    ofh = open('cleaned/' + file, 'w+')
    csvwrite = csv.writer(ofh)

    print 'Processing ' + file

    linecount = 1
    
    for line in csvread:
        r2 = re.match(TODOFUKEN,line[2].decode('utf8'))
        if line[0] == 'name':
            line.insert(3,'ku')
            line.insert(3,'entity_type')
            line.insert(3,'entity_name')
            line.insert(3,'todofuken')
        else:
            if r2:
                todofuken = r2.group(1)
                line.insert(3,todofuken)

                address = r2.group(2)
                if not address:
                    address = ''
            else:
                print 'Ouch!'
                print line[2]
                sys.exit()
            r = re.match(CITIES,address)
            if r:
                if r.group(2):
                    ku = r.group(2)
                else:
                    ku = ''
            
                line.insert(4,ku)
                line.insert(4,r.group(1)[-1])
                line.insert(4,r.group(1)[:-1])
            else:
                line.insert(4,"")
                line.insert(4,"")
                line.insert(4,"")
                print '  WARNING: Unparsed address at line %d: %s' % (linecount, address)
        
        csvwrite.writerow( line )
        
        linecount += 1
