#!/usr/bin/env python

from distutils.core import setup

long_description='''
This program creates a spec file for use with
TaskJuggler III, suitable for coordinating
preparation work for the Intercollegiate
Negotiation Competition held each year at Sophia 
University in Tokyo.  To convert the spec file
into a set of pretty Web-based reports, you
need to have TaskJuggler III installed.
'''.strip()

templates = []
templates.append('templates/negotasks.tjp')

setup(name='nugsl-negotasks',
      version='1.3',
      description='TaskJugger III spec file generator',
      author='Frank Bennett',
      author_email='biercenator@gmail.com',
      maintainer='Frank Bennett',
      maintainer_email='biercenator@gmail.com',
      url='http://gsl-nagoya-u.net/',
      packages=['nugsl','nugsl.negotasks'],
      requires=['nugsl.parsetool'],
      provides=['nugsl.negotasks'],
      scripts=['scripts/nugsl-negotasks'],
      package_dir={'nugsl':''},
      data_files=[('share/nugsl-negotasks/templates',templates)],
      long_description=long_description,
      platforms=['any'],
      license='http://www.gnu.org/copyleft/gpl.html'
      )
