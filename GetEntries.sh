#/bin/bash

cd ..
wget --no-check-certificate -O gsl-frontpage-master.zip https://github.com/fbennett/gsl-frontpage/archive/master.zip
rm -fR gsl-frontpage-master
mkdir gsl-frontpage-master
mkdir gsl-frontpage-master/Alert
mkdir gsl-frontpage-master/News
mkdir gsl-frontpage-master/Events
unzip gsl-frontpage-master.zip
