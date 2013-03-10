#!/usr/bin/python

from nugsl.renumerate.Report import Report
from nugsl.renumerate.CategoryHint import categoryHinter

ch = categoryHinter('config/test-jcategories.conf')

report = Report(ch,'headings.csv')
report.write_headings()