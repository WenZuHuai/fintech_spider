# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.conf import settings
import pymongo


class CninfospiderPipeline(object):
    def __init__(self):
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        db = "scrapy"
        col = "cninfo_szmb"
        client = pymongo.MongoClient(host=host, port=port)
        tdb = client[db]
        self.tcol = tdb[col]

    def process_item(self, item, spider):
        company_info = dict(item)
        self.tcol.insert(company_info)
        return item
