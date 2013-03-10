#!/usr/bin/env python

from distutils.core import setup

long_description='''
This program generates bills in the form required
for billing software project work to Nagoya University.
'''.strip()

templates = []
templates.append('templates/seikyuu_template.odt')
templates.append('templates/houkoku_template.odt')
templates.append('templates/mitsumori_template.odt')

setup(name='nugsl-sitebills',
      version='1.1',
      description='Generate bills for support contract',
      author='Frank Bennett',
      author_email='biercenator@gmail.com',
      maintainer='Frank Bennett',
      maintainer_email='biercenator@gmail.com',
      url='http://gsl-nagoya-u.net/',
      requires=['nugsl.datetool','nugsl.mergetool'],
      scripts=['scripts/nugsl-sitebills'],
      data_files=[('share/nugsl-mergetool/templates',templates)],
      long_description=long_description,
      platforms=['any'],
      license='http://www.gnu.org/copyleft/gpl.html'
      )
