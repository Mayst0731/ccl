#!/bin/bash
cd detail/detail_3333/detail_3333
scrapy crawl detail -O ../../../file_store/detail_1.json
cd ../../..
python3 main.py

# output will be inside file_store/ directory
