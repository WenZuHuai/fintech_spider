#!/usr/bin/env python3
# coding: utf-8
# File: utils.py
# Author: lxw
# Date: 4/26/17 2:57 PM

import logging
import requests
import os
from Spiders.CJOSpider.settings import TEST_API


# logging.basicConfig(level=logging.WARNING, filemode="w")


def generate_logger(logger_name):
    my_logger = logging.getLogger(logger_name)
    file_name = os.path.join(os.getcwd(), logger_name+".log")
    """
    if os.path.isfile(fileName):
        with open(fileName, "w"):
            pass
    """
    fh = logging.FileHandler(file_name)
    formatter = logging.Formatter("%(levelname)s - %(asctime)s - %(message)s")
    fh.setFormatter(formatter)
    my_logger.addHandler(fh)
    return my_logger


def check_proxy_alive(proxy):
    """
    when calling this method, YOU MUST make sure the type of proxy is str instead of bytes.
    """
    if not isinstance(proxy, str):
        # print("TypeError: Please make sure the type of proxy is str instead of bytes.")
        return False

    try:
        proxies = {"http": proxy, "https": proxy}  # NOTE: 这里"http"和"https"一定要都写，不能只写http或者是只写https
        # req = requests.get(TEST_API, proxies=proxies, timeout=(5, 30))
        req = requests.get(TEST_API, proxies=proxies, timeout=3)
        # print(type(req))
        # print(req)
        return req.status_code == 200
    except Exception as e:
        # print("Bad Proxy", proxy)
        return False

