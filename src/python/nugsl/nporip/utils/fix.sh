#!/bin/bash

rm -f *.ppm

pdftoppm financials/pdf/naikakufu/$1.pdf TEST

for i in *.ppm; do
  BASE=`basename $i .ppm`
  unpaper -bn h -bs 1 -bd 150 -bp 1 -bt 0.9 -bi 5 --overwrite $i TEST-unpaper.ppm
  gocr -l 200 -m 130 -a 100 -l 200 -C 0123456789収,l TEST-unpaper.ppm
  echo '1) Add to stoplist'
  read hello
  if [ "${hello}" == "1" ]; then
    echo 'Adding to stoplist!'
    echo ${BASE} >> financials/stoplist/naikakufu.txt
  fi
done
