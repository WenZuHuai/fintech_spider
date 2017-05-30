#!/usr/bin/env python3
# coding: utf-8
# File: utils.py
# Author: lxw
# Date: 4/26/17 2:57 PM

import logging
import redis
import requests
import os
from Spiders.CJOSpider.settings import TEST_API


# logging.basicConfig(level=logging.WARNING, filemode="w")


def generate_logger(logger_name):
    """
    # debug/error    
    """
    my_logger = logging.getLogger(logger_name)
    file_name = os.path.join(os.getcwd(), logger_name+".log")
    if os.path.isfile(file_name):
        with open(file_name, "w"):
            pass
    fh = logging.FileHandler(file_name)
    formatter = logging.Formatter("%(levelname)s - %(asctime)s - %(message)s")
    fh.setFormatter(formatter)
    my_logger.addHandler(fh)
    return my_logger


def generate_output_logger(logger_name):
    my_logger = logging.getLogger(logger_name)
    file_name = os.path.join(os.getcwd(), logger_name+".md")
    if os.path.isfile(file_name):
        with open(file_name, "w"):
            pass
    fh = logging.FileHandler(file_name)
    formatter = logging.Formatter("%(message)s")
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


def join_param(param):
    """
    :param param: type(param) dict
    :return: str
    """
    str_list = []
    for key, value in param.items():
        str_list.append("{0}:{1}".format(key, value))
    return ",".join(str_list)


def get_redis_uri(REDIS_HOST, REDIS_PORT):
    pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=0)
    # [redis连接对象是线程安全的](http://www.cnblogs.com/clover-siyecao/p/5600078.html)
    # [redis是单线程的](https://stackoverflow.com/questions/17099222/are-redis-operations-on-data-structures-thread-safe)
    return redis.Redis(connection_pool=pool)

