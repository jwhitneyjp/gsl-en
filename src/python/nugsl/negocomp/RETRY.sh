#!/bin/bash

rm ~/.nugsl-mergetool/cards_template.odt
rm ~/.nugsl-mergetool/arbplates_template.odt
rm ~/.nugsl-mergetool/negoplates_template.odt
cd ../parsetool
sudo python ./setup.py install
cd ../negocomp
sudo python ./setup.py install
echo Merging ...
nugsl-negomerge -C 2 -E '.*Gab.*' -c 10 -f ~/Desktop/Work/NegoComp/FrankMaterials/第６回登録シート_Nagoya.xls
#nugsl-negomerge -c 1 -f ~/Desktop/Work/NegoComp/FrankMaterials/第６回登録シート_Nagoya.xls
