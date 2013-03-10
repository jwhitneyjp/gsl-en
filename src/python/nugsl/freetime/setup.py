#!/usr/bin/env python

from distutils.core import setup

long_description='''
A simple calendar tool for sharing available and unavailable
meeting times.
'''.strip()

configs = []
configs.append('config/profile-default.txt')
configs.append('config/repeat.png')
configs.append('config/empty.png')
configs.append('config/right.png')
configs.append('config/left.png')
configs.append('config/times-c.txt')
configs.append('config/times-jp.txt')
configs.append('config/times-en.txt')
configs.append('config/weekdays-c.txt')
configs.append('config/weekdays-jp.txt')
configs.append('config/weekdays-en.txt')
configs.append('config/known_hosts')
configs.append('config/groups-default.txt')

setup(name='nugsl-freetime',
      version='1.8',
      description='Simple schedule coordination tool',
      author='Frank Bennett',
      author_email='biercenator@gmail.com',
      maintainer='Frank Bennett',
      maintainer_email='biercenator@gmail.com',
      url='http://gsl-nagoya-u.net/',
      scripts=['scripts/nugsl-freetime'],
      data_files=[('share/nugsl-freetime',configs)],
      packages=['nugsl','nugsl.freetime'],
      provides=['nugsl.freetime'],
      package_dir={'nugsl':''},
      long_description=long_description,
      platforms=['any'],
      license='http://www.gnu.org/copyleft/gpl.html'
      )
