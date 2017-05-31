#!/usr/bin/env python3
# coding: utf-8
# File: CJOSpider.py
# Author: lxw
# Date: 5/11/17 3:57 PM

import calendar
import copy
import datetime
import json
import random
import re
import requests
import scrapy
import time

from Spiders.CJOSpider.CJOSpider.middlewares import RotateUserAgentMiddleware
from Spiders.CJOSpider.CJOSpider.items import CjoMiddlewareItem
from Spiders.CJOSpider.get_proxy import get_proxy
from Spiders.CJOSpider.CJOSpider import items
from Spiders.CJOSpider.utils import generate_output_logger
from Spiders.CJOSpider.utils import generate_logger
# from Spiders.CJOSpider.utils import join_param
from Spiders.CJOSpider.utils import get_redis_uri
from Spiders.CJOSpider.CJOSpider.settings import REDIS_HOST
from Spiders.CJOSpider.CJOSpider.settings import REDIS_PORT
from Spiders.CJOSpider.CJOSpider.settings import REDIS_KEY_DOC_ID
from Spiders.CJOSpider.CJOSpider.settings import REDIS_KEY_TASKS


class CJOSpider(scrapy.Spider):
    name = "CJOSpider"
    cases_per_page = 20
    CRAWL_LIMIT = 2000  # 2000  裁判文书网以POST请求的方式最多允许爬取100页（每页最多20条）；如果直接请求网页，最多请求25页（每页最多20条）
    url = "http://wenshu.court.gov.cn/List/ListContent"
    # url = "http://xiujinniu.com/xiujinniu/index.php"   # Validating Host/Referer/User-Agent/Proxy. OK.
    CASE_CATEGORY = ["刑事案件", "民事案件", "行政案件", "赔偿案件", "执行案件"]    # 案件类型
    COURT_CATEGORY = ["最高法院", "高级法院", "中级法院", "基层法院"]   # 法院层级
    # filter according to DATE: 按照"日期"(每年/每月/每天)进行过滤("当事人"+"案件类型"+"法院层级"+"日期")
    # 每年: 裁判年份:2017    每月/每天: 裁判日期:2017-05-01 TO 2017-05-31/裁判日期:2017-05-01 TO 2017-05-01
    DOC_CATEGORY = ["判决书", "裁定书", "调解书", "决定书", "通知书", "批复", "答复", "函", "令", "其他"]  # 文书类型
    JUDGE_PROCEDURE = ["一审", "二审", "再审", "复核", "刑罚变更", "再审审查与审判监督", "其他"]   # 审判程序

    DIGIT_DICT = {1: "01", 2: "02", 3: "03", 4: "04", 5: "05", 6: "06", 7: "07", 8: "08", 9: "09"}  # 月份, 只处理单个的数字即可
    # 日志记录哪些案例应该爬取，哪些案例爬取过了，从而推导出哪些没有爬取
    # should_output_logger = generate_output_logger("CJOSpiderOuputShould")
    # actual_output_logger = generate_output_logger("CJOSpiderOuputActual")
    # 错误日志
    error_logger = generate_logger("CJOSpiderError")
    # 记录超过CRAWL_LIMIT的情况
    exceed_crawl_limit_logger = generate_output_logger("CJOSpiderExceedCrawlLimit")
    REDIS_URI = get_redis_uri(REDIS_HOST, REDIS_PORT)
    TIMEOUT = 50    # Proxy: request.meta['download_timeout'] = 120.0; request.meta['retry_times'] = 2; settings.py: RETRY_TIMES: 2(default)

    def start_requests(self):
        """
        从Redis中读取Request的data, 并yield Request
        data = {
            "Param": param,    # param: "当事人:工商银行",
            "Index": repr(index),
            # "Page": repr(self.CASES_PER_PAGE),
            # "Order": "法院层级",
            # "Direction": "asc",
            "case_parties": code,   # 当事人
            "abbr_full_category": category,  # 使用全称还是简称, 标志位
            # "crawl_date": crawl_date  # 爬取日期
        }
        """
        count = 0
        continue_flag = True
        while continue_flag:
            continue_flag = False
            count += 1
            print("进入次数:", count)
            for item in self.REDIS_URI.hscan_iter(REDIS_KEY_TASKS):
                # print(type(item), item)   # <class 'tuple'> (b'{"Param": "\\u5f53\\u4e8b\\u4eba:\\u5927\\u667a\\u6167", "Index": "1", "case_parties": "601519", "abbr_full_category": "abbr_single"}', b'0')
                left_right = item[1].decode("utf-8").split("_")
                flag_code = int(left_right[0])
                timestamp = int(left_right[1])
                if flag_code >= 0:    # {0: 初始值, 未爬取, 负值: 爬取成功, > 0: 未爬取成功, 爬取的次数} 等于-1的不yield
                    continue_flag = True
                    if timestamp == 0:    # 0: 初始值, 当前请求还没有真正的发出去
                        # 当前请求还没有真正的发出去, 需要发出请求
                        data_dict_str = item[0].decode("utf-8")
                        data_dict = json.loads(data_dict_str)
                        # 这儿不能hset(timestamp), 请求真正发出去的时候才能hset(timestamp)
                        yield self.yield_formrequest(data_dict["Param"], int(data_dict["Index"]), data_dict["case_parties"], data_dict["abbr_full_category"], flag_code)
                        # self.REDIS_URI.hset(REDIS_KEY_TASKS, data_dict_str, "{0}_{1}".format(flag_code + 1, int(time.time())))
                        # self.REDIS_URI.hset(REDIS_KEY_DOC_ID, "lxw", "123")
                    else:   # 当前请求在timestamp的时候真正发出去了
                        if int(time.time()) - timestamp > self.TIMEOUT:    # 超过了self.TIMEOUT时间, 还没有收到该请求的response, 认为该请求上次失败了
                            # 该请求上次失败了, 重发请求
                            data_dict_str = item[0].decode("utf-8")
                            data_dict = json.loads(data_dict_str)
                            # 这儿不能hset(timestamp), 请求真正发出去的时候才能hset(timestamp)
                            # self.REDIS_URI.hset(REDIS_KEY_TASKS, data_dict_str, "{0}_{1}".format(flag_code+1, "timestamp"))
                            yield self.yield_formrequest(data_dict["Param"], int(data_dict["Index"]), data_dict["case_parties"], data_dict["abbr_full_category"], flag_code)
                        else:
                            pass    # 什么都不做, 还没到超时时间

    def yield_formrequest(self, param, index, code, category, flag_code):
        """
        :param param: "POST" parameters
        :param index: page number (must be integer)
        :param code: company code
        :param category: abbr_single/abbr/full (abbr_single: 简称in全称; abbr: 使用简称; full: 使用全称)
        :param flag_code: flag_code to be transported to middlewares.
        :return: 
        """
        post_data = {
            # "Param": "案件类型:刑事案件,法院层级:高级法院",
            "Param": param,
            "Index": repr(index),
            "Page": repr(self.cases_per_page),
            "Order": "法院层级",
            "Direction": "asc",
        }

        data = copy.deepcopy(post_data)
        data["case_parties"] = code  # parties: 当事人
        data["abbr_full_category"] = category  # 使用全称还是简称, 标志位
        # data["crawl_date"] = datetime.datetime.now().strftime("%Y-%m-%d")    # 爬取日期, 不需要传递

        form_request = scrapy.FormRequest(url=self.url, formdata=post_data,
                                  callback=lambda response: self.parse(response, data),
                                  dont_filter=True)  # TODO: 关闭URL去重(有些url请求不成功，需要重新yield。如果打开URL去重, 这些请求无法成功?)

        item_data_dict = {
            "Param": param,  # param: "当事人:工商银行",
            "Index": repr(index),
            "case_parties": code,  # 当事人
            "abbr_full_category": category,  # 使用全称还是简称, 标志位
        }
        item = CjoMiddlewareItem()
        item["data_dict_str"] = json.dumps(item_data_dict)  # unicode
        # print(item["data_dict_str"])
        item["flag_code"] = flag_code
        form_request.meta["item"] = item

        return form_request
        # return scrapy.FormRequest(url=self.url, formdata=data, callback=self.parse, dont_filter=True, meta={"dont_redirect": True})   # 不要禁用redirect，否则重定向到502页面的request就无法到parse了
        # yield scrapy.Request(url, method="POST", body=json.dumps(data), callback=self.parse)  # Not-working

    def into_redis(self, param, index, code, category):
        """
        :param param: "POST" parameters
        :param index: page number (must be integer)
        :param code: company code
        :param category: abbr_single/abbr/full (abbr_single: 简称in全称; abbr: 使用简称; full: 使用全称)
        :return: 
        """
        # Redis中多余的字段一概不存, 只存yield_request需要的数据(Page, Order, Direction, crawl_date可以在yield_request时生成, 无需存储)
        data = {
            "Param": param,    # param: "当事人:工商银行",
            "Index": repr(index),
            # "Page": repr(self.CASES_PER_PAGE),
            # "Order": "法院层级",
            # "Direction": "asc",
            "case_parties": code,   # 当事人
            "abbr_full_category": category,  # 使用全称还是简称, 标志位
            # "crawl_date": crawl_date  # 爬取日期
        }

        # name = json.dumps(data, ensure_ascii=False)   # utf-8
        name = json.dumps(data)  # unicode
        # print("into Redis, data: ", name)
        self.REDIS_URI.hset(REDIS_KEY_TASKS, name, "0_0")
        """
        REDIS_KEY_TASKS: TASKS_HASH
        0: 初始值, 未爬取
        -1: 爬取成功
        > 0: 未爬取成功, 爬取的次数
        """

    def parse(self, response, data):
        """
        先按序请求各个start_url， 然后才会进入到parse中(可能是异步处理的，当start_urls比较多时，可能先进入parse? 待确定, 内部实现细节和工作原理)
        """
        print("in parse(). data:", data)
        text = response.text
        try:
            text_str = json.loads(text)
            text_list = json.loads(text_str)  # json.loads() twice, don't know why.
            # text_list: [{'Count': '0'}] or [{'Count': '1'},{'裁判要旨段原文': '本院认为，被告人王某为他人吸食毒品提供场所，其行为已构成容留他人吸毒罪，依法应予惩处。泰兴市人民检察院对被告人王某犯容留他人吸毒罪的指控成立，本院予以支持。被告人王某自动投案并如实供述自己的罪行，是自首，依法可以从轻处罚。被告人王某具有犯罪前科和多次吸毒劣迹，可酌情从重处罚。被告人王某主动向本院缴纳财产刑执行保证金，可酌情从轻处罚。关于辩护人提出“被告人王某具有自首、主动缴纳财产刑执行保证金等法定和酌定从轻处罚的情节，建议对被告人王某从轻处罚”的辩护意见，经查属实，本院予以采纳。依照《中华人民共和国刑法》第三百五十四条、第三百五十七条第一款、第六十七条第一款之规定，判决如下', '不公开理由': '', '案件类型': '1', '裁判日期': '2017-02-21', '案件名称': '王某容留他人吸毒罪一审刑事判决书', '文书ID': 'f42dfa1f-b5ca-4a22-a416-a74300f61906', '审判程序': '一审', '案号': '（2017）苏1283刑初44号', '法院名称': '江苏省泰兴市人民法院'}]
            # text_list == []. 当请求参数有错误时才会出现text_list == [], 如data: {'Param': '当事人:深赤湾', 'Index': "'1'", 'Page': '20', 'Order': '法院层级', 'Direction': 'asc', 'case_parties': '000022', 'abbr_full_category': 'abbr', 'crawl_date': '2017-05-28'} (Index:类型错误)
            total_count = int(text_list[0]["Count"])
            print("Count:", total_count)
            redis_data = {
                "Param": data["Param"],
                "Index": repr(int(data["Index"])),  # must be repr(int())
                "case_parties": data["case_parties"],
                "abbr_full_category": data["abbr_full_category"]}
            redis_data_str = json.dumps(redis_data)

            if total_count == 0:
                # self.actual_output_logger.info(json.dumps(data, ensure_ascii=False))  # 记录成功抓取的（包括数目为0的）
                self.REDIS_URI.hset(REDIS_KEY_TASKS, redis_data_str, "-2_0")     # [抓取完成]count == 0, 后续无需再抓取
                return
            elif total_count > self.CRAWL_LIMIT:
                self.REDIS_URI.hset(REDIS_KEY_TASKS, redis_data_str, "-3_0")      # [抓取完成]无效抓取 count > CRAWL_LIMIT,需要添加新的过滤条件
                # 理论上来说只有data["Index"] == 1的情况下才会进这里来，如果data["Index"] != 1, 说明在爬取的过程中网站的数据又增加了（使用当前的过滤条件组合无法将查询结果限定到self.CRAWL_LIMIT条以内），对于这种情况以后通过爬取新的日期的数据来补充，不要也不应该在这里补充（如果在这里补充，之前爬取并入库的数据就没法撤销了，导致数据重复、数据缺失等一系列问题）
                if int(data["Index"]) != 1:
                    self.error_logger.critical("lxw_CRITICAL_ERROR: Count > CRAWL_LIMIT. data[\"Index\"]({0}) should == 1, but not. 这可能是网站数据更新的原因. data: {1}. 当事人的所有相关数据应该全部删除, 并重新爬取".format(data["Index"], json.dumps(data, ensure_ascii=False)))
                    # return  # 不要return，继续入库
                else:
                    # 依靠 多个过滤条件 将查询结果限定到self.CRAWL_LIMIT条以内，具体过滤条件的过滤顺序参见 Spiders/CJOSpider/README.md
                    """
                    1)以公司名称(简称/全称)作为"当事人"过滤条件进行爬取
                    2)若1)中的"当事人"超过CJOSpider.CRAWL_LIMIT，则再按照"案件类型"进行过滤("当事人"+"案件类型")
                    3)若2)中的"案件类型"超过CJOSpider.CRAWL_LIMIT，则再按照"法院层级"进行过滤("当事人"+"案件类型"+"法院层级")
                    4)若3)中的"法院层级"超过CJOSpider.CRAWL_LIMIT，则再按照"日期"(每年/每月/每天)进行过滤("当事人"+"案件类型"+"法院层级"+"日期")
                    每年: 裁判年份:2017    每月/每天: 裁判日期:2017-05-01 TO 2017-05-31/裁判日期:2017-05-01 TO 2017-05-01
                    5)若4)中的"日期"超过CJOSpider.CRAWL_LIMIT，则再按照"文书类型"进行过滤("当事人"+"案件类型"+"法院层级"+"日期"+"文书类型")
                    6)若5)中的"文书类型"超过CJOSpider.CRAWL_LIMIT，则再按照"审判程序"进行过滤("当事人"+"案件类型"+"法院层级"+"日期"+"文书类型"+"审判程序")
                    """
                    origin_param_list = data["Param"].split(",")
                    length = len(origin_param_list)
                    if length == 1:    # 只有"当事人"，改用"当事人"+"案件类型"进行筛选
                        for category in self.CASE_CATEGORY:
                            temp_param = "{0},案件类型:{1}".format(data["Param"], category)
                            # yield self.yield_formrequest(temp_param, int(data["Index"]), data["case_parties"], data["abbr_full_category"])
                            # 不再直接yield_formrequest(), 而是通过添加到Redis(TASKS_HASH)中, 然后通过start_requests生成Request
                            self.into_redis(temp_param, int(data["Index"]), data["case_parties"], data["abbr_full_category"])   # 写 消息队列 Redis(TASKS_HASH)
                        return
                    elif length == 2:   # "当事人"+"案件类型"，改用"当事人"+"案件类型"+"法院层级"进行筛选
                        for category in self.COURT_CATEGORY:
                            temp_param = "{0},法院层级:{1}".format(data["Param"], category)
                            # yield self.yield_formrequest(temp_param, int(data["Index"]), data["case_parties"], data["abbr_full_category"])
                            # 不再直接yield_formrequest(), 而是通过添加到Redis(TASKS_HASH)中, 然后通过start_requests生成Request
                            self.into_redis(temp_param, int(data["Index"]), data["case_parties"], data["abbr_full_category"])   # 写 消息队列 Redis(TASKS_HASH)
                        return
                    elif length == 3:   # "当事人"+"案件类型"+"法院层级"，改用"当事人"+"案件类型"+"法院层级"+"日期"进行筛选
                        """
                        按照"日期"(每年/每月/每天)进行过滤("当事人"+"案件类型"+"法院层级"+"日期")
                        每年: 裁判年份:2017    每月/每天: 裁判日期:2017-05-01 TO 2017-05-31/裁判日期:2017-05-01 TO 2017-05-01
                        """
                        for year in self.get_year():    # 改用"当事人"+"案件类型"+"法院层级"+"裁判年份"进行筛选
                            temp_param = "{0},裁判年份:{1}".format(data["Param"], year)
                            # yield self.yield_formrequest(temp_param, int(data["Index"]), data["case_parties"], data["abbr_full_category"])
                            # 不再直接yield_formrequest(), 而是通过添加到Redis(TASKS_HASH)中, 然后通过start_requests生成Request
                            self.into_redis(temp_param, int(data["Index"]), data["case_parties"], data["abbr_full_category"])   # 写 消息队列 Redis(TASKS_HASH)
                        return
                    elif length == 4:
                        param_date = origin_param_list[3]  # param:  "裁判日期:2016-02-07 TO 2016-02-07,案件类型:刑事案件"
                        if "裁判年份" in param_date: # 改用"当事人"+"案件类型"+"法院层级"+"裁判日期"(每月)进行筛选
                            # 绕过每个月天数不一样，1月和12月比较特殊: 0101-0201, 0202-0301, 0302-0401, ..., 1002-1101, 1102-1201, 1202-1231
                            param_year = param_date.split(":")[1]
                            for month_param in self.get_month_param(param_year):  # 改用"当事人"+"案件类型"+"法院层级"+"裁判日期"(每月)进行筛选
                                origin_param_list[3] = "裁判日期:{0}".format(month_param)
                                # temp_param = "{0},裁判年份:{1}".format(data["Param"], year)
                                temp_param = ",".join(origin_param_list)
                                # yield self.yield_formrequest(temp_param, int(data["Index"]), data["case_parties"], data["abbr_full_category"])
                                # 不再直接yield_formrequest(), 而是通过添加到Redis(TASKS_HASH)中, 然后通过start_requests生成Request
                                self.into_redis(temp_param, int(data["Index"]), data["case_parties"], data["abbr_full_category"])   # 写 消息队列 Redis(TASKS_HASH)
                            return  # essential
                        elif "裁判日期" in param_date:   # 改用"当事人"+"案件类型"+"法院层级"+"裁判日期"(每天)进行筛选
                            param_day_list = param_date.split(":")[1].split(" TO ")
                            if param_day_list[0] == param_day_list[1]:  # 已经是“每天”的情况了，需要增加"文书类型"进行筛选
                                pass
                            else:
                                year = int(param_day_list[0].split("-")[0])
                                for year_month_date in self.get_date(year):  # 改用"当事人"+"案件类型"+"法院层级"+"裁判日期"(每天)进行筛选
                                    origin_param_list[3] = "裁判日期:{0} TO {0}".format(year_month_date)
                                    temp_param = ",".join(origin_param_list)
                                    # yield self.yield_formrequest(temp_param, int(data["Index"]), data["case_parties"], data["abbr_full_category"])
                                    # 不再直接yield_formrequest(), 而是通过添加到Redis(TASKS_HASH)中, 然后通过start_requests生成Request
                                    self.into_redis(temp_param, int(data["Index"]), data["case_parties"], data["abbr_full_category"])   # 写 消息队列 Redis(TASKS_HASH)
                                return  # essential
                        # "当事人"+"案件类型"+"法院层级"+"日期"，改用"当事人"+"案件类型"+"法院层级"+"日期"+"文书类型"进行筛选
                        for category in self.DOC_CATEGORY:
                            temp_param = "{0},文书类型:{1}".format(data["Param"], category)
                            # yield self.yield_formrequest(temp_param, int(data["Index"]), data["case_parties"], data["abbr_full_category"])
                            # 不再直接yield_formrequest(), 而是通过添加到Redis(TASKS_HASH)中, 然后通过start_requests生成Request
                            self.into_redis(temp_param, int(data["Index"]), data["case_parties"], data["abbr_full_category"])   # 写 消息队列 Redis(TASKS_HASH)
                        return
                    elif length == 5:   # "当事人"+"案件类型"+"法院层级"+"日期"+"文书类型"，改用"当事人"+"案件类型"+"法院层级"+"日期"+"文书类型"+"审判程序"进行筛选
                        # NOTE: "赔偿案件" 和 "执行案件" 不能使用审判程序进行筛选，网页上就是这样的
                        if "赔偿案件" in origin_param_list[1] or "执行案件" in origin_param_list[1]:
                            # 无法再精确，先把这self.CRAWL_LIMIT条数据入库，并把超过self.CRAWL_LIMIT的情况(data)，单独输出到文件中
                            self.exceed_crawl_limit_logger.error(json.dumps(data, ensure_ascii=False))
                        else:
                            for category in self.JUDGE_PROCEDURE:
                                temp_param = "{0},审判程序:{1}".format(data["Param"], category)
                                # yield self.yield_formrequest(temp_param, int(data["Index"]), data["case_parties"], data["abbr_full_category"])
                                # 不再直接yield_formrequest(), 而是通过添加到Redis(TASKS_HASH)中, 然后通过start_requests生成Request
                                self.into_redis(temp_param, int(data["Index"]), data["case_parties"], data["abbr_full_category"])   # 写 消息队列 Redis(TASKS_HASH)
                            return
                    else:
                        # 无法再精确，先把这self.CRAWL_LIMIT条数据入库，并把超过self.CRAWL_LIMIT的情况(data)，单独输出到文件中
                        self.exceed_crawl_limit_logger.error(json.dumps(data, ensure_ascii=False))
                        # DO NOT return.    # 继续下面的入库操作，先把这self.CRAWL_LIMIT条数据入库
            else:   # total_count > 0 && total_count < self.CRAWL_LIMIT
                # 不能直接yield next_index=True, 需判断是否需要yield，像count=3和count=11这种显然不需要yield下一页
                # Just continue to run the following code
                pass

            # 如果有下一页的cases需要爬取，那么继续爬取下一页
            index = int(data["Index"])
            # 提速：第一次进来的时候（Index==1的时候）就把所有后面的页面请求全部发出去；
            # 其他情况下（Index>1）进来时都不再重复发出下面的请求
            # 能够显著提高速度，并且能够提高抓取成功率: 某一页抓取错误不会影响后面的页面数据的抓取
            if index == 1:
                quotient, remainder = divmod(total_count, self.cases_per_page)
                while index <= quotient:
                    if index < quotient:
                        # yield self.re_yield(data["Param"], index+1, data["case_parties"], data["abbr_full_category"])
                        # 不再直接yield_formrequest(), 而是通过添加到Redis(TASKS_HASH)中, 然后通过start_requests生成Request
                        self.into_redis(data["Param"], index+1, data["case_parties"], data["abbr_full_category"])   # 写 消息队列 Redis(TASKS_HASH)
                    else:   # index == quotient
                        if remainder != 0:
                            # yield self.re_yield(data["Param"], index+1, data["case_parties"], data["abbr_full_category"])
                            # 不再直接yield_formrequest(), 而是通过添加到Redis(TASKS_HASH)中, 然后通过start_requests生成Request
                            self.into_redis(data["Param"], index+1, data["case_parties"], data["abbr_full_category"])   # 写 消息队列 Redis(TASKS_HASH)
                    index += 1

            # 把当前Index的self.cases_per_page条cases入库
            for case_dict in text_list[1:]:
                """
                case_dict: {'裁判要旨段原文': '本院认为，被告人王某为他人吸食毒品提供场所，其行为已构成容留他人吸毒罪，依法应予惩处。泰兴市人民检察院对被告人王某犯容留他人吸毒罪的指控成立，本院予以支持。被告人王某自动投案并如实供述自己的罪行，是自首，依法可以从轻处罚。被告人王某具有犯罪前科和多次吸毒劣迹，可酌情从重处罚。被告人王某主动向本院缴纳财产刑执行保证金，可酌情从轻处罚。关于辩护人提出“被告人王某具有自首、主动缴纳财产刑执行保证金等法定和酌定从轻处罚的情节，建议对被告人王某从轻处罚”的辩护意见，经查属实，本院予以采纳。依照《中华人民共和国刑法》第三百五十四条、第三百五十七条第一款、第六十七条第一款之规定，判决如下', '不公开理由': '', '案件类型': '1', '裁判日期': '2017-02-21', '案件名称': '王某容留他人吸毒罪一审刑事判决书', '文书ID': 'f42dfa1f-b5ca-4a22-a416-a74300f61906', '审判程序': '一审', '案号': '（2017）苏1283刑初44号', '法院名称': '江苏省泰兴市人民法院'}
                """
                # case_dict["case_details"] = ""  # 先统一置为空
                case_dict["case_parties"] = data["case_parties"]
                case_dict["abbr_full_category"] = data["abbr_full_category"]
                case_dict["crawl_date"] = datetime.datetime.now().strftime("%Y-%m-%d")    # 爬取日期
                # 说明: 爬取日期按理说应该以"发出请求"的时间为准
                # 但"发出请求"(在各个Middlewares中)时, crawl_date不能加到POST数据中;
                # 也不能以"产生请求"的时间代替, 因为产生请求的时间,并不一定发出该请求
                # 因此相比之下, 得到响应的时间与真正发出请求的时间更近
                yield self.into_mongo(case_dict)
            # self.actual_output_logger.info(json.dumps(data, ensure_ascii=False))  # 记录所有成功抓取并入库的
            self.REDIS_URI.hset(REDIS_KEY_TASKS, redis_data_str, "-1_0")     # [抓取完成] 正确抓取到所需要的数据

        except json.JSONDecodeError as jde:
            if "<title>502</title>" in response.text:
                self.error_logger.error("The website returns 502")
                time.sleep(10)  # 服务器压力大，休息会儿
            elif "remind" in response.text:
                self.error_logger.error("Bad news: the website block the spider")
                time.sleep(10)  # IP代理被禁用了，休息会儿等会儿新的代理
            else:
                self.error_logger.error("lxw_JSONDecodeError_NOTE:{0}".format(jde))
            # 针对这些抓取不成功的case, 重新yield进行抓取
            # yield self.re_yield(data)  # 若禁掉redirect连parse都进不来了; 若不禁掉redirect,跳转到502页面是通过302跳转的，那么通过response.request.body无法获取到原来的request,所以要用data
            # 不再直接yield_formrequest(), 而是通过添加到Redis(TASKS_HASH)中, 然后通过start_requests生成Request
            self.into_redis(data["Param"], int(data["Index"]), data["case_parties"], data["abbr_full_category"])   # 写 消息队列 Redis(TASKS_HASH)
        except Exception as e:
            self.error_logger.error("lxw_Exception_NOTE:{0}".format(e))
            # 针对这些抓取不成功的case, 重新yield进行抓取
            # [NO]实际上此时已经爬取成功了，不能重新yield，这种情况要求必须要提供记录哪些案例(data即可)爬取过了，哪些没有爬取，然后重爬没有爬取到的
            # yield self.re_yield(data)
            # 不再直接yield_formrequest(), 而是通过添加到Redis(TASKS_HASH)中, 然后通过start_requests生成Request
            self.into_redis(data["Param"], int(data["Index"]), data["case_parties"], data["abbr_full_category"])   # 写 消息队列 Redis(TASKS_HASH)

    # def re_yield(self, data):
    #    return self.yield_formrequest(data["Param"], int(data["Index"]), data["case_parties"], data["abbr_full_category"])

    def get_year(self):
        year_list = [year for year in range(1996, 2018)]
        for year in year_list:
            yield year

    def get_month_param(self, year):
        """
        # 此函数与get_year()/get_date()不一样，此函数直接返回param中“裁判日期”（每月）对应的值
        # 绕过每个月天数不一样，1月和12月比较特殊: 0101-0201, 0202-0301, 0302-0401, ..., 1002-1101, 1102-1201, 1202-1231
        """
        for month in range(1, 13):  # Jan - Dec
            next_month = month + 1
            if month in self.DIGIT_DICT:
                month = self.DIGIT_DICT[month]
            if next_month in self.DIGIT_DICT:
                next_month = self.DIGIT_DICT[next_month]
            if month == "01":   # str
                yield "{0}-01-01 TO {0}-02-01".format(year)
            elif month == 12:   # int
                yield "{0}-12-02 TO {0}-12-31".format(year)
            else:
                yield "{0}-{1}-02 TO {0}-{2}-01".format(year, month, next_month)

    def get_date(self, year):
        """        
        :param year: type(year): int 
        :return: str
        """
        # year_list = [year for year in range(1996, 2018)]
        # print(year_list)
        for month in range(1, 13):  # Jan - Dec
            date_list = list(range(calendar.monthrange(year, month)[1] + 1)[1:])
            if month in self.DIGIT_DICT:
                month = self.DIGIT_DICT[month]
            for date in date_list:
                if date in self.DIGIT_DICT:
                    date = self.DIGIT_DICT[date]
                yield "{0}-{1}-{2}".format(year, month, date)
                # yield "1996-01-10"    # 1
                # yield "1996-02-07"    # 1
                # yield "2016-02-07"    # 4

    def get_detail(self, doc_id, data):
        url = "http://wenshu.court.gov.cn/CreateContentJS/CreateContentJS.aspx?DocID=" + doc_id
        # url = "http://xiujinniu.com/xiujinniu/index.php"
        headers = {"Host": "wenshu.court.gov.cn", "Referer": url}
        ua = random.choice(RotateUserAgentMiddleware.user_agent_list)
        if ua:
            headers["User-Agent"] = ua
        try:
            # with proxy
            proxy = get_proxy()
            proxies = {"http": proxy, "https": proxy}  # NOTE: 这里"http"和"https"一定要都写，不能只写http或者是只写https
            req = requests.get(url=url, headers=headers, proxies=proxies, timeout=180)
            """
            # w/o proxy
            req = requests.get(url=url, headers=headers, timeout=180)
            """
            text = req.text
            json_data = ""
            match_result = re.finditer(r"jsonHtmlData.*?jsonData", text, re.S)
            for m in match_result:
                # print("in for cyclic body")
                data = m.group(0)
                right_index = data.rfind("}")
                left_index = data.find("{")
                json_data = data[left_index + 1:right_index]
                break  # this is essential. Only the first match is what we want.
            return "\"{" + json_data + "}\""
            """            
            if text:
                index = text.index('{')  # $(function() {\r\n    var jsonHtmlData = "{\\"Title\\":...
                text = text[index + 1:]  # \r\n    var jsonHtmlData = "{\\"Title\\":...
                index = text.index('{')
                text = text[index + 1:]  # \\"Title\\":...

                index = text.index('}')  # ... </div>\\"}";\r\n    var jsonData...});
                text = text[:index]
                text = "\"{" + text + "}\""
                # print(text)
                # text_str = json.loads(text)
                # text_dict = json.loads(text_str)
            return text
            """
        except Exception as e:
            self.error_logger.error("in get_detail(): {0}. data:{1}".format(e, data))
            return ""

    def into_mongo(self, case_dict):
        print(case_dict)
        cjo_item = items.CjospiderItem()
        cjo_item["abstract"] = case_dict.get("裁判要旨段原文", "")
        cjo_item["reason_not_public"] = case_dict.get("不公开理由", "")
        cjo_item["case_category"] = case_dict.get("案件类型", "")
        cjo_item["judge_date"] = case_dict.get("裁判日期", "")
        cjo_item["case_name"] = case_dict.get("案件名称", "")
        cjo_item["doc_id"] = case_dict.get("文书ID", "")
        cjo_item["judge_procedure"] = case_dict.get("审判程序", "")
        cjo_item["case_num"] = case_dict.get("案号", "")
        cjo_item["court_name"] = case_dict.get("法院名称", "")
        # cjo_item["case_details"] = case_dict.get("case_details", "")
        cjo_item["case_parties"] = case_dict.get("case_parties", "")
        cjo_item["abbr_full_category"] = case_dict.get("abbr_full_category", "")
        cjo_item["crawl_date"] = case_dict.get("crawl_date", "")
        return cjo_item

