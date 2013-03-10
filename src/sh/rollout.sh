#!/usr/local/bin/bash

#
# mod_gzip is currently turned off.  It does not
# play well with the mod_rewrite stuff.
#

ZIPIT=`pwd`/zipit.sh

sudo /usr/local/etc/rc.d/apache.sh start

cd /home/production/staging/gsl-en
svn update

cd /home/production/staging/gsl-en
sudo rm -fR release
./Install

sudo cp src/apache/httpd.conf.staging /usr/local/apache/conf/httpd.conf
sudo mkdir release/docroot/cgi-bin
sudo chown frontpage:www release/docroot/cgi-bin
sudo cp /home/frontpage/content/pyblosxom.cgi release/docroot/cgi-bin
sudo chown frontpage:www release/docroot/cgi-bin/pyblosxom.cgi
sudo chmod uog+x release/docroot/cgi-bin/pyblosxom.cgi
sudo apachectl graceful

sudo rsync -a --delete release/docroot/* ../../final/gsl-en/release/docroot/*

find ../../final/gsl-en/release/docroot/ -name '*.html' -exec $ZIPIT {} \;
sudo cp src/apache/httpd.conf.final /usr/local/apache/conf/httpd.conf
sudo apachectl graceful
