# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class CninfospiderItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    code = scrapy.Field()
    scrapy_time = scrapy.Field()
    company_fullname = scrapy.Field()  # 公司全称
    english_name = scrapy.Field()  # 英文名称
    registered_address = scrapy.Field()  # 注册地址
    company_sortname = scrapy.Field()  # 公司简称
    legal_representative = scrapy.Field()  # 法定代表人
    board_secretariat = scrapy.Field()  # 公司董秘
    registered_capital = scrapy.Field()  # 注册资本（万元）
    business = scrapy.Field()  # 行业种类
    zip_code = scrapy.Field()  # 邮政编码
    phone = scrapy.Field()  # 公司电话
    faxes = scrapy.Field()  # 公司传真
    website = scrapy.Field()  # 公司网址
    time_market = scrapy.Field()  # 上市时间
    time_listing = scrapy.Field()  # 招股时间
    issure_price = scrapy.Field()  # 发行价格（元）
    issure_number = scrapy.Field()  # 发行数量（万股）
    issure_ratio = scrapy.Field()  # 发行市盈率
    issure_way = scrapy.Field()  # 发行方式
    underwriter = scrapy.Field()  # 主承销商
    referrer = scrapy.Field()  # 上市推荐人
    sponsor_institution = scrapy.Field()  # 保荐机构