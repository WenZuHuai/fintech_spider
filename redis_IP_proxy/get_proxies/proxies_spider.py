#!/usr/bin/env python3
# coding: utf-8
# File: proxies_spider.py
# Author: lxw
# Date: 4/26/17 3:13 PM

from scrapy import cmdline

# cmdline.execute("scrapy crawl daili66_spider -L WARNING".split())
cmdline.execute("scrapy crawl next_page_spider -L WARNING".split())
