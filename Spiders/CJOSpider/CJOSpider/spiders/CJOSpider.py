#!/usr/bin/env python3
# coding: utf-8
# File: CJOSpider.py
# Author: lxw
# Date: 5/11/17 3:57 PM

import scrapy


class CJOSpider(scrapy.Spider):
    name = 'cjo'

    start_urls = ["http://ipecho.net/plain"]

    def parse(self, response):
        print("response.body:", response.body.decode("utf-8"))
