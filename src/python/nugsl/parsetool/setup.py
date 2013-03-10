#!/usr/bin/env python

from distutils.core import setup

long_description = '''
This package forms a part of the oomerge utilities
in the NUGSL (Nagoya University Graduate School of Law)
utility suite.  It can be used to extract the content
of an Excel file, for use as an array in memory, or
for dumping as a CSV file.  Options support the extraction
of data from files structured in a number of ways.  The
code is still in a rough state.
'''.strip()

setup(name='nugsl-parsetool',
      version='1.3',
      description='Extract CSV and array data from XLS file',
      author='Frank Bennett',
      author_email='biercenator@gmail.com',
      maintainer='Frank Bennett',
      maintainer_email='biercenator@gmail.com',
      url='http://gsl-nagoya-u.net/',
      packages=['nugsl','nugsl.parsetool'],
      requires=['pyExcelerator'],
      provides=['gsl.parsetool'],
      package_dir={'nugsl':''},
      long_description=long_description,
      platforms=['any'],
      license='http://www.gnu.org/copyleft/gpl.html'
      )
