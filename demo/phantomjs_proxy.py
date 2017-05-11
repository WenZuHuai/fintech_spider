#!/usr/bin/env python3
# coding: utf-8
# File: phantomjs_proxy.py
# Author: lxw
# Date: 4/25/17 2:42 PM

import requests
from selenium import webdriver
from selenium.webdriver.common.proxy import ProxyType
# from redis_IP_proxy.proxy_interface import RedisClient


def main():
    # browser = webdriver.PhantomJS()   # Be OK in command line, but not in PyCharm.
    # browser = webdriver.PhantomJS(r"/home/lxw/Downloads/phantomjs/phantomjs-2.1.1-linux-x86_64/bin/phantomjs")
    browser = webdriver.Chrome(r"/home/lxw/Software/chromedirver_selenium/chromedriver") # OK
    browser.get("http://ipecho.net/plain")
    print('session_id: ', browser.session_id)
    print('page_source: ', browser.page_source)
    print('cookie: ', browser.get_cookies())
    print("----"*10, "\n")

    # 利用DesiredCapabilities(代理设置)参数值，重新打开一个sessionId，我看意思就相当于浏览器清空缓存后，加上代理重新访问一次url
    proxy = webdriver.Proxy()
    proxy.proxy_type = ProxyType.MANUAL
    # req = requests.get("http://datazhiyuan.com:60001/plain", timeout=10)
    req = requests.get("http://localhost:60001/plain", timeout=10)
    print("Get an IP proxy:", req.text)
    if req.text:
        proxy.http_proxy = req.text    # '1.9.171.51:800'
    # 将代理设置添加到webdriver.DesiredCapabilities.PHANTOMJS中
    proxy.add_to_capabilities(webdriver.DesiredCapabilities.PHANTOMJS)
    browser.start_session(webdriver.DesiredCapabilities.PHANTOMJS)
    browser.get("http://ipecho.net/plain")
    print('session_id: ', browser.session_id)
    print('page_source: ', browser.page_source)
    print('cookie: ', browser.get_cookies())
    print("----"*10, "\n")

    # 还原为系统代理
    proxy = webdriver.Proxy()
    proxy.proxy_type = ProxyType.DIRECT
    proxy.add_to_capabilities(webdriver.DesiredCapabilities.PHANTOMJS)
    browser.start_session(webdriver.DesiredCapabilities.PHANTOMJS)
    browser.get("http://ipecho.net/plain")
    print('session_id: ', browser.session_id)
    print('page_source: ', browser.page_source)
    print('cookie: ', browser.get_cookies())
    print("----"*10, "\n")

if __name__ == "__main__":
    main()
