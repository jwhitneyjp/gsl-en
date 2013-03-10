#!/usr/bin/env python

from distutils.core import setup

long_description='''
This package provides simple support for merging
multiple copies of a single Open Office file
from a list of maps.  The merged content is
written into a single file.
'''.strip()

setup(name='nugsl-merge',
      version='1.1',
      description='Simple Open Office merge utility',
      author='Frank Bennett',
      author_email='biercenator@gmail.com',
      maintainer='Frank Bennett',
      maintainer_email='biercenator@gmail.com',
      url='http://gsl-nagoya-u.net/',
      packages=['nugsl','nugsl.mergetool'],
      package_dir={'nugsl':''},
      requires=['zipfile'],
      provides=['nugsl.mergetool'],
      long_description=long_description,
      platforms=['any'],
      license='http://www.gnu.org/copyleft/gpl.html'
      )
