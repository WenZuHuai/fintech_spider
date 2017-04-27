#!/usr/bin/env python3
# coding: utf-8
# File: daili66_spider.py
# Author: lxw
# Date: 4/26/17 2:56 PM

import redis
import scrapy

from redis_IP_proxy.proxy_interface import RedisClient
from redis_IP_proxy.utils import check_proxy_alive


class Daili66Spider(scrapy.Spider):
    name = "daili66_spider"
    page_count = 0
    proxy_db = RedisClient()
    start_urls = ["http://www.66ip.cn/index.html"]

    def parse(self, response):
        table = response.xpath('//table')[2]
        ip_list = table.xpath('./tr/td[1]/text()').extract()[1:]
        port_list = table.xpath('./tr/td[2]/text()').extract()[1:]
        for ip, port in zip(ip_list, port_list):
            proxy = "{0}:{1}".format(ip, port)
            if check_proxy_alive(proxy):
                self.proxy_db.put(proxy)

        next_page = response.xpath('//div[@id="PageList"]/a')
        next_page = next_page.xpath("./@href").extract()[-1]
        next_page = "http://www.66ip.cn" + next_page if "http" not in next_page else next_page

        self.page_count += 1
        if self.page_count < 4:    # only crawl proxies on top 4 pages
            yield scrapy.Request(url=next_page, callback=self.parse)

            """
        else:
            # zset
            print(self.proxy_list)

            for proxy in self.proxy_list:
                conn.zadd("proxy_zset", proxy, self._INITIAL_SCORE)
            print(conn.zcard("proxy_zset"))  # total count
            print(conn.zrange("proxy_zset", 0, 100, withscores=True))
            """


    """
    def get_raw_proxies(self, callback):
        proxies = []
        print('Callback', callback)
        for proxy in eval("self.{}()".format(callback)):
            print('Getting', proxy, 'from', callback)
            proxies.append(proxy)
        return proxies

    def crawl_daili66(self, page_count=4):
        start_url = 'http://www.66ip.cn/{}.html'
        urls = [start_url.format(page) for page in range(1, page_count + 1)]
        for url in urls:
            print('Crawling', url)
            html = get_page(url)
            if html:
                doc = pq(html)
                trs = doc('.containerbox table tr:gt(0)').items()
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text()
                    port = tr.find('td:nth-child(2)').text()
                    yield ':'.join([ip, port])

    def crawl_proxy360(self):
        start_url = 'http://www.proxy360.cn/Region/China'
        print('Crawling', start_url)
        html = get_page(start_url)
        if html:
            doc = pq(html)
            lines = doc('div[name="list_proxy_ip"]').items()
            for line in lines:
                ip = line.find('.tbBottomLine:nth-child(1)').text()
                port = line.find('.tbBottomLine:nth-child(2)').text()
                yield ':'.join([ip, port])

    def crawl_goubanjia(self):
        start_url = 'http://www.goubanjia.com/free/gngn/index.shtml'
        html = get_page(start_url)
        if html:
            doc = pq(html)
            tds = doc('td.ip').items()
            for td in tds:
                td.find('p').remove()
                yield td.text().replace(' ', '')

    def crawl_haoip(self):
        start_url = 'http://haoip.cc/tiqu.htm'
        html = get_page(start_url)
        if html:
            doc = pq(html)
            results = doc('.row .col-xs-12').html().split('<br/>')
            for result in results:
                if result: yield result.strip()
    """

