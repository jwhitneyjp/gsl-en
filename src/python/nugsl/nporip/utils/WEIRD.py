#!/usr/bin/python
#-*- encoding: utf8 -*-

text1 = list ('きょうとＣＡＰ〜子どもの人権・暴力防止〜'.decode('utf8') )
text2 = list ('きょうとＣＡＰ～子どもの人権・暴力防止～'.decode('utf8') )

for pos in range(0,len(text1),1):
    if text1[pos] != text2[pos]:
        print '%s\n  orig: %d\n  add: %d' % (text1[pos],ord(text1[pos]), ord(text2[pos])) 