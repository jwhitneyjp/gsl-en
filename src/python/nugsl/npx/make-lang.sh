#/bin/bash


echo 'box training ...'
for i in *.tif; do
    echo $i
    base=`basename $i .tif`
    tesseract $i junk -l npo nobatch box.train
    cat ${base}.tr | sed -e "s/UnknownFont/${base}/g" > ${base}.NEWTR
    mv ${base}.NEWTR ${base}.tr
done

echo 'mftraining ...'
mftraining *.tr

echo 'cntraining ...'
cntraining *.tr

echo 'uncharset extracting ...'
unicharset_extractor *.box

echo 'renaming new files ...'
mv inttemp npx.inttemp
mv normproto npx.normproto
mv pffmtable npx.pffmtable
mv unicharset npx.unicharset
wordlist2dawg words_list npx.word-dawg
wordlist2dawg frequent_words_list npx.freq-dawg
cp DangAmbigs npx.DangAmbigs
touch npx.user-words

rm *.tr

sudo mv npx.* /usr/local/share/tessdata/
