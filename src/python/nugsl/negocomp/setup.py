#!/usr/bin/env python

from distutils.core import setup

long_description='''
This program creates a set of name cards and name
plates for use in the Intercollegiate Negotiation
Competition held each year at Sophia University in
Tokyo.  The number of name cards created for each
group can be controlled via parameters.  Creating
cards for individual members or groups is also
supported.
'''.strip()

templates = []
templates.append('templates/cards_template.odt')
templates.append('templates/arbplates_template.odt')
templates.append('templates/negoplates_template.odt')

setup(name='nugsl-negocomp',
      version='1.4',
      description='Merge utility for name tags and nameplates',
      author='Frank Bennett',
      author_email='biercenator@gmail.com',
      maintainer='Frank Bennett',
      maintainer_email='biercenator@gmail.com',
      url='http://gsl-nagoya-u.net/',
      packages=['nugsl','nugsl.negocomp'],
      requires=['nugsl.mergetool','nugsl.parsetool'],
      provides=['gsl.negocomp'],
      scripts=['scripts/nugsl-negomerge'],
      package_dir={'nugsl':''},
      data_files=[('share/nugsl-mergetool/templates',templates)],
      long_description=long_description,
      platforms=['any'],
      license='http://www.gnu.org/copyleft/gpl.html'
      )
