#!/usr/bin/env python3
# coding: utf-8
# File: runCJOAbbrFullSpider.py
# Author: lxw
# Date: 5/11/17 3:56 PM

# Supporting:
# 1. User-Agent
# 2. IP Proxy(API: http://datazhiyuan.com:60001/plain)
# 3. Redis(As message Queue)/MongoDB(As database)


import json
from scrapy import cmdline
import sys
# from Spiders.CJOSpider.CJOSpider.spiders.CJOSpider import CJOSpider   # 这里有这条语句的话, 会导致所有logger的数据打印两次

sys.path.append("/home/lxw/IT/projects/fintech_spider")
sys.path.append("/home/lxw/IT/projects/fintech_spider/Spiders/CJODocIDSpider")


cmdline.execute("scrapy crawl CJODocIDSpider -L WARNING".split())

# redis-cli -h 192.168.1.29
# mongo 192.168.1.36:27017
