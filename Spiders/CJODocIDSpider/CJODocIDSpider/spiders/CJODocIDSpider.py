#!/usr/bin/env python3
# coding: utf-8
# File: CJODocIDSpider.py
# Author: lxw
# Date: 5/11/17 3:57 PM

import json
import re
import scrapy
import time

from Spiders.CJODocIDSpider.utils import generate_logger
from Spiders.CJODocIDSpider.utils import get_redis_uri
from Spiders.CJODocIDSpider.CJODocIDSpider.items import CjodocidMiddlewaresItem
from Spiders.CJODocIDSpider.CJODocIDSpider.settings import REDIS_HOST
from Spiders.CJODocIDSpider.CJODocIDSpider.settings import REDIS_PORT
from Spiders.CJODocIDSpider.CJODocIDSpider.settings import REDIS_KEY_DOC_ID


class CjodocidspiderSpider(scrapy.Spider):
    name = "CJODocIDSpider"

    error_logger = generate_logger("CJODocIDSpiderError")   # 错误日志
    REDIS_URI = get_redis_uri(REDIS_HOST, REDIS_PORT)
    TIMEOUT = 480   # Proxy: request.meta['download_timeout'] = 120.0; request.meta['retry_times'] = 2; settings.py: RETRY_TIMES: 2(default)
    headers = {"Host": "wenshu.court.gov.cn"}

    def start_requests(self):
        # url = "http://xiujinniu.com/xiujinniu/index.php"
        count = 0
        continue_flag = True
        while continue_flag:
            continue_flag = False
            count += 1
            print("进入次数:", count)
            for item in self.REDIS_URI.hscan_iter(REDIS_KEY_DOC_ID):
                try:
                    # print(type(item), item)   # <class 'tuple'> (b'65d07ad1-09f1-45d6-8c9f-6fe379e146f1', b'0')
                    doc_id = item[0].decode("utf-8")
                    flag_code_timestamp = int(item[1].decode("utf-8"))
                    if flag_code_timestamp >= 0:    # {0: 初始值, 未爬取; -1: 爬取成功; > 0: 上次爬取的时间戳} 等于-1的不yield
                        continue_flag = True
                        if flag_code_timestamp == 0:    # 0: 初始值, 当前请求还没有真正的发出去, 需要发出请求
                            url = "http://wenshu.court.gov.cn/CreateContentJS/CreateContentJS.aspx?DocID=" + doc_id
                            self.headers["Referer"] = url
                            req = scrapy.Request(url=url, headers=self.headers,
                                                 callback=lambda response: self.parse(response, doc_id),
                                                 dont_filter=True)
                            item = CjodocidMiddlewaresItem()
                            item["doc_id"] = doc_id
                            req.meta["item"] = item
                            yield req
                        else:   # 当前请求在timestamp的时候真正发出去了
                            if int(time.time()) - flag_code_timestamp > self.TIMEOUT:    # 超过了self.TIMEOUT时间, 还没有收到该请求的response, 认为该请求上次失败了, 需要重发请求
                                url = "http://wenshu.court.gov.cn/CreateContentJS/CreateContentJS.aspx?DocID=" + doc_id
                                self.headers["Referer"] = url
                                req = scrapy.Request(url=url, headers=self.headers,
                                                     callback=lambda response: self.parse(response, doc_id),
                                                     dont_filter=True)
                                item = CjodocidMiddlewaresItem()
                                item["doc_id"] = doc_id
                                req.meta["item"] = item
                                yield req
                            else:
                                pass    # 什么都不做, 还没到超时时间
                except Exception as e:
                    self.error_logger.error("in start_requests(): {0}".format(e))

    def parse(self, response, doc_id):
        print("in parse(). data:", doc_id)
        text = response.text
        json_data = ""
        match_result = re.finditer(r"jsonHtmlData.*?jsonData", text, re.S)
        for m in match_result:
            # print("in for cyclic body")
            data = m.group(0)
            right_index = data.rfind("}")
            left_index = data.find("{")
            json_data = data[left_index + 1:right_index]
            break  # this is essential. Only the first match is what we want.
        if json_data == "":
            self.error_logger.error("doc_id: {0}. re.finditer() got nothing.".format(doc_id))
        else:
            self.REDIS_URI.hset(REDIS_KEY_DOC_ID, doc_id, "-1")
        return "\"{" + json_data + "}\""

    def into_mongo(self, case_dict):
        print(case_dict)
