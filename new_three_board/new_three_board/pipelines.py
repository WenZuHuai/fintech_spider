# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from scrapy.conf import settings

class NewThreeBoardPipeline(object):
    def __init__(self):
        db_name = "neeq"
        collection_name = "company_basic_info"

        conn = pymongo.MongoClient(settings.get("MONGODB_HOST"), settings.get("MONGODB_PORT"))
        db = conn[db_name]
        self.col = db[collection_name]

    def process_item(self, item, spider):
        self.col.insert(dict(item))
        return item

