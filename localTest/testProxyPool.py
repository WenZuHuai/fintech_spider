#!/usr/bin/env python3
# coding: utf-8
# File: testProxyPool.py
# Author: lxw
# Date: 4/27/17 3:17 PM

from redis_IP_proxy.proxy_interface import RedisClient


def main():
    client = RedisClient()
    print(client.queue_len)
    print(client.get(2))


if __name__ == "__main__":
    main()