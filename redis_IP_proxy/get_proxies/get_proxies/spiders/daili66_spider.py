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
    """
    66IP.cn有时候会限定cookie，这时候需要下面的代码
    在settings中也需要相应的修改(settings.py参考new_three_board/settings.py)

    cookies = {"_cfduid":"dfd9a215f03c6a0008a48e6fbe844c3cb1493704103", "cf_clearance":"9b1492af01429e5e8076dcaf0ec959668c1ef2b9-1493704107-604800"}

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, cookies=cookies, callback=self.parse)

    cookies是从网站的F12->Network中拷贝出来的
    
    可以进一步尝试把cookies的修改和headers一样:放到middlewares.py中修改
    """
    name = "daili66_spider"
    current_page = "index.html"
    proxy_db = RedisClient()
    # start_urls = ["http://www.66ip.cn/index.html"]    # 这个页面的代理时国外的不稳定，太慢
    start_urls = ["http://www.66ip.cn/areaindex_1/index.html"]

    def parse(self, response):
        table = response.xpath('//table')[2]
        ip_list = table.xpath('./tr/td[1]/text()').extract()[1:]
        port_list = table.xpath('./tr/td[2]/text()').extract()[1:]
        for ip, port in zip(ip_list, port_list):
            proxy = "{0}:{1}".format(ip, port)
            if check_proxy_alive(proxy):
                Daili66Spider.proxy_db.put(proxy)
                print(proxy)

        if Daili66Spider.proxy_db.queue_len > 50:
            return

        next_page = response.css("#PageList .pageCurrent").xpath("following-sibling::a").css("::attr(href)").extract_first()
        print("Next_page:", next_page)
        # if next_page == Daili66Spider.current_page:   # NO
        if ".html" not in next_page:
            return

        print("Current page {0} is crawled successfully.".format(Daili66Spider.current_page))
        yield scrapy.Request(url="http://www.66ip.cn"+next_page, callback=self.parse)

        """
        next_page = response.xpath('//div[@id="PageList"]/a')
        next_page = next_page.xpath("./@href").extract()[-1]
        next_page = "http://www.66ip.cn" + next_page if "http" not in next_page else next_page

        self.page_count += 1
        if self.page_count < 4:    # only crawl proxies on top 4 pages
            yield scrapy.Request(url=next_page, callback=self.parse)
        """
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

