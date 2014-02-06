#!/bin/bash

echo Usage: scriptname.sh --help
echo Usage: scriptname.sh -l
echo "Usage: scriptname.sh <comma_delimited_list_of_names>"

if [ "" == "$1" ]; then
  ./src/python/bin/staffblast.py --help
elif [ "-l" == "$1" ]; then
  ./src/python/bin/staffblast.py -l
else
  echo $1
  ./src/python/bin/staffblast.py -d -m hello.txt -f status,family_name,given_name,proper_name,birthdate,field,affiliation,phone,office,office_hours,photo_web_ok,email,email_disclose_ok,website,degrees,career_history,research_interests,memberships,visitorships,publications,recommended_readings,preparation_suggestions \
    -r $1
fi
