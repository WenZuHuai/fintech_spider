#!/usr/bin/env python3
# coding: utf-8
# File: public_utils.py
# Author: lxw
# Date: 5/12/17 3:10 PM

import requests
import random
import os


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
            print("Using IP proxy:", req.text)     # req.text: "119.75.213.61:80"
            return req.text
        return None
    except Exception as e:
        print("lxw_Exception: in get_proxy(). ", e)
        return None


def get_proxy_xcdl():
    """
    http://www.xicidaili.com/api 代理
    稳定性和可用性一般, 感觉比自己的还是稍微好一些，自己获取到的代理质量一般
    """
    try:
        # req = requests.get("http://datazhiyuan.com:60001/plain", timeout=10)
        headers = {"Host": "api.xicidaili.com"}
        ua = random.choice(user_agent_list)
        if ua:
            headers["User-Agent"] = ua
        req = requests.get("http://api.xicidaili.com/free2016.txt", headers=headers, timeout=10)
        if req.text:
            proxy_list = req.text.split("\r\n")
            proxy = random.choice(proxy_list)
            print("Using IP proxy:", proxy)     # req.text: "119.75.213.61:80"
            return proxy
        return None
    except Exception as e:
        print("lxw_Exception: in get_proxy_xcdl(). ", e)
        return None


def get_proxy_xcdl_localfile():
    try:
        with open("./xcdl_proxies_1.txt") as f:
            lines = f.readlines()
            while 1:
                proxy = random.choice(lines)
                if proxy:
                    print("Using IP proxy:", proxy)     # req.text: "119.75.213.61:80"
                    return proxy
        return None
    except Exception as e:
        print("lxw_Exception: in get_proxy_xcdl_localfile(). ", e)
        return None


def check_proxy_alive(proxy):
    """
    when calling this method, YOU MUST make sure the type of proxy is str instead of bytes.
    """
    if not isinstance(proxy, str):
        if proxy:
            print("TypeError: Please make sure the type of proxy is str instead of bytes.")
        return False

    try:
        proxies = {"http": proxy, "https": proxy}   # NOTE: 这里"http"和"https"一定要都写，不能只写http或者是只写https
        # req = requests.get(TEST_API, proxies=proxies, timeout=(5, 30))
        req = requests.get("http://www.baidu.com/", proxies=proxies, timeout=3)
        # print(type(req))
        # print(req)
        return req.status_code == 200
    except Exception as e:
        # print("Bad Proxy", proxy)
        return False


def clean_xcdl_proxies():
    usable_proxies = []
    with open("./xcdl_proxies.txt") as f:
        while 1:
            line = f.readline()
            if not line:
                break
            line = line.strip()
            if check_proxy_alive(line):
                usable_proxies.append(line)

    with open("./xcdl_proxies_1.txt", "w") as f:
        f.write("\n".join(usable_proxies))


# clean_xcdl_proxies()
