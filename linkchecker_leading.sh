#!/bin/bash


linkchecker \
            --timeout=5 \
	    -Fhtml/UTF-8/linkcheck_leading.html \
	    --ignore-url=^mailto: \
	    http://www.cus-ymctest.com/kariup/Nagoya-Leading/index.html
