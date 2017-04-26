#!/usr/bin/env python3
# coding: utf-8
# File: main.py.py
# Author: lxw
# Date: 4/20/17 2:51 PM

from scrapy import cmdline

# cmdline.execute(["scrapy", "crawl", "new_three_board", "-L", "WARNING"])
cmdline.execute(["scrapy", "crawl", "neeq", "-L", "WARNING"])

# for i in range(10):
#     print(i)
