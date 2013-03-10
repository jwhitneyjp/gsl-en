#!/bin/bash


linkchecker -q \
            --timeout=5 \
	    -Fhtml/UTF-8/nomologcheck.html \
	    --no-warnings \
	    --ignore-url=^mailto: \
	    http://www.law.nagoya-u.ac.jp/
