#!/usr/bin/env python3
# coding: utf-8
# File: neeq_com_info.py
# Author: lxw
# Date: 4/20/17 8:13 PM

import json
import scrapy
from new_three_board import items


class NewThreeBoard(scrapy.Spider):
    """
    新三板又称全国中小企业股份转让系统 --#http://www.360doc.com/content/15/0529/13/49267_474193531.shtml
    全国中小企业股份转让系统(http://www.neeq.com.cn/nq/listedcompany.html)
    """
    name = "neeq"
    page = 0

    start_urls = ["http://www.neeq.com.cn/nqxxController/nqxx.do?page={0}&typejb=T&sortfield=xxzqdm&sorttype=asc".format(page)]

    def parse(self, response):
        json_content = json.loads(response.body.decode("utf-8")[6:-2])    # null([{"content": .......}])

        # print(type(json_content)) # <class 'dict'> # print(len(json_content))    # 9
        # print(json_content) # print(len(json_content["content"]))     # 20

        for com_dict in json_content["content"]:
            com_code = com_dict.get("xxzqdm", "")   # xxzqdm 证券代码
            print("com_code:{0}".format(com_code))
            if com_code:
                # http://www.neeq.com.cn/nq/detailcompany.html?companyCode=430002&typeId=1&typename=G
                url = "http://www.neeq.com.cn/nqhqController/detailCompany.do?zqdm={0}".format(com_code)
                yield scrapy.Request(url=url, callback=self.parse_details)

        NewThreeBoard.page += 1
        print("NewThreeBoard.page:{0}".format(NewThreeBoard.page))
        url = "http://www.neeq.com.cn/nqxxController/nqxx.do?page={0}&typejb=T&sortfield=xxzqdm&sorttype=asc".format(NewThreeBoard.page)

        # type(json_content.get("lastPage"))   # bool
        if not json_content.get("lastPage"):
            yield scrapy.Request(url=url, callback=self.parse)

    def parse_details(self, response):
        detail_dict = json.loads(response.body[5:-1])
        ntbi = items.NewThreeBoardItem()
        ntbi["basic_info"] = detail_dict.get("basic_info", {})    # 公司概况
        ntbi["finance"] = detail_dict.get("finance", {})   # 财务指标
        ntbi["top_ten_holders"] = detail_dict.get("top_ten_holders", {})   # 十大股东
        ntbi["executives"] = detail_dict.get("executives", {})    # 高管人员
        yield ntbi
