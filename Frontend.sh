#!/bin/bash

set -e

rm -fR prerendered/*

python src/pyblosxom/content/pyblosxom.cgi staticrender --config=src/pyblosxom/content
#pyblosxom-cmd staticrender --config=src/pyblosxom/content

rm -fR release/docroot/Alert
rm -fR release/docroot/Events
rm -fR release/docroot/News

if [ -d ../gsl-prerendered/Alert ]; then
  cp -R ../gsl-prerendered/Alert release/docroot
fi

if [ -d ../gsl-prerendered/Events ]; then
  cp -R ../gsl-prerendered/Events release/docroot
fi

if [ -d ../gsl-prerendered/News ]; then
  cp -R ../gsl-prerendered/News release/docroot
fi

cp ../gsl-prerendered/index.html release/docroot
cp ../gsl-prerendered/index.atom release/docroot
cp ../gsl-prerendered/index.rss release/docroot
