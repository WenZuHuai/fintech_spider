#!/usr/bin/env python3
# coding: utf-8
# File: com_code_name_addr.py
# Author: lxw
# Date: 4/20/17 1:57 PM

import scrapy
from new_three_board import items


class NewThreeBoard(scrapy.Spider):
    """
    新三板在线(http://www.chinaipo.com/listed)
    """
    name = "new_three_board"

    def start_requests(self):
        # page_count = 573
        page_count = 1
        for page in range(1, page_count+1):
            url = "http://www.chinaipo.com/listed/?p={0}".format(page)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        row_list = response.xpath("//tbody/tr")
        for row in row_list[1:]:
            tds = row.xpath("td")   # <class 'scrapy.selector.unified.SelectorList'>
            ntbi = items.NewThreeBoardItem()
            field_list = ["com_code", "com_detail_link", "com_name", "listing_date", "method_of_transfer", "registered_capital", "primary_business", "province", "zbqs", "zss", "accounting_firm", "law_firm", "csrc"]
            for index, td in enumerate(tds):
                ntbi[field_list[index]] = td.xpath("string(.)").extract()

            print(len(field_list))  # 13
            try:
                assert len(field_list) == len(content)
            except Exception as e:
                print("lxw_AssertError: {0}. len(field_list) != len(content)".format(content[0]))

            #yield ntbi
            #break



