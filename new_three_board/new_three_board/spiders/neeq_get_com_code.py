#!/usr/bin/env python3
# coding: utf-8
# File: neeq_get_com_code.py
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
    name = "neeq_com_code"
    page = 0

    start_urls = ["http://www.neeq.com.cn/nqxxController/nqxx.do?page={0}&typejb=T&sortfield=xxzqdm&sorttype=asc".format(page)]

    """
    "公司详细信息"
    "http://www.neeq.com.cn/nq/detailcompany.html?companyCode=430002&typeId=1&typename=G&zrlx=%E5%8D%8F%E8%AE%AE"
    """

    def parse(self, response):
        """
        公司简要信息 
        http://www.neeq.com.cn/nq/listedcompany.html
        #所需要的信息在“公司详细信息”页面里都有，只需要抓取公司代码即可
        """

        json_content = json.loads(response.body.decode("utf-8")[6:-2])    # null([{"content": .......}])

        # print(type(json_content)) # <class 'dict'> # print(len(json_content))    # 9
        # print(json_content) # print(len(json_content["content"]))     # 20

        for com_dict in json_content["content"]:
            print(com_dict.get("xxzqdm", ""))
            """
            ntbi["com_code"] = com_dict.get("xxzqdm", "")  # xxzqdm 证券代码
            ntbi["com_abbr_name"] = com_dict.get("xxzqjc", "").replace(" ", "")  # xxzqjc 证券简称
            ntbi["type_of_transfer"] = com_dict.get("xxzrlx", "")   # xxzrlx 转让类型
            ntbi["com_industry"] = com_dict.get("xxhyzl", "")   # xxhyzl 所属行业
            ntbi["zbqs"] = com_dict.get("xxzbqs", "")   # xxzbqs 主办券商
            ntbi["region"] = com_dict.get("xxssdq", "")   # xxssdq 地区
            """
        NewThreeBoard.page += 1
        url = "http://www.neeq.com.cn/nqxxController/nqxx.do?page={0}&typejb=T&sortfield=xxzqdm&sorttype=asc".format(NewThreeBoard.page)

        # type(json_content.get("lastPage"))   # bool
        if not json_content.get("lastPage"):
            yield scrapy.Request(url=url, callback=self.parse)
