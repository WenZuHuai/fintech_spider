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
    # start_urls = ['http://www.gsxt.gov.cn/index.html']
    # start_urls = ["http://xiaoweiliu.cn"]
    start_urls = ["http://ipecho.net/plain"]

    def parse(self, response):
        # print("response.body:", response.body.decode("utf-8"))
        print("Your Accessing IP Address is:", response.xpath('//pre/text()').extract_first())
        """
        print(sys.path)
        print(os.getcwd())  # /home/lxw/IT/projects/fintech_spider/Spiders/NECIPSSpider
        with open("./NECIPSSpider/utils/companyList.csv") as fp:
            for each in fp:
                print(each, end="")
        """
