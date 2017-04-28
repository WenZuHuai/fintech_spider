#!/usr/bin/env python3
# coding: utf-8
# File: phantomjs_proxy.py
# Author: lxw
# Date: 4/25/17 2:42 PM

from selenium import webdriver
from selenium.webdriver.common.proxy import ProxyType
from redis_IP_proxy.proxy_interface import RedisClient


def main():
    # 不使用代理代打开ip138
    # browser = webdriver.PhantomJS()   # Be OK in command line, but not in PyCharm.
    browser = webdriver.PhantomJS(r"/home/lxw/Downloads/phantomjs/phantomjs-2.1.1-linux-x86_64/bin/phantomjs")
    browser.get("http://xiujinniu.com/xiujinniu/index.php")
    print('session_id: ', browser.session_id)
    # print('page_source: ', browser.page_source)
    print('cookie: ', browser.get_cookies())
    print("----"*10, "\n")

    # 利用DesiredCapabilities(代理设置)参数值，重新打开一个sessionId，我看意思就相当于浏览器清空缓存后，加上代理重新访问一次url
    redis_client = RedisClient()
    proxy = webdriver.Proxy()
    proxy.proxy_type = ProxyType.MANUAL
    proxy_list = redis_client.get()
    if proxy_list:
        proxy.http_proxy = proxy_list[0]    # '1.9.171.51:800'
    # 将代理设置添加到webdriver.DesiredCapabilities.PHANTOMJS中
    proxy.add_to_capabilities(webdriver.DesiredCapabilities.PHANTOMJS)
    browser.start_session(webdriver.DesiredCapabilities.PHANTOMJS)
    browser.get("http://xiujinniu.com/xiujinniu/index.php")
    print('session_id: ', browser.session_id)
    # print('page_source: ', browser.page_source)
    print('cookie: ', browser.get_cookies())
    print("----"*10, "\n")

    # 还原为系统代理
    proxy = webdriver.Proxy()
    proxy.proxy_type = ProxyType.DIRECT
    proxy.add_to_capabilities(webdriver.DesiredCapabilities.PHANTOMJS)
    browser.start_session(webdriver.DesiredCapabilities.PHANTOMJS)
    browser.get("http://xiujinniu.com/xiujinniu/index.php")
    print('session_id: ', browser.session_id)
    # print('page_source: ', browser.page_source)
    print('cookie: ', browser.get_cookies())
    print("----"*10, "\n")

if __name__ == "__main__":
    main()
