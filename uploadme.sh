#!/bin/bash

# http://support.google.com/a/bin/request.py?hl=en&contact_type=nonprofit

find ./release/docroot -type d -exec chmod uog+x {} \;
find ./release/docroot -exec chmod uog+r {} \;
rm -f ./release/docroot/en
rsync -av ./release/docroot/ en@law.nagoya-u.ac.jp:/var/www/html/en
