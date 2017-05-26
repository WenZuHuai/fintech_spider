#!/usr/bin/env python3
# coding: utf-8
# File: temp.py
# Author: lxw
# Date: 5/26/17 4:03 PM

import scrapy


class CnkiPatentSpider(scrapy.Spider):
    name = "cnki_patent"
    start_urls = ['http://www.cnki.net/']

    def parse(self, response):
        print(response.text)
