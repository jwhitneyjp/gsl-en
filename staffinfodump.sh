#!/bin/bash

src/python/bin/staffblast.py -d -f status,family_name,given_name,proper_name,birthdate,field,affiliation,phone,office,office_hours,photo_web_ok,email,email_disclose_ok,website,degrees,career_history,research_interests,memberships,visitorships,publications,recommended_readings,preparation_suggestions -r $1

