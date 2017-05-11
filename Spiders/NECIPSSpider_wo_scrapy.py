#!/usr/bin/env python3
# coding: utf-8
# File: NECIPSSpider_wo_scrapy.py
# Author: lxw
# Date: 5/10/17 4:24 PM

import random
import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.proxy import ProxyType
import time

"""
Supporting:
0. [TODO] CAPTCHA
1. PhantomJS/Chrome
2. User-Agent
3. IP Proxy

TODO：
整合线程池
"""


# the default user_agent_list composes chrome,I E,firefox,Mozilla,opera,netscape
# for more user agent strings,you can find it in http://www.useragentstring.com/pages/useragentstring.php
user_agent_list = [
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv,2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
    "Mozilla/5.0 (Windows NT 6.1; rv,2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
    "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
]


def start():
    """
    References:
    1. [设置PHANTOMJS的USER-AGENT](http://smilejay.com/2013/12/set-user-agent-for-phantomjs/)
    2. [Selenium 2 - Setting user agent for IE and Chrome](http://stackoverflow.com/questions/6940477/selenium-2-setting-user-agent-for-ie-and-chrome)
    """
    ua = random.choice(user_agent_list)
    if ua:
        print("Current User-Agent is:", ua)

        # PhantomJS
        dcap = dict(DesiredCapabilities.PHANTOMJS)  # PhantomJS
        dcap["phantomjs.page.settings.userAgent"] = ua    # PhantomJS
        driver = webdriver.PhantomJS(executable_path=r"/home/lxw/Downloads/phantomjs/phantomjs-2.1.1-linux-x86_64/bin/phantomjs", desired_capabilities=dcap)   # PhantomJS

        """
        # Chrome
        options = webdriver.ChromeOptions()
        options.add_argument("--user-agent=" + ua)
        driver = webdriver.Chrome(executable_path=r"/home/lxw/Software/chromedirver_selenium/chromedriver", chrome_options=options)
        """

        """
        # Using IP Proxies:
        # 打开两次chrome？那第一次chrome会暴露IP吗？应该没事儿，没有访问特定的网站
        # 利用DesiredCapabilities(代理设置)参数值，重新打开一个sessionId，我看意思就相当于浏览器清空缓存后，加上代理重新访问一次url
        proxy = webdriver.Proxy()
        proxy.proxy_type = ProxyType.MANUAL
        # req = requests.get("http://datazhiyuan.com:60001/plain", timeout=10)
        req = requests.get("http://localhost:60001/plain", timeout=10)
        if req.text:
            print("Get an IP proxy:", req.text)
            proxy.http_proxy = req.text  # "1.9.171.51:800"

        # 将代理设置添加到webdriver.DesiredCapabilities.PHANTOMJS中
        # proxy.add_to_capabilities(webdriver.DesiredCapabilities.PHANTOMJS)
        # driver.start_session(webdriver.DesiredCapabilities.PHANTOMJS)
        # PhantomJS
        proxy.add_to_capabilities(dcap)
        driver.start_session(dcap)
        """

        """
        # Chrome
        proxy.add_to_capabilities(webdriver.DesiredCapabilities.CHROME)
        driver.start_session(webdriver.DesiredCapabilities.CHROME)
        """


        # 设置超时时间
        driver.set_page_load_timeout(90)
        driver.set_script_timeout(90)  # 这两种设置都进行才有效

        try:
            # driver.get("http://ipecho.net/plain")
            driver.get("http://xiujinniu.com/xiujinniu/index.php")
        except TimeoutException as te:
            print("lxw_NOTE: TimeoutException. ", te)
        else:
            time.sleep(2)
            print(driver.page_source)

        """
        driver.get(request.url) # 京东的商品详情页面太慢了, 改用http://roll.news.qq.com/页面
        time.sleep(2)
        js = "var q=document.documentElement.scrollTop=10000"
        driver.execute_script(js)   # 可执行js，模仿用户操作。此处为将页面拉至最底端。
        time.sleep(3)
        body = driver.page_source
        """

if __name__ == "__main__":
    start()
