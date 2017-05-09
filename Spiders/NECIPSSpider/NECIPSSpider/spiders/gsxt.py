# -*- coding: utf-8 -*-
import scrapy
import NECIPSSpider.utils
from NECIPSSPider.NECIPSSPider.utils import geetestcrack
import csv
import sys
class GsxtSpider(scrapy.Spider):
    name = 'gsxt'
    allowed_domains = ['gsxt.gov.cn']
    start_urls = ['http://www.gsxt.gov.cn/index.html']

    def parse(self, response):
        print(sys.path)
        with open("companyList.csv") as fp:
            for each in fp:
                print(each)
