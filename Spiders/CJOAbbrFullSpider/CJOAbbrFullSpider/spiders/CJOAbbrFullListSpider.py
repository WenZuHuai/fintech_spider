#!/usr/bin/env python3
# coding: utf-8
# File: CJOAbbrFullListSpider.py
# Author: lxw
# Date: 5/20/17 10:37 PM
# Usage:
"""
892家公司简称不被公司全称包含的公司，分别看以简称和全称作为当事人进行爬取所得到的案例数目
不知道什么原因CJOAbbrFullSpider.py有些简称和全称没有爬取出来，所以手动将这部分简称和全称构造出一个left_list，然后对left_list再爬取一次
"""

import calendar
import json
import random
import requests
import scrapy
import time
import urllib.parse

from Spiders.CJOAbbrFullSpider.CJOAbbrFullSpider.middlewares import RotateUserAgentMiddleware
from Spiders.CJOAbbrFullSpider.get_proxy import get_proxy
from Spiders.CJOAbbrFullSpider.CJOAbbrFullSpider import items
from Spiders.CJOAbbrFullSpider.utils import generate_logger


class CJOAbbrFullListSpider(scrapy.Spider):
    name = "CJOAbbrFullListSpider"
    cases_per_page = 5
    url = "http://wenshu.court.gov.cn/List/ListContent"
    # url = "http://xiujinniu.com/xiujinniu/index.php"   # Validating Host/Referer/User-Agent/Proxy. OK.
    result_dict = {}
    left_list = ["泰嘉股份", "湖南泰嘉新材料科技股份有限公司", "英联股份", "广东英联包装股份有限公司", "海南钧达汽车饰件股份有限公司", "新宁物流", "江苏新宁现代物流股份有限公司", "奥克股份", "中环装备", "中节能环保装备股份有限公司", "元力股份", "福建元力活性炭股份有限公司", "湖北华舟重工应急装备股份有限公司", "前锋股份", "钱江生化", "清源股份", "大化股份", "锦旅股份", "百联股份", "德宏股份", "佛山市海天调味食品股份有限公司", "国药股份", "天津天药药业股份有限公司", "国瓷材料", "汇冠股份", "纳川股份", "烟台龙源电力技术股份有限公司", "汕头万顺包装材料股份有限公司", "洁美科技", "西藏易明西雅医药科技股份有限公司", "萃华珠宝", "申科股份", "东莞勤上光电股份有限公司", "安徽德力日用玻璃股份有限公司", "西泵股份", "天汽模", "天津汽车模具股份有限公司", "江苏常宝钢管股份有限公司", "宝莫股份", "沪士电子股份有限公司", "无锡双象超纤材料股份有限公司", "浙江伟星新型建材股份有限公司", "威创股份", "洋河股份", "湖南友谊阿波罗商业股份有限公司", "华明电力装备股份有限公司", "御银股份", "深圳赤湾石油基地股份有限公司", "河北宣化工程机械股份有限公司", "新疆天山水泥股份有限公司", "智度股份", "陕西省国际信托股份有限公司", "徐工机械", "国农科技"]
    output_logger = generate_logger("CJOAbbrFullListSpider")

    def start_requests(self):
        for com in self.left_list:
            param = {}
            param["当事人"] = com
            param = self.join_param(param)
            yield self.yield_formrequest(param, 1)

    def yield_formrequest(self, param, index):
        data = {
            # "Param": "案件类型:刑事案件,法院层级:高级法院",
            "Param": param,
            "Index": repr(index),
            "Page": repr(self.cases_per_page),
            "Order": "法院层级",
            "Direction": "asc",
        }

        return scrapy.FormRequest(url=self.url, formdata=data, callback=lambda response: self.parse(response, data), dont_filter=True)   # 关闭URL去重(有些url请求不成功，需要重新yield。如果打开URL去重, 这些请求无法成功?)

    def parse(self, response, data):
        """
        先按序请求各个start_url， 然后才会进入到parse中(可能是异步处理的，当start_urls比较多时，可能先进入parse? 待确定, 内部实现细节和工作原理)
        """
        body = urllib.parse.unquote_plus(response.request.body.decode("utf-8"), encoding="utf-8")
        # body: "Param=裁判日期:2016-02-07 TO 2016-02-07,案件类型:刑事案件&Index=1&Page=20&Order=法院层级&Direction=asc"
        print("body:", body)
        print("data:", data)

        text = response.text
        try:
            text_str = json.loads(text)
            text_list = json.loads(text_str)  # I don't know why I need json.loads() twice. ??????

            total_count = int(text_list[0]["Count"])
            print("Count:", total_count)
            self.result_dict[data["Param"].split(":")[1]] = total_count
            print(self.result_dict)
            self.output_logger.debug(self.result_dict)
            # self.output_logger.flush()
        except json.JSONDecodeError as jde:
            if "<title>502</title>" in response.text:
                print("The website returns 502")
                time.sleep(10)  # 服务器压力大，休息会儿
            elif "remind" in response.text:
                print("Bad news: the website block the spider")
                time.sleep(10)  # IP代理被禁用了，休息会儿等会儿新的代理
            else:
                print("lxw_JSONDecodeError_NOTE:", jde)
            # 针对这些抓取不成功的case, 重新yield进行抓取
            yield scrapy.FormRequest(url=self.url, formdata=data, callback=lambda resp: self.parse(resp, data), dont_filter=True)
        except Exception as e:
            print("lxw_Exception_NOTE:", e)
            # 针对这些抓取不成功的case, 重新yield进行抓取
            # TODO: 增加记录哪些案例应该爬取，哪些案例爬取过了，哪些没有爬取
            # "lxw_Exception_NOTE: 'Logger' object has no attribute 'flush'", 实际上此时已经爬取成功了，不能重新yield，这种情况要求必须要提供记录哪些案例(data即可)爬取过了，哪些没有爬取，然后重爬没有爬取到的
            # yield scrapy.FormRequest(url=self.url, formdata=data, callback=lambda resp: self.parse(resp, data), dont_filter=True)
            self.output_logger.error("[NOTE: NOT CRAWLED]: " + json.dumps(data))

    def join_param(self, param):
        """
        :param param: type(param) dict
        :return: str
        """
        str_list = []
        for key, value in param.items():
            str_list.append("{0}:{1}".format(key, value))
        return ",".join(str_list)
