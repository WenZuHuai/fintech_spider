# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CjodocidspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # abstract = scrapy.Field()  # 1.裁判要旨段原文
    pass


class CjodocidMiddlewaresItem(scrapy.Item):
    # Middlewares.py. self.REDIS_URI.hset(REDIS_KEY_TASKS, data_dict_str, "{0}_{1}".format(flag_code+1, "timestamp"))
    doc_id = scrapy.Field()  # the "doc_id" in DOC_ID_HASH(Redis)