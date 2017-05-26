#!/usr/bin/env python3
# coding: utf-8
# File: runCJOAbbrFullSpider.py
# Author: lxw
# Date: 5/11/17 3:56 PM

# Supporting:
# 1. User-Agent
# 2. IP Proxy(API: http://datazhiyuan.com:60001/plain)


import json
from scrapy import cmdline
import sys
# from Spiders.CJOSpider.CJOSpider.spiders.CJOSpider import CJOSpider   # 这里有这条语句的话, 会导致所有logger的数据打印两次

sys.path.append("/home/lxw/IT/projects/fintech_spider")
sys.path.append("/home/lxw/IT/projects/fintech_spider/Spiders/CJOSpider")


cmdline.execute("scrapy crawl CJOSpider -L WARNING".split())

# redis-cli -h 192.168.1.29
# mongo 192.168.1.36:27017


"""
# Test
cjospider = CJOSpider()
# doc_id = "26286a27-bdad-4142-9479-da759996ae0f"   # 孙丽娜
# doc_id = "62d93ccb-38ca-408e-9e8f-b6a588c55b1f"   # 证券虚假
doc_id = "02010b5f-4d04-4997-8818-460d57a66803" # 上诉人昆明雨柠电子工程
result = cjospider.get_detail(doc_id, {})
print(type(result), result)
result = json.loads(result)
result = json.loads(result)
print(type(result), result)
"""
