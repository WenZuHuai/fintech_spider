#!/usr/bin/env python3
# coding: utf-8
# File: utils.py
# Author: lxw
# Date: 4/26/17 2:57 PM

import requests
from requests.exceptions import ConnectionError
from redis_IP_proxy.settings import TEST_API

base_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
    # 'Accept-Encoding': 'gzip, deflate, sdch',
    # 'Accept-Language': 'zh-CN,zh;q=0.8'
}


def get_page(url, options={}):
    headers = dict(base_headers, **options)
    print('Getting', url)
    try:
        r = requests.get(url, headers=headers)
        print('Getting result', url, r.status_code)
        if r.status_code == 200:
            return r.text
    except ConnectionError:
        print('Crawling Failed', url)
        return None


def check_proxy_alive(proxy):
    """
    when calling this method, YOU MUST make sure the type of proxy is str instead of bytes.
    """
    if not isinstance(proxy, str):
        print("TypeError: Please make sure the type of proxy is str instead of bytes.")
        return False

    try:
        proxies = {"http": proxy, "https": proxy}   # NOTE: 这里"http"和"https"一定要都写，不能只写http或者是只写https
        # req = requests.get(TEST_API, proxies=proxies, timeout=(5, 30))
        req = requests.get(TEST_API, proxies=proxies, timeout=3)
        # print(type(req))
        # print(req)
        return req.status_code == 200
    except Exception as e:
        # print("Bad Proxy", proxy)
        return False
