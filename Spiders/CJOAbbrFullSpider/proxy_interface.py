#!/usr/bin/env python3
# coding: utf-8
# File: proxy_interface.py
# Author: lxw
# Date: 4/26/17 2:46 PM

import random
import redis
import requests

from Spiders.CJOAbbrFullSpider.error import PoolEmptyError
from Spiders.CJOAbbrFullSpider.settings import HOST, PORT, DB_NAME
from Spiders.CJOAbbrFullSpider.utils import generate_logger
from Spiders.CJOAbbrFullSpider.utils import check_proxy_alive


class RedisClient():
    """
    By now, only (a) random IP proxy(s) from the proxy-pool is/are provided.
    """

    def __init__(self, host=HOST, port=PORT):
        pool = redis.ConnectionPool(host=host, port=port, db=0)
        self._db = redis.Redis(connection_pool=pool)
        self.logger = generate_logger("RedisClient")

    def get(self, count=1):
        """
        get proxies from redis
        """
        """
        # daxiangdaili
        proxies = []
        req = requests.get(url="http://tvp.daxiangdaili.com/ip/?tid=557295271204258&num=10&delay=1&category=2&exclude_ports=8088,80,8080", timeout=60)
        if req.text:
            proxy_list = req.text.split("\r\n")
            proxy = random.choice(proxy_list)
            # print("Using IP proxy:", req.text)  # req.text: "119.75.213.61:80"
            print("Using IP proxy:", proxy)  # req.text: "119.75.213.61:80"
            proxies.append(proxy)
        return proxies
        """

        """
        # taobao 动态代理
        proxies = []
        req = requests.get(url="http://api.ip.data5u.com/dynamic/get.html?order=f305a6efa6aff38589285b8f66dd05fd", timeout=60)
        if req.text:
            # proxy = req.text.strip()
            proxy_list = req.text.strip().split("\n")   # req.text: '121.234.229.55:19739\n122.237.241.167:33923\n125.92.34.246:28653\n183.155.152.226:61394\n113.3.253.234:52948\n175.155.138.99:14135\n'
            proxy = random.choice(proxy_list)
            print("Using IP proxy:", proxy)  # req.text: "119.75.213.61:80"
            proxies.append(proxy)
        return proxies
        """

        # Get proxies from Redis
        proxies = []
        if count < 1:
            return proxies

        try:
            # When providing users with proxies, we must make sure these proxies are all usable.
            for index in range(count):
                index = random.randint(0, self.queue_len-1)
                proxy = self._db.lindex(DB_NAME, index).decode("utf-8")
                print("Using IP proxy:", proxy)  # req.text: "119.75.213.61:80"
                proxies.append(proxy)
        except ValueError as ve:
            self.logger.error("ValueError:queue_len is too short(<1).\n{0}".format(ve))
        except Exception as e:
            self.logger.error("lxw:Unexpected Error.\n{0}".format(e))
        finally:
            # self.logger.info("Using proxies:{0}".format(proxies))
            if len(proxies) < count:
               self.logger.warning("The requested count is larger than what we have in Redis, more proxies are needed.")
            return proxies

    def clean_proxies(self):
        """
        Test whether the proxies in Redis is usable, and remove the useless proxies.
        """
        proxies = self._db.lrange(DB_NAME, 0, -1)
        for proxy in proxies:
            if not isinstance(proxy, str):
                proxy = proxy.decode("utf-8")
            if not check_proxy_alive(proxy):
                self.logger.info("Remove useless proxy:{0} Current number of proxy available is:{1}".format(proxy, self.queue_len))
                self._db.lrem(DB_NAME, proxy, 0)

    def put(self, proxy):
        """
        add proxy to right top
        # zset
        self._db.zadd("proxy_zset", proxy, self._INITIAL_SCORE)
        """
        self._db.rpush(DB_NAME, proxy)  # list

    def pop(self):
        """
        get proxy from right.
        """
        # list
        try:
            # 移除列表的右侧第一个元素，并返回值右侧第一个元素
            return self._db.rpop(DB_NAME).decode('utf-8')  # return unicode('str' in Python3)
        except:
            raise PoolEmptyError

    @property
    def queue_len(self):
        """
        get length from queue.
        """
        return self._db.llen(DB_NAME)

    def showall(self):
        """
        show all elements in the list.
        """
        #print(self._db.lrange(DB_NAME, 0, -1))
        self.logger.info(repr(self._db.lrange(DB_NAME, 0, -1)))

    def del_all_proxies(self):
        """
        delete all the proxies in DB_NAME
        """
        self._db.delete(DB_NAME)


    def flush(self):
        """
        flush db
        """
        # self._db.flushall()    # DO NOT DO THIS.
        pass


if __name__ == "__main__":
    """
    client = RedisClient()
    proxy_list = ["190.229.237.14:8080", "192.129.144.237:9001", "196.22.249.124:80", "201.55.143.1:3128", "202.59.74.190:808", "203.168.166.146:8088", "212.96.99.229:8080", "27.96.32.82:80", "49.205.235.188:8080", "5.9.61.243:8118"]
    for proxy in proxy_list:
        client.put(proxy)
        print(client.queue_len)
        print(client.get(1))
    print(client.pop())
    """
    client = RedisClient()
    client.logger.info(repr(client.queue_len))
    client.logger.info(repr(client.get(2)))
    client.logger.info(repr(client.get()[0]))
