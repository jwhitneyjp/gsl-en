#!/bin/bash
find ./docroot -type d -exec chmod uog+x {} \;
find ./docroot -exec chmod uog+r {} \;
rsync -av ./docroot/ en@law.nagoya-u.ac.jp:/var/www/html/en
