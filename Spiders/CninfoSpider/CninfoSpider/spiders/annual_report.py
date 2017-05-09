# -*- coding: utf-8 -*-
import scrapy


class AnnualReportSpider(scrapy.Spider):
    name = 'annual_report'
    allowed_domains = ['cninfo.com.cn']

    def start_requests(self):
        for page_num in range()
    def parse(self, response):
        pass
