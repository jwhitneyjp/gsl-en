#!/usr/bin/env python

from distutils.core import setup

long_description='''
Cleans and validates financial statements and other data containing
totals and grand totals.  This tool was originally designed to
extract classified income totals from OCR scans of the financial statements of
Japanese non-profit organizations, but the design is fairly general and
may find other applications.
'''.strip()

configs = []
configs.append('config/test-jcategories.conf')
configs.append('config/test-categories.conf')
configs.append('config/finish.png')
configs.append('config/renumerate-default.conf')
configs.append('config/tess.conf')

setup(name='nugsl-renumerate',
      version='1.8',
      description='Extract totals from plain text data',
      author='Frank Bennett',
      author_email='biercenator@gmail.com',
      maintainer='Frank Bennett',
      maintainer_email='biercenator@gmail.com',
      url='http://gsl-nagoya-u.net/',
      scripts=['scripts/nugsl-validate','scripts/nugsl-renumerate'],
      data_files=[('share/nugsl-renumerate/config',configs)],
      packages=['nugsl','nugsl.renumerate'],
      provides=['nugsl.renumerate'],
      package_dir={'nugsl':''},
      long_description=long_description,
      platforms=['any'],
      license='http://www.gnu.org/copyleft/gpl.html'
      )
