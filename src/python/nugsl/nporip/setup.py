#!/usr/bin/env python

from distutils.core import setup

long_description='''
Rip contents of the Japanese national registry of
NPOs to a CSV file for onward processing.
'''.strip()

setup(name='nugsl-nporip',
      version='1.0',
      description='Rip Japanese NPO registry to CSV',
      author='Frank Bennett',
      author_email='biercenator@gmail.com',
      maintainer='Frank Bennett',
      maintainer_email='biercenator@gmail.com',
      url='http://gsl-nagoya-u.net/',
      packages=['nugsl','nugsl.nporip'],
      provides=['nugsl.nporip'],
      package_dir={'nugsl':''},
      long_description=long_description,
      platforms=['any'],
      scripts=['scripts/nugsl-nporip'],
      license='http://www.gnu.org/copyleft/gpl.html'
      )
