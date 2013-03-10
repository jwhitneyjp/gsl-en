#!/bin/bash


linkchecker -q \
            --timeout=5 \
	    -Fhtml/UTF-8/nuaecheck.html \
	    --no-warnings \
	    --ignore-url=^mailto: \
	    http://nuae.nagoya-u.ac.jp/
