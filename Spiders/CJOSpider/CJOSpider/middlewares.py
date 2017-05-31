# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

import copy
import random
import requests
from selenium import webdriver
from scrapy import signals
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from scrapy.http import HtmlResponse
import time
from selenium.webdriver.common.proxy import ProxyType
from Spiders.CJOSpider.get_proxy import get_proxy
from Spiders.CJOSpider.utils import get_redis_uri
from Spiders.CJOSpider.CJOSpider.settings import REDIS_HOST
from Spiders.CJOSpider.CJOSpider.settings import REDIS_PORT
from Spiders.CJOSpider.CJOSpider.settings import REDIS_KEY_TASKS


class RotateUserAgentMiddleware(UserAgentMiddleware):
    REDIS_URI = get_redis_uri(REDIS_HOST, REDIS_PORT)

    def __init__(self, user_agent=''):
        self.user_agent = user_agent

    def process_request(self, request, spider):
        ua = random.choice(self.user_agent_list)
        if ua:
            request.headers.setdefault('User-Agent', ua)
        # 按照scrapy的架构图, 只有当请求真正发出去时(不是yield在scrapy的队列中等待)才会进入到DOWNLOADER_MIDDLEWARES中的各个MIDDLEWARE
        # 当请求真正发出去时, 将TASKS_HASH中的数据修改为当前的时间戳
        # meta_data = copy.deepcopy(request.meta)
        meta_data = request.meta
        # print(meta_data["item"])
        flagcode_timestamp = "{0}_{1}".format(int(meta_data["item"]["flag_code"])+1, int(time.time()))
        self.REDIS_URI.hset(REDIS_KEY_TASKS, meta_data["item"]["data_dict_str"], flagcode_timestamp)
        print(self.REDIS_URI.hget(REDIS_KEY_TASKS, meta_data["item"]["data_dict_str"]), flagcode_timestamp)
        del meta_data["item"]
        # request.replace(meta=meta_data)   # OK.

    # the default user_agent_list composes chrome,I E,firefox,Mozilla,opera,netscape
    # for more user agent strings,you can find it in http://www.useragentstring.com/pages/useragentstring.php
    user_agent_list = [
        # OK
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv,2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
        "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
    ]


"""
class JavaScriptMiddleware(object):
    def process_request(self, request, spider):
        # print("PhantomJS is starting...")
        # driver = webdriver.PhantomJS(r"/home/lxw/Downloads/phantomjs/phantomjs-2.1.1-linux-x86_64/bin/phantomjs")   # OK
        driver = webdriver.Chrome(r"/home/lxw/Software/chromedirver_selenium/chromedriver") # OK

        "" "
        # Using IP Proxies:
        # 打开两次chrome？那第一次chrome会暴露IP吗？应该没事儿，没有访问特定的网站
        # 利用DesiredCapabilities(代理设置)参数值，重新打开一个sessionId，我看意思就相当于浏览器清空缓存后，加上代理重新访问一次url
        proxy = webdriver.Proxy()
        proxy.proxy_type = ProxyType.MANUAL
        req = requests.get("http://datazhiyuan.com:60001/plain", timeout=10)
        print("Get an IP proxy:", req.text)

        if req.text:
            proxy.http_proxy = req.text  # "1.9.171.51:800"
        # 将代理设置添加到webdriver.DesiredCapabilities.PHANTOMJS中
        proxy.add_to_capabilities(webdriver.DesiredCapabilities.PHANTOMJS)
        driver.start_session(webdriver.DesiredCapabilities.PHANTOMJS)
        "" "

        driver.get(request.url) # 京东的商品详情页面太慢了, 改用http://roll.news.qq.com/页面
        time.sleep(2)
        js = "var q=document.documentElement.scrollTop=10000"
        driver.execute_script(js)   # 可执行js，模仿用户操作。此处为将页面拉至最底端。
        time.sleep(3)
        body = driver.page_source
        print("访问" + request.url)
        return HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=request)
"""


class ProxyMiddleware(object):
    """
    如果不使用Selenium/PhantomJS，那么Scrapy中使用代理可以这样用
    但如果使用Selenium/PhantomJS，并且想让代理在Selenium/PhantomJS中生效则不能这样用(这样用，即使在settings.py中ProxyMiddleware具有比JavaScriptMiddleware高的优先级，代理依然无法在Selenium/PhantomJS中生效)
    """
    # overwrite process request
    def process_request(self, request, spider):
        try:
            proxy = get_proxy()
            if proxy:
                request.meta['proxy'] = "http://" + proxy   # "http://" is essential here.
                request.meta['download_timeout'] = 120.0
                request.meta['retry_times'] = 2
            else:
                print("in ProxyMiddleware.process_request(): no proxy available")
        except Exception as e:
            print("lxw_Exception", e)
            return


class CjospiderSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
