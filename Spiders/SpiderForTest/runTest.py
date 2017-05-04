#!/usr/bin/env python3
# coding: utf-8
# File: proxies_spider.py
# Author: lxw
# Date: 4/20/17 2:51 PM

from scrapy import cmdline

# Supporting:
# User-Agent
# IP Proxy(API: http://datazhiyuan.com:60001/plain)

cmdline.execute("scrapy crawl test_proxy_pool_api -L WARNING".split())

