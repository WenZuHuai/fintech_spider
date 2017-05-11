#!/usr/bin/env python3
# coding: utf-8
# File: run_CJOSpider.py
# Author: lxw
# Date: 5/11/17 3:56 PM


from scrapy import cmdline

cmdline.execute(["scrapy", "crawl", "cjo", "-L", "WARNING"])