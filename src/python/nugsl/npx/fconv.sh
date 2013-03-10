#!/bin/bash

test -f $1.ps || exit 0

echo 'Running'
pstopnm -xsize 3600 $1.ps
ppmtopgm ${1}001.ppm | pgmtopbm > $1.pbm
pnmtotiff -g4 $1.pbm > $1.tif
rm ${1}001.ppm
rm $1.pbm
echo 'Hit ENTER to generate box file'
read hello
tesseract $1.tif $1 -l npx batch.nochop makebox
mv $1.txt $1.box

echo 'Hit ENTER again to delete ps file'
read hello2
rm $1.ps
