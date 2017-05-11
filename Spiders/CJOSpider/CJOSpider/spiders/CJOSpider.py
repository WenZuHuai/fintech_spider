#!/usr/bin/env python3
# coding: utf-8
# File: CJOSpider.py
# Author: lxw
# Date: 5/11/17 3:57 PM

import scrapy


class CJOSpider(scrapy.Spider):
    """
    数据一直在增长，这个数据只是作为参考
    刑事案件: 4,764,067
    民事案件: 17,801,622
    行政案件: 968,183
    赔偿案件: 23,177
    执行案件: 5,283,286
    """

    name = 'cjo'

    """
    # Just for test.
    start_urls = [
        "http://ipecho.net/plain",
        "http://www.cnblogs.com/lxw0109",
        "https://kangzubin.com/",
    ]
    """
    start_urls = [
        "http://wenshu.court.gov.cn/List/List?sorttype=1&conditions=searchWord+1+AJLX++%E6%A1%88%E4%BB%B6%E7%B1%BB%E5%9E%8B:%E5%88%91%E4%BA%8B%E6%A1%88%E4%BB%B6",  # 刑事案件
        # "http://wenshu.court.gov.cn/List/List?sorttype=1&conditions=searchWord+2+AJLX++%E6%A1%88%E4%BB%B6%E7%B1%BB%E5%9E%8B:%E6%B0%91%E4%BA%8B%E6%A1%88%E4%BB%B6", # 民事案件
        # "http://wenshu.court.gov.cn/List/List?sorttype=1&conditions=searchWord+3+AJLX++%E6%A1%88%E4%BB%B6%E7%B1%BB%E5%9E%8B:%E8%A1%8C%E6%94%BF%E6%A1%88%E4%BB%B6", # 行政案件
        # "http://wenshu.court.gov.cn/List/List?sorttype=1&conditions=searchWord+4+AJLX++%E6%A1%88%E4%BB%B6%E7%B1%BB%E5%9E%8B:%E8%B5%94%E5%81%BF%E6%A1%88%E4%BB%B6", # 赔偿案件
        # "http://wenshu.court.gov.cn/List/List?sorttype=1&conditions=searchWord+5+AJLX++%E6%A1%88%E4%BB%B6%E7%B1%BB%E5%9E%8B:%E6%89%A7%E8%A1%8C%E6%A1%88%E4%BB%B6", # 执行案件
    ]

    def parse(self, response):
        """
        先按序请求各个start_url， 然后才会进入到parse中(可能是异步处理的，当start_urls比较多时，可能先进入parse? 待确定, 内部实现细节和工作原理)
        """
        print("response.body:", response.body.decode("utf-8"))
        print("response.url:", response.url)

        # yield scrapy.Request(url="http://xiaoweiliu.cn/", callback=self.parse)  # yield多次，但该url只爬取一次，自动去重
