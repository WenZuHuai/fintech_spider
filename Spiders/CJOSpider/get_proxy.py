#!/usr/bin/env python3
# coding: utf-8
# File: get_proxy.py
# Author: lxw
# Date: 5/17/17 4:09 PM

from Spiders.CJOSpider.proxy_interface import RedisClient

client = RedisClient()


def get_proxy():
    proxy = None
    try:
        proxy = client.get()[0]
    except IndexError as ie:
        print("lxw_IndexError: No proxy available?", ie)
    except Exception as e:
        print("lxw_Exception", e)
    finally:
        return proxy

