# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import redis
from scrapy.conf import settings


class CjospiderPipeline(object):
    collection_name = "cjo0528"

    def __init__(self, mongo_uri, mongo_port, mongo_db, redis_uri, redis_port, redis_key):
        self.mongo_uri = mongo_uri
        self.mongo_port = mongo_port
        self.mongo_db = mongo_db

        pool = redis.ConnectionPool(host=redis_uri, port=redis_port, db=0)
        # [redis连接对象是线程安全的](http://www.cnblogs.com/clover-siyecao/p/5600078.html)
        # [redis是单线程的](https://stackoverflow.com/questions/17099222/are-redis-operations-on-data-structures-thread-safe)
        self.redis_uri = redis.Redis(connection_pool=pool)
        self.redis_key = redis_key

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get("MONGODB_HOST"),
            mongo_port=crawler.settings.get("MONGODB_PORT"),
            mongo_db=crawler.settings.get("MONGODB_DATABASE", "items"),

            redis_uri=crawler.settings.get("REDIS_HOST"),
            redis_port=crawler.settings.get("REDIS_PORT"),
            redis_key=crawler.settings.get("REDIS_KEY")
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri, self.mongo_port)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert(dict(item))
        # self.redis_uri.rpush(self.redis_key, item.get("doc_id", "0"))
        # self.redis_uri.zadd(self.redis_key, item.get("doc_id", "0"), 0)
        self.redis_uri.hset(self.redis_key, item.get("doc_id", "0"), 0)
        """
        redis_key: DOC_ID_HASH
        0: 初始值, 未爬取
        -1: 爬取成功
        > 0: 爬取失败, 爬取的次数
        """
        return item
