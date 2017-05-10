# -*- coding: utf-8 -*-

import csv
import os
import scrapy
import sys

from ..utils import geetestcrack

# from NECIPSSpider.utils import geetestcrack # YES
# from NECIPSSpider.NECIPSSpider.utils import geetestcrack    # NO


class GsxtSpider(scrapy.Spider):
    name = 'gsxt'
    # allowed_domains = ['gsxt.gov.cn']
    # start_urls = ["http://xiaoweiliu.cn"]
    # start_urls = ["http://ipecho.net/plain"]

    url = "http://www.gsxt.gov.cn/index.html"

    def start_requests(self):
        # print(sys.path)
        # print(os.getcwd())  # /home/lxw/IT/projects/fintech_spider/Spiders/NECIPSSpider
        with open("./NECIPSSpider/utils/companyList.csv") as fp:
            while 1:
                line = fp.readline()
                if not line:
                    break
                line = line.strip()
                line_list = line.split(",")
                if len(line_list) > 1:
                    print(type(line_list[1]))
                    yield scrapy.Request(url=self.url+line_list[1], callback=self.parse)

    def parse(self, response):
        print("response.body:", response.body.decode("utf-8"))
        # print("Your Accessing IP Address is:", response.xpath('//pre/text()').extract_first())
