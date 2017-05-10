#!/usr/bin/env python3
# coding: utf-8
# File: NECIPSSpider_wo_scrapy.py
# Author: lxw
# Date: 5/10/17 4:24 PM

import random
import requests
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
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
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]


def get_proxy():
    """
    :return: <str> proxy
    """
    try:
        req = requests.get("http://datazhiyuan.com:60001/plain", timeout=10)
        print("Get an IP proxy:", req.text)
        return req.text     #
    except Exception as e:
        return None


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
        """
        dcap = dict(DesiredCapabilities.PHANTOMJS)  # PhantomJS
        dcap["phantomjs.page.settings.userAgent"] = ua    # PhantomJS
        driver = webdriver.PhantomJS(executable_path=r"/home/lxw/Downloads/phantomjs/phantomjs-2.1.1-linux-x86_64/bin/phantomjs", desired_capabilities=dcap)   # PhantomJS
        """

        # Chrome
        options = webdriver.ChromeOptions()
        options.add_argument("--user-agent=" + ua)
        driver = webdriver.Chrome(executable_path=r"/home/lxw/Software/chromedirver_selenium/chromedriver", chrome_options=options)

        # driver.get("http://ipecho.net/plain")
        driver.get("http://xiujinniu.com/xiujinniu/index.php")
        time.sleep(2)

    """
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
    """

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
