#!/usr/bin/env python3
# coding: utf-8
# File: proxies_spider.py
# Author: lxw
# Date: 4/20/17 2:51 PM

from scrapy import cmdline


cmdline.execute("scrapy crawl ProxyPoolTest_spider -L WARNING".split())

