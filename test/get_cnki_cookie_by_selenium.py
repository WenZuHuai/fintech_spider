#!/usr/bin/env python3
# coding: utf-8
# File: get_cnki_cookie_by_selenium.py.py
# Author: lxw
# Date: 5/27/17 3:24 PM

import random
import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from Spiders.CNKI_Patent.CNKI_Patent.middlewares import RotateUserAgentMiddleware


TIMEOUT = 60


def get_driver_chrome():
    """
    References:
    ChromeDriver:
    [爬虫：3. selenium](http://www.jianshu.com/p/2631bf34328e)
    """
    options = webdriver.ChromeOptions()

    # Setting User-Agent
    ua = random.choice(RotateUserAgentMiddleware.user_agent_list)
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
    driver = get_driver_chrome()

    try:
        # driver.get("http://www.ip138.com/ua.asp")      # 查看当前请求的User-Agent和所使用的IP
        # driver.get("http://ipecho.net/plain")
        driver.get("http://kns.cnki.net/kns/brief/default_result.aspx")
    except TimeoutException as te:
        print("lxw_NOTE: TimeoutException. ", te)
    else:
        time.sleep(2)
        selenium_cookies = driver.get_cookies()
        cookies = {}
        for item in selenium_cookies:
            cookies[item['name']] = item['value']
        print("selenium_cookies:", selenium_cookies)
        print("cookies:", cookies)
        print("OK")
    finally:
        driver.quit()
