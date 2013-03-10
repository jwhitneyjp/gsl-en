#!/usr/bin/env python

from distutils.core import setup

long_description='''
These are useful data manipulation functions
adapted from code copied from ActiveState.
A link to the location of the original author's
posting is included in the source code file.
'''.strip()

setup(name='nugsl-datetool',
      version='1.2',
      description='Handy date functions ripped off from elsewhere',
      author='Frank Bennett',
      author_email='biercenator@gmail.com',
      url='http://gsl-nagoya-u.net/',
      packages=['nugsl','nugsl.datetool'],
      provides=['nugsl.datetool'],
      package_dir={'nugsl':''},
      license='http://www.gnu.org/copyleft/gpl.html',
      platforms=['any'],
      long_description=long_description
      )
