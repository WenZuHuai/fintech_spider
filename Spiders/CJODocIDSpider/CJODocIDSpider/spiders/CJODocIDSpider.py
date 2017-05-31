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
from Spiders.CJODocIDSpider.CJODocIDSpider.items import CjodocidspiderItem
from Spiders.CJODocIDSpider.CJODocIDSpider.settings import REDIS_HOST
from Spiders.CJODocIDSpider.CJODocIDSpider.settings import REDIS_PORT
from Spiders.CJODocIDSpider.CJODocIDSpider.settings import REDIS_KEY_DOC_ID


class CjodocidspiderSpider(scrapy.Spider):
    name = "CJODocIDSpider"

    error_logger = generate_logger("CJODocIDSpiderError")   # 错误日志
    REDIS_URI = get_redis_uri(REDIS_HOST, REDIS_PORT)
    TIMEOUT = 60    # 可能产生重复的请求(得到重复的数据), 之后再去重
    headers = {"Host": "wenshu.court.gov.cn"}

    def start_requests(self):
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
                            # url = "http://xiujinniu.com/xiujinniu/index.php"
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
                                # url = "http://xiujinniu.com/xiujinniu/index.php"
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
        if "<title>502</title>" in text:
            # self.error_logger.error("{0}. The website returns 502".format(doc_id))    # not necessary
            # 收到响应了, 只是响应不是想要的(502). 让爬虫立刻重跑(hset(REDIS_KEY_DOC_ID, doc_id, "0"))
            # 注意, 此处hset不是更改为timestamp, 更改为timestamp只是是为了防止重复发多次请求(从而防止数据重复)
            # 此处已经收到请求了, 所以可以立刻重发请求
            self.REDIS_URI.hset(REDIS_KEY_DOC_ID, doc_id, "0")
            return
        elif "remind" in response.text:
            # self.error_logger.error("Bad news: the website block the spider")    # not necessary
            time.sleep(10)  # IP代理被禁用了，休息会儿等会儿新的代理
            self.REDIS_URI.hset(REDIS_KEY_DOC_ID, doc_id, "0")
            return

        try:
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
                self.error_logger.error("doc_id: {0}. re.finditer() got nothing. text: {1}".format(doc_id, text))
                self.REDIS_URI.hset(REDIS_KEY_DOC_ID, doc_id, "0")
            else:   # Success
                # self.into_mongo("\"{" + json_data + "}\"", doc_id)
                case_details_json = "\"{" + json_data + "}\""
                self.REDIS_URI.hset(REDIS_KEY_DOC_ID, doc_id, "-1")  # Success
                cjo_doc_id_items = CjodocidspiderItem()
                cjo_doc_id_items["doc_id"] = doc_id
                cjo_doc_id_items["case_details_json"] = case_details_json
                yield cjo_doc_id_items

        except Exception as e:
            self.error_logger.error("lxw_Exception_NOTE: {0}. text: {1}".format(e, text))
            self.REDIS_URI.hset(REDIS_KEY_DOC_ID, doc_id, "0")
