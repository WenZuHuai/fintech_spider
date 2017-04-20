# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewThreeBoardItem(scrapy.Item):
    # define the fields for your item here like:
    """
    # Spider("new_three_board")
    com_code = scrapy.Field()
    com_name = scrapy.Field()
    com_detail_link = scrapy.Field()    # href 新三板在线网站内的详细信息页
    listing_date = scrapy.Field()   # 挂牌日期
    method_of_transfer = scrapy.Field()     # 转让方式
    registered_capital = scrapy.Field()   # 注册资本(万元)
    primary_business = scrapy.Field()   # 主营业务
    province = scrapy.Field()
    zbqs = scrapy.Field()   # 主办券商
    zss = scrapy.Field()   # 做市商
    accounting_firm = scrapy.Field()   # 会计事务所
    law_firm = scrapy.Field()   # 律师事务所
    csrc = scrapy.Field()   # 证监会行业  #CSRC (China Securities Regulatory Commission)
    """

    # Spider("neeq")
    com_code = scrapy.Field()   # xxzqdm 证券代码
    com_name = scrapy.Field()
    com_abbr_name = scrapy.Field()   # xxzqjc 证券简称
    type_of_transfer = scrapy.Field()  # xxzrlx 转让类型
    com_industry = scrapy.Field()   # xxhyzl 所属行业
    zbqs = scrapy.Field()   # xxzbqs 主办券商
    region = scrapy.Field()   # xxssdq 地区

