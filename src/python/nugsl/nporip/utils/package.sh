#!/bin/bash

convmv -f utf8 -t shift-jis --notest final/*
rm final.zip
zip final.zip final/*
convmv -f shift-jis -t utf8 --notest final/*
