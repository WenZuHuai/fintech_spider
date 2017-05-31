#!/usr/bin/env python3
# coding: utf-8
# File: get_not_succeed.py
# Author: lxw
# Date: 5/31/17 9:19 AM

import json

from Spiders.CJOSpider.utils import get_redis_uri
from Spiders.CJOSpider.CJOSpider.settings import REDIS_HOST
from Spiders.CJOSpider.CJOSpider.settings import REDIS_PORT
from Spiders.CJOSpider.CJOSpider.settings import REDIS_KEY_DOC_ID
from Spiders.CJOSpider.CJOSpider.settings import REDIS_KEY_TASKS


class GetNotSucceed:
    REDIS_URI = get_redis_uri(REDIS_HOST, REDIS_PORT)

    def check_not_succeed(self):
        for item in self.REDIS_URI.hscan_iter(REDIS_KEY_TASKS):
            # print(type(item), item)   # <class 'tuple'> (b'{"Param": "\\u5f53\\u4e8b\\u4eba:\\u5927\\u667a\\u6167", "Index": "1", "case_parties": "601519", "abbr_full_category": "abbr_single"}', b'0_0')
            left_right = item[1].decode("utf-8").split("_")
            data_dict_str = item[0].decode("utf-8")
            data_dict = json.loads(data_dict_str)
            flag_code = int(left_right[0])
            timestamp = int(left_right[1])
            if timestamp != 0:
                print(json.dumps(data_dict, ensure_ascii=False), left_right)


if __name__ == "__main__":
    gns = GetNotSucceed()
    gns.check_not_succeed()

    """
    /home/lxw/IT/program/LXW_VIRTUALENV/py361scrapy133/bin/python /home/lxw/IT/projects/fintech_spider/Spiders/get_not_succeed.py
    {"Param": "当事人:乐视网,案件类型:民事案件,法院层级:中级法院", "Index": "1", "case_parties": "300104", "abbr_full_category": "abbr_single"} ['56', '1496191854']
    {"Param": "当事人:乐视网,案件类型:民事案件,法院层级:基层法院", "Index": "45", "case_parties": "300104", "abbr_full_category": "abbr_single"} ['55', '1496191857']
    {"Param": "当事人:乐视网,案件类型:民事案件,法院层级:基层法院", "Index": "65", "case_parties": "300104", "abbr_full_category": "abbr_single"} ['55', '1496191859']
    {"Param": "当事人:乐视网,案件类型:民事案件,法院层级:基层法院", "Index": "44", "case_parties": "300104", "abbr_full_category": "abbr_single"} ['55', '1496192015']
    {"Param": "当事人:乐视网,案件类型:民事案件,法院层级:基层法院", "Index": "27", "case_parties": "300104", "abbr_full_category": "abbr_single"} ['55', '1496192022']
    {"Param": "当事人:乐视网,案件类型:民事案件,法院层级:基层法院", "Index": "2", "case_parties": "300104", "abbr_full_category": "abbr_single"} ['55', '1496192025']
    
    Process finished with exit code 0
    """
