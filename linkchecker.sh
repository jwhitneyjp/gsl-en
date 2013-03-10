#!/bin/bash


linkchecker -q \
            --timeout=5 \
	    -Fhtml/UTF-8/linkcheck.html \
	    --no-warnings \
	    --ignore-url=^mailto: \
	    http://gsl-nagoya-u.net/
