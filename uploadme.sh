#!/bin/bash

# http://support.google.com/a/bin/request.py?hl=en&contact_type=nonprofit

find ./release/docroot -type d -exec chmod uog+x {} \;
find ./release/docroot -exec chmod uog+r {} \;
rm -f ./release/docroot/en

rsync -av --rsh="/usr/bin/sshpass -f .sshpass.txt /usr/bin/ssh -l en" en@law.nagoya-u.ac.jp:/var/www/html/en/index.html ./release/docroot/index.html
rsync -av --rsh="sshpass -f .sshpass.txt /usr/bin/ssh -l en" law.nagoya-u.ac.jp:/var/www/html/en/calendar.ics ./release/docroot/calendar.ics
rsync -av --rsh="sshpass -f .sshpass.txt /usr/bin/ssh -l en" law.nagoya-u.ac.jp:/var/www/html/en/News/ ./release/docroot/News
rsync -av --rsh="sshpass -f .sshpass.txt /usr/bin/ssh -l en" law.nagoya-u.ac.jp:/var/www/html/en/Events/ ./release/docroot/Events

rsync -av --rsh="sshpass -f .sshpass.txt /usr/bin/ssh -l en" law.nagoya-u.ac.jp:/var/www/html/en/curriculum/owl/index.html ./release/docroot/curriculum/owl/index.html
rsync -av --rsh="sshpass -f .sshpass.txt /usr/bin/ssh -l en" law.nagoya-u.ac.jp:/var/www/html/en/curriculum/owl/calendar.ics ./release/docroot/curriculum/owl/calendar.ics
rsync -av --rsh="sshpass -f .sshpass.txt /usr/bin/ssh -l en" law.nagoya-u.ac.jp:/var/www/html/en/curriculum/owl/index.atom ./release/docroot/curriculum/owl/index.atom
rsync -av --rsh="sshpass -f .sshpass.txt /usr/bin/ssh -l en" law.nagoya-u.ac.jp:/var/www/html/en/curriculum/owl/News/ ./release/docroot/curriculum/owl/News
rsync -av --rsh="sshpass -f .sshpass.txt /usr/bin/ssh -l en" law.nagoya-u.ac.jp:/var/www/html/en/curriculum/owl/Events/ ./release/docroot/curriculum/owl/Events

rsync -av --rsh="sshpass -f .sshpass.txt /usr/bin/ssh -l en" ./release/docroot/ en@law.nagoya-u.ac.jp:/var/www/html/en
