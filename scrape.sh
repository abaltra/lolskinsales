#!/bin/bash

rm tmp/*
pwd=$(pwd)
cd champions-data-getter
python getChampionsData.py
cd ..
cd url-getter
scrapy crawl urlgetter -o $pwd/tmp/items.json -t json
cd ..
cd skingetter
scrapy crawl skingetter -a file_path=$pwd/tmp/items.json
