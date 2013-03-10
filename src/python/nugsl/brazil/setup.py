#!/usr/bin/env python

from distutils.core import setup

long_description='''
A software suite for downloading tables published by the Brazilian Congress
on the progress of Presidential orders through the constitutionally mandated
approval process.
'''.strip()

configs = ['config/brazil-dist.conf']
configs.append('config/headings-pre.conf')
configs.append('config/headings-post.conf')

setup(name='nugsl-brazil',
      version='1.1',
      description='Convert Brazilian Congress statutory tables to database form',
      author='Frank Bennett',
      author_email='biercenator@gmail.com',
      maintainer='Frank Bennett',
      maintainer_email='biercenator@gmail.com',
      url='http://gsl-nagoya-u.net/',
      scripts=['scripts/nugsl-brazil-grab','scripts/nugsl-brazil-convert','scripts/nugsl-brazil-import'],
      data_files=[('share/nugsl-brazil',configs)],
      packages=['nugsl','nugsl.brazil'],
      provides=['nugsl.brazil'],
      package_dir={'nugsl':''},
      long_description=long_description,
      platforms=['any'],
      license='http://www.gnu.org/copyleft/gpl.html'
      )
