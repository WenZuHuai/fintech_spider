#!/usr/bin/env python3.6
# coding=utf-8
import requests
import redis
import time
import datetime
class IpPool():
    def __init__(self, url):
        self.url = url
        self.redis_client = redis.Redis(host="192.168.1.29", port=6379, db=0)
        self.key = "IPPool"
        self.db = "IPDaxiang"

    def get_ip_list(self):
        ip_list = []
        response = requests.get(self.url)
        result = response.text
        ip_tmp_list = result.split("\n")
        for ip in ip_tmp_list:
            ip_list.append(ip.strip())
        return ip_list
    def insert_redis(self):
        ip_list = self.get_ip_list()
        for each_ip in ip_list:
            self.redis_client.rpush(self.key, each_ip)
            if self.redis_client.sismember(self.db, each_ip):
                continue
            else:
                self.redis_client.sadd(self.db, each_ip)
    def update_redis(self):
        num = self.redis_client.llen(self.key)
        self.insert_redis()
        for index in range(num):
            self.redis_client.lpop(self.key)


    def close_redis(self):
        pass

    def get_data(self):
        print(self.redis_client.lrange(self.key,0,self.redis_client.llen(self.key)))
        


def run():

    url = "http://tvp.daxiangdaili.com/ip/?tid=557295271204258&num=500&delay=3&category=2&exclude_ports=8088,80,8080"
    ip_pool = IpPool(url)
    ip_pool.update_redis()
    log_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    with open("ip.log","a") as fp:
        fp.write(log_str)



if __name__== "__main__":
    run()


