#!/usr/bin/python
#-*- encoding: utf8 -*-

import csv, sys

AMOUNT = []
AMOUNT.append('0〜100万円未満')
AMOUNT.append('100万円以上1,000万円未満')
AMOUNT.append('1,000万円以上1億円未満')
AMOUNT.append('1億円以上')

class Analyze:
    def __init__(self):
        self.ifh = open('envo-cleaned/EnvironmentalNGOs.csv')
        self.csvread = csv.reader( self.ifh )
        self.headers = self.csvread.next()

    def get_data(self, name):
        pos = self.headers.index( name )
        return self.line[pos]

if __name__ == '__main__':
    
    obj = Analyze()

    for header in obj.headers:
        print header
    print '***'
    npo = 0
    non_npo = 0
    npo_budget = [0,0,0,0]
    non_npo_budget = [0,0,0,0]
    big_non_npo = []
    big_npo = []
    for line in obj.csvread:
        obj.line = line
        try:
            amount = AMOUNT.index( obj.get_data('budget') )
        except:
            print 'No match: ' + obj.get_data('budget')
        if obj.get_data('name').startswith('(特定)'):
            npo += 1
            npo_budget[ amount ] += 1
            if amount == 3:
                founding = obj.get_data('founding')
                entity_type = obj.get_data('name')
                big_npo.append( (founding, entity_type) )
        else:
            non_npo += 1
            non_npo_budget[ amount ] += 1
            if amount == 3:
                founding = obj.get_data('founding')
                entity_type = obj.get_data('name')
                big_non_npo.append( (founding, entity_type) )
            
    print 'NPOs: %d' %npo
    print '  0-100: %d' %npo_budget[0]
    print '  100-1000: %d' %npo_budget[1]
    print '  1000-10000: %d' %npo_budget[2]
    print '  10000+: %d' %npo_budget[3]
    print '(year of founding of the biggest ones)'
    big_npo.sort()
    for item in big_npo:
        print '%s  %s' % item
    print ''
    print 'Non-NPOs: %d' %non_npo
    print '  0-100: %d' %non_npo_budget[0]
    print '  100-1000: %d' %non_npo_budget[1]
    print '  1000-10000: %d' %non_npo_budget[2]
    print '  10000+: %d' %non_npo_budget[3]
    print '(year of founding of the biggest ones)'
    big_non_npo.sort()
    for item in big_non_npo:
        print '%s  %s' % item
    
    