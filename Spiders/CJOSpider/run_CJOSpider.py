#!/usr/bin/env python3
# coding: utf-8
# File: run_CJOSpider.py
# Author: lxw
# Date: 5/11/17 3:56 PM

# Supporting:
# 0. CAPTCHA(1st Generation)
# 1. User-Agent
# 2. IP Proxy(API: http://datazhiyuan.com:60001/plain)


from scrapy import cmdline

# cmdline.execute(["scrapy", "crawl", "CJO_Spider", "-L", "WARNING"])
cmdline.execute("scrapy crawl CJO_Spider -L WARNING".split())
