#!/usr/bin/env python3
# coding: utf-8
# File: check_doc_id_mongo.py
# Author: lxw
# Date: 5/31/17 9:41 PM

import redis


class DOCIDMongo:
    REDIS_HOST = "192.168.1.29"
    # REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379
    REDIS_KEY_DOC_ID = "DOC_ID_HASH"
    pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=0)
    REDIS_URI = redis.Redis(connection_pool=pool)

    def check_doc_id_mongo(self):
        for item in self.REDIS_URI.hscan_iter(self.REDIS_KEY_DOC_ID):
            # print(type(item), item)   # <class 'tuple'> (b'65d07ad1-09f1-45d6-8c9f-6fe379e146f1', b'0')
            doc_id = item[0].decode("utf-8")
            flag_code_timestamp = int(item[1].decode("utf-8"))
            if flag_code_timestamp != 0:
                print(doc_id, flag_code_timestamp)


if __name__ == "__main__":
    doc_id_mongo = DOCIDMongo()
    doc_id_mongo.check_doc_id_mongo()
