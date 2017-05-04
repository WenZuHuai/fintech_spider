#!/usr/bin/env python3
# coding: utf-8
# File: testProxyPool.py
# Author: lxw
# Date: 4/27/17 3:17 PM
"""
Test the User-Agent and Proxy. Works well.
"""

import scrapy


class ProxyPoolTest(scrapy.Spider):
    name = "test_proxy_pool_api"

    # start_urls = ["http://xiujinniu.com/xiujinniu/index.php"]
    # start_urls = ["http://xiaoweiliu.cn"]
    start_urls = ["http://ipecho.net/plain"]

    def parse(self, response):
        # print("repsonse.headers:", response.headers)
        print("response.body:", response.body.decode("utf-8"))
        # print("Request:", response.request.headers)     # User-Agent does work

        """
        Scrapy w/o User-Agent:
        {
            "Accept":[
                "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
            ],
            "Accept-Language":[
                "en"
            ],
            "User-Agent":[
                "Scrapy/1.3.3 (+http://scrapy.org)"
            ],
            "Accept-Encoding":[
                "gzip,deflate"
            ]
        }
        
        Scrapy with RANDOM User-Agent:
        {
            "Accept":[
                "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
            ],
            "Accept-Language":[
                "en"
            ],
            "User-Agent":[
                "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3"
            ],
            "Accept-Encoding":[
                "gzip,deflate"
            ]
        }
        """
