#!/usr/bin/env python3
# coding: utf-8
# File: proxy_interface.py
# Author: lxw
# Date: 4/26/17 2:46 PM

import random
import redis

from redis_IP_proxy.error import PoolEmptyError
from redis_IP_proxy.settings import HOST, PORT
from redis_IP_proxy.utils import check_proxy_alive


class RedisClient():
    """
    By now, only (a) random IP proxy(s) from the proxy-pool is/are provided.
    
    TODO: The getting policy of proxy will/must be improved in the very near future.
    """

    def __init__(self, host=HOST, port=PORT):
        pool = redis.ConnectionPool(host=host, port=port, db=0)
        self._db = redis.Redis(connection_pool=pool)

    def get(self, count=1):
        """
        get proxies from redis
        # zset
        print("Total count of elements:", self._db.zcard("proxy_zset"))  # total count
        print(self._db.zrange("proxy_zset", 0, 100, withscores=True))
        return self._db.zrange("proxy_zset", 0, 100, withscores=True)
        """
        # list
        proxies = []
        if count < 1:
            return proxies

        try:
            # When providing users with proxies, we must make sure these proxies are all usable.
            # However, it is much too slow for get(), because clean_proxies() needs to check all proxies in Redis.
            self.clean_proxies()

            for index in range(count):
                index = random.randint(0, self.queue_len-1)
                proxy = self._db.lindex("proxy_list", index).decode("utf-8")
                proxies.append(proxy)
        except ValueError as ve:
            print("queue_len is too short(<1)", ve)
        except Exception as e:
            print("lxw:Unexpected Error", e)
        finally:
            print("Using proxies:", proxies)
            if len(proxies) < count:
                print("The requested count is larger than what we have in Redis, more proxies are needed.")
            return proxies

    def clean_proxies(self):
        """
        Test whether the proxies in Redis is usable, and remove the useless proxies.
        """
        proxies = self._db.lrange("proxy_list", 0, -1)
        for proxy in proxies:
            if not isinstance(proxy, str):
                proxy = proxy.decode("utf-8")
            if not check_proxy_alive(proxy):
                print("Remove useless proxy:{0} Current number of proxy available is:{1}".format(proxy, self.queue_len))
                self._db.lrem("proxy_list", proxy, 0)

    def put(self, proxy):
        """
        add proxy to right top
        # zset
        self._db.zadd("proxy_zset", proxy, self._INITIAL_SCORE)
        """
        self._db.rpush("proxy_list", proxy)  # list

    def pop(self):
        """
        get proxy from right.
        """
        # list
        try:
            # 移除列表的右侧第一个元素，并返回值右侧第一个元素
            return self._db.rpop("proxy_list").decode('utf-8')  # return unicode('str' in Python3)
        except:
            raise PoolEmptyError

    @property
    def queue_len(self):
        """
        get length from queue.
        """
        return self._db.llen("proxy_list")

    def showall(self):
        """
        show all elements in the list.
        """
        print(self._db.lrange("proxy_list", 0, -1))

    def flush(self):
        """
        flush db
        """
        self._db.flushall()


if __name__ == '__main__':
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
    print(client.queue_len)
    print(client.get(2))
