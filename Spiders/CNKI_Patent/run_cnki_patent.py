#!/usr/bin/env python3
# coding: utf-8
# File: run_cnki_patent.py
# Author: lxw
# Date: 5/26/17 4:06 PM

# Supporting:
# 1. User-Agent
# 2. IP Proxy(API: http://datazhiyuan.com:60001/plain)


from scrapy import cmdline
import sys

sys.path.append("/home/lxw/IT/projects/fintech_spider")
sys.path.append("/home/lxw/IT/projects/fintech_spider/Spiders/CNKI_Patent")

cmdline.execute("scrapy crawl cnki_patent -L WARNING".split())

# redis-cli -h 192.168.1.29
# mongo 192.168.1.36:27017