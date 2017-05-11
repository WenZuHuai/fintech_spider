#!/usr/bin/env python3
# coding: utf-8
# File: NECIPSSpider_wo_scrapy.py
# Author: lxw
# Date: 5/10/17 4:24 PM

from lxml import etree
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

TIMEOUT = 60

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


def get_proxy():
    try:
        # req = requests.get("http://datazhiyuan.com:60001/plain", timeout=10)
        req = requests.get("http://localhost:60001/plain", timeout=10)
        if req.text:
            print("Get an IP proxy:", req.text)     # req.text: "119.75.213.61:80"
            return req.text
        return None
    except Exception as e:
        print("lxw_Exception: in get_proxy(). ", e)
        return None


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
    # driver = get_driver_phantomjs()
    driver = get_driver_chrome()

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
