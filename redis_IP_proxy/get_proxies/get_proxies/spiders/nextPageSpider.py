#!/usr/bin/env python3
# coding: utf-8
# File: nextPageSpider.py
# Author: lxw
# Date: 4/28/17 3:25 PM

import scrapy


class NextPageSpider(scrapy.Spider):
    """
    Just for test.
    """
    name = "next_page_spider"
    last_page = "index.html"
    start_urls = ["http://www.66ip.cn/areaindex_1/80.html"]

    def parse(self, response):
        next_page = response.css("#PageList .pageCurrent").xpath("following-sibling::a").css("::attr(href)").extract_first()
        print("Current_page:", NextPageSpider.last_page)
        print("Next_page:", next_page)

        if ".html" not in next_page:
            return

        NextPageSpider.last_page = next_page
        yield scrapy.Request(url="http://www.66ip.cn"+next_page, callback=self.parse)
        print("After yield")
