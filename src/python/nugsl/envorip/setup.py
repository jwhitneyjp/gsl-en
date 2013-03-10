#!/usr/bin/env python

from distutils.core import setup

long_description='''
Rip contents of the Japanese national registry of
NPOs to a CSV file for onward processing.
'''.strip()

setup(name='nugsl-envorip',
      version='1.0',
      description='Rip Japan Kankyo NGO Soran to CSV',
      author='Frank Bennett',
      author_email='biercenator@gmail.com',
      maintainer='Frank Bennett',
      maintainer_email='biercenator@gmail.com',
      url='http://gsl-nagoya-u.net/',
      packages=['nugsl','nugsl.envorip'],
      provides=['nugsl.envorip'],
      package_dir={'nugsl':''},
      long_description=long_description,
      platforms=['any'],
      scripts=['scripts/nugsl-envorip'],
      license='http://www.gnu.org/copyleft/gpl.html'
      )
