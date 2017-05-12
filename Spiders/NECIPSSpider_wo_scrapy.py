#!/usr/bin/env python3
# coding: utf-8
# File: NECIPSSpider_wo_scrapy.py
# Author: lxw
# Date: 5/10/17 4:24 PM

from lxml import etree
import random
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.proxy import ProxyType
import time
from PIL import Image
import uuid
from io import BytesIO

from Spiders.public_utils import user_agent_list
from Spiders.public_utils import get_proxy

"""
Supporting:
0. [TODO] CAPTCHA
1. PhantomJS/Chrome
2. User-Agent
3. IP Proxy

TODO：
整合线程池
"""

TIMEOUT = 60

def get_driver_phantomjs():
    """
    References:
    PhantomJS:
    1. [设置PHANTOMJS的USER-AGENT](http://smilejay.com/2013/12/set-user-agent-for-phantomjs/)
    2. [Selenium 2 - Setting user agent for IE and Chrome](http://stackoverflow.com/questions/6940477/selenium-2-setting-user-agent-for-ie-and-chrome)
    """
    dcap = dict(DesiredCapabilities.PHANTOMJS)

    # Setting User-Agent
    ua = random.choice(user_agent_list)
    if ua:
        print("Current User-Agent is:", ua)
        dcap["phantomjs.page.settings.userAgent"] = ua

    driver = webdriver.PhantomJS(executable_path=r"/home/lxw/Downloads/phantomjs/phantomjs-2.1.1-linux-x86_64/bin/phantomjs", desired_capabilities=dcap)

    """
    # Setting IP Proxies
    # 利用DesiredCapabilities(代理设置)参数值，重新打开一个sessionId，我看意思就相当于浏览器清空缓存后，加上代理重新访问一次url
    proxy = webdriver.Proxy()
    proxy.proxy_type = ProxyType.MANUAL
    ip_proxy = get_proxy()
    if ip_proxy:
        proxy.http_proxy = ip_proxy

    # 将代理设置添加到webdriver.DesiredCapabilities.PHANTOMJS中
    # proxy.add_to_capabilities(DesiredCapabilities.PHANTOMJS)
    # driver.start_session(DesiredCapabilities.PHANTOMJS)
    proxy.add_to_capabilities(dcap)
    driver.start_session(dcap)
    """

    # 设置超时时间
    driver.set_page_load_timeout(TIMEOUT)
    driver.set_script_timeout(TIMEOUT)  # 这两种设置都进行才有效

    return driver


def get_driver_chrome():
    """
    References:
    ChromeDriver:
    [爬虫：3. selenium](http://www.jianshu.com/p/2631bf34328e)
    """
    options = webdriver.ChromeOptions()

    # Setting User-Agent
    ua = random.choice(user_agent_list)
    if ua:
        print("Current User-Agent is:", ua)
        options.add_argument("--user-agent=" + ua)

    """
    # Setting IP Proxies
    ip_proxy = get_proxy()
    if ip_proxy:
        options.add_argument('--proxy-server=' + ip_proxy)
    """
    driver = webdriver.Chrome(executable_path=r"/home/lxw/Software/chromedirver_selenium/chromedriver", chrome_options=options)

    # 设置超时时间
    driver.set_page_load_timeout(TIMEOUT)
    driver.set_script_timeout(TIMEOUT)  # 这两种设置都进行才有效

    return driver


if __name__ == "__main__":
    driver = get_driver_phantomjs()
    # driver = get_driver_chrome()

    try:
        # driver.get("http://ipecho.net/plain")
        # driver.get("http://xiujinniu.com/xiujinniu/index.php")
        driver.get("http://www.ip138.com/ua.asp")      # 查看当前请求的User-Agent和所使用的IP
    except TimeoutException as te:
        print("lxw_NOTE: TimeoutException. ", te)
    else:
        time.sleep(2)
        print("OK")
        # sourcecode = driver.page_source
        selector = etree.HTML(driver.page_source)
        try:
            trs = selector.xpath('//table/tbody')[2]
        except IndexError as ie:
            print("Getting page_source Error:", driver.page_source)
        else:
            td_list = trs.xpath('./tr/td')
            for td in td_list:
                print(td.xpath("string(.)").replace("\n", " ").replace("  ", ""))
    finally:
        driver.quit()


    """
    driver.get(request.url) # 京东的商品详情页面太慢了, 改用http://roll.news.qq.com/页面
    time.sleep(2)
    js = "var q=document.documentElement.scrollTop=10000"
    driver.execute_script(js)   # 可执行js，模仿用户操作。此处为将页面拉至最底端。
    time.sleep(3)
    body = driver.page_source
    """
