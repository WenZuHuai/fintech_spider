#!/usr/bin/env python3
# coding: utf-8
# File: phantomjs_scrapy_demo.py
# Author: lxw
# Date: 5/5/17 11:09 AM

import chardet
import codecs
import scrapy


class PhantomJSScrapyDemo(scrapy.Spider):
    name = "phantomjs_scrapy"

    # start_urls = ["https://search.jd.com/Search?keyword=http%E6%9D%83%E5%A8%81%E6%8C%87%E5%8D%97&enc=utf-8&wq=http%E6%9D%83%E5%A8%81%E6%8C%87%E5%8D%97&pvid=2951aaa42692435ca955c34171d6a380"]
    # start_urls = ["https://item.jd.com/11056556.html"]
    start_urls = ["http://roll.news.qq.com/"]   # js

    def parse(self, response):
        # print(type(response.body))    # bytes
        result = response.body
        code_detect = chardet.detect(response.body)['encoding']
        # code_detect = chardet.detect(result)['encoding']
        # print(code_detect)
        if code_detect:
            html = result.decode(code_detect, 'ignore')
        else:
            html = result.decode("utf-8", 'ignore')

        print(html)
        f = codecs.open("/home/lxw/phantomjs_result.html", "w")
        f.write(html)

        """
        with open("/home/lxw/phantomjs_result.html", "w") as f:
            # f.write(response.body.decode("utf-8"))    # UnicodeDecodeError: 'utf-8' codec can't decode byte 0xa1 in position 137: invalid start byte
            f.write(html.encode())
        """
