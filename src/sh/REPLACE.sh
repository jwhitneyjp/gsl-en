#!/bin/bash

for f in *.txt; do
  BASE=`basename $f .txt`
  echo $BASE
  cat ${BASE}.txt | sed -e 's~/extra~/materials~' > ${BASE}.new
  mv ${BASE}.new ${BASE}.txt
done
