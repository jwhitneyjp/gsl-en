''' Module
'''

from PursueTotals import assumptionSpec
import csv

class Report:
    
    def __init__(self, category_hinter, filename):
        self.spec = assumptionSpec()
        self.categories = []
        self.set_categories( category_hinter )
        self.filename = filename

    def generate_report(self, name, results):
        self.name = name
        self.results = results
        self.compile_report()
        self.write_report( name )

    def write_headings(self):
        ofh = open(self.filename,'a+')
        c = csv.writer( ofh )
        row = []
        row.append('Name')
        row.append( 'Grand total' )
        for section in ['Unknown'] + self.sections:
            row.append( section + ' (total)' )
            row.append( section + ' (total_count)' )
            row.append( section + ' (entries)' )
        row.append('max_value')
        row.append('assumptions')
        row.append('specs')
        row.append('retries')
        c.writerow( row )
        ofh.close()

    def set_categories(self, category_hinter ):
        self.category = {}
        sections = category_hinter.sections()
        sections.remove('Start')
        sections.remove('End')
        sections.remove('Total')
        for category in ['Unknown'] + sections:
            self.category[category] = {}
            self.category[category]['total'] = 0
            self.category[category]['total_count'] = 0
            self.category[category]['entries'] = 0
        self.category['Grand total'] = 'nil'
        self.sections = sections

    def write_report(self, name):
        ofh = open(self.filename,'a+')
        c = csv.writer( ofh )
        row = []
        row.append(name)
        row.append( self.category['Grand total'] )
        for section in ['Unknown'] + self.sections:
            row.append( self.category[section]['total'] )
            row.append( self.category[section]['total_count'] )
            row.append( self.category[section]['entries'] )
        row.append( self.results.max_value )
        row.append( self.results.assumptions_count )
        row.append( self.results.specs_count )
        row.append( self.results.retries_count)
        c.writerow( row )
        ofh.close()

    def compile_report(self):
        for num in self.results:
            
            mycategory = num.info['nontotal']

            if num.state() == self.spec.GRAND_TOTAL:
                self.category['Grand total'] = num
            elif num.state() == self.spec.TOTAL:
                self.category[mycategory]['total'] += num
                self.category[mycategory]['total_count'] += 1
            else:
                self.category[mycategory]['entries'] += 1
