#!/usr/bin/env python3
# coding: utf-8
# File: CJOSpider.py
# Author: lxw
# Date: 5/11/17 3:57 PM

import calendar
import json
import random
import requests
import scrapy
import urllib.parse

from Spiders.CJOSpider.CJOSpider.middlewares import RotateUserAgentMiddleware
from Spiders.CJOSpider.get_proxy import get_proxy


class CJOSpider(scrapy.Spider):
    name = 'cjo'
    cases_per_page = 20
    stop_flag = False
    CRAWL_LIMIT = 200
    # CRAWL_LIMIT = 0
    url = "http://wenshu.court.gov.cn/List/ListContent"
    # url = "http://xiujinniu.com/xiujinniu/index.php"   # Validating Host/Referer/User-Agent/Proxy. OK.
    CASE_CATEGORY = ["刑事案件", "民事案件", "行政案件", "赔偿案件", "执行案件"]    # 案件类型
    COURT_CATEGORY = ["最高法院", "高级法院", "中级法院", "基层法院"]   # 法院层级
    DOC_CATEGORY = ["判决书", "裁定书", "调解书", "决定书", "通知书", "批复", "答复", "函", "令", "其他"]  # 文书类型
    JUDGE_PROCEDURE = ["一审", "二审", "再审", "复核", "刑罚变更", "再审审查与审判监督", "其他"]   # 审判程序

    def start_requests(self):
        index = 1
        for date in self.get_date():
            param = {}
            param["裁判日期"] = "{0} TO {0}".format(date)
            param["案件类型"] = "执行案件"
            param["法院层级"] = "基层法院"
            param = self.join_param(param)

            yield self.yield_formrequest(param, index)

            index += 1
            if index >= 2:
                break

    def yield_formrequest(self, param, index):
        data = {
            # "Param": "案件类型:刑事案件,法院层级:高级法院",
            "Param": param,
            "Index": repr(index),
            "Page": repr(self.cases_per_page),
            "Order": "法院层级",
            "Direction": "asc",
        }

        if index > 1:
            print("in yield_formrequest(): index > 1")

        temp_data = "?{0}".format(urllib.parse.urlencode(data))
        return scrapy.FormRequest(url=self.url+temp_data, formdata=data, callback=self.parse, dont_filter=True)
        # yield scrapy.Request(url, method="POST", body=json.dumps(data), callback=self.parse)  # Not-working

    def parse(self, response):
        """
        先按序请求各个start_url， 然后才会进入到parse中(可能是异步处理的，当start_urls比较多时，可能先进入parse? 待确定, 内部实现细节和工作原理)
        """
        # print("response.text:", response.text)
        text = response.text
        try:
            text_str = json.loads(text)
            text_list = json.loads(text_str)  # I don't know why I need json.loads() twice. ??????

            # TODO: MODIFICATION IS NEEDED. what is text_list?
            if not text_list:   # [{'Count': '0'}] or  [{'Count': '1'},{'裁判要旨段原文': '本院认为，被告人王某为他人吸食毒品提供场所，其行为已构成容留他人吸毒罪，依法应予惩处。泰兴市人民检察院对被告人王某犯容留他人吸毒罪的指控成立，本院予以支持。被告人王某自动投案并如实供述自己的罪行，是自首，依法可以从轻处罚。被告人王某具有犯罪前科和多次吸毒劣迹，可酌情从重处罚。被告人王某主动向本院缴纳财产刑执行保证金，可酌情从轻处罚。关于辩护人提出“被告人王某具有自首、主动缴纳财产刑执行保证金等法定和酌定从轻处罚的情节，建议对被告人王某从轻处罚”的辩护意见，经查属实，本院予以采纳。依照《中华人民共和国刑法》第三百五十四条、第三百五十七条第一款、第六十七条第一款之规定，判决如下', '不公开理由': '', '案件类型': '1', '裁判日期': '2017-02-21', '案件名称': '王某容留他人吸毒罪一审刑事判决书', '文书ID': 'f42dfa1f-b5ca-4a22-a416-a74300f61906', '审判程序': '一审', '案号': '（2017）苏1283刑初44号', '法院名称': '江苏省泰兴市人民法院'}]
                self.stop_flag = True
                return

            body = urllib.parse.unquote_plus(response.request.body.decode("utf-8"), encoding="utf-8")
            # body: "Param=裁判日期:2016-02-07 TO 2016-02-07,案件类型:刑事案件&Index=1&Page=20&Order=法院层级&Direction=asc"
            print(body)
            body_list = body.split("&")
            index = int(body_list[1].split("=")[1])  # body_list[1]: "Index=1"
            if index > 1:
                print("index > 1")

            total_count = int(text_list[0]["Count"])
            print("Count:", total_count)
            if total_count == 0:
                return
            elif total_count > self.CRAWL_LIMIT:  # 依靠 “日期”/“日期+案件类型”/“日期+案件类型+法院层级”/ “日期+案件类型+法院层级+文书类型”/“日期+案件类型+法院层级+文书类型+审判程序” 将查询结果限定到2000条以内
                body = urllib.parse.unquote_plus(response.request.body.decode("utf-8"), encoding="utf-8")
                # body: "Param=裁判日期:2016-02-07 TO 2016-02-07,案件类型:刑事案件&Index=1&Page=20&Order=法院层级&Direction=asc"
                body_list = body.split("&")
                param = body_list[0]    # "Param=裁判日期:2016-02-07 TO 2016-02-07,案件类型:刑事案件"
                origin_param = param.split("=")[1]  # "裁判日期:2016-02-07 TO 2016-02-07,案件类型:刑事案件"
                origin_param_list = origin_param.split(",")
                index = int(body_list[1].split("=")[1])    # body_list[1]: "Index=1"
                length = len(origin_param_list)
                if length == 1:    # 只有“日期”，改用“日期+案件类型”进行筛选
                    """
                    for category in self.CASE_CATEGORY:
                        temp_param = "{0},案件类型:{1}".format(origin_param, category)
                        yield self.yield_formrequest(temp_param, index)
                    return
                    """
                    temp_param = "{0},案件类型:{1}".format(origin_param, "执行案件")
                    yield self.yield_formrequest(temp_param, index)
                    return
                elif length == 2:   # “日期+案件类型”，改用“日期+案件类型+法院层级”进行筛选
                    """
                    for category in self.COURT_CATEGORY:
                        temp_param = "{0},法院层级:{1}".format(origin_param, category)
                        yield self.yield_formrequest(temp_param, index)
                    return
                    """
                    temp_param = "{0},法院层级:{1}".format(origin_param, "基层法院")
                    yield self.yield_formrequest(temp_param, index)
                    return
                elif length == 3:   # “日期+案件类型+法院层级”，改用“日期+案件类型+法院层级+文书类型”进行筛选
                    for category in self.DOC_CATEGORY:
                        temp_param = "{0},文书类型:{1}".format(origin_param, category)
                        yield self.yield_formrequest(temp_param, index)
                    return
                elif length == 4:   # “日期+案件类型+法院层级+文书类型”，改用“日期+案件类型+法院层级+文书类型+审判程序”进行筛选
                    # NOTE: "赔偿案件" 和 "执行案件" 不能使用审判程序进行筛选，网页上就是这样的
                    if "赔偿案件" in origin_param_list[1] or "执行案件" in origin_param_list[1]:
                        pass    # 无法再精确，先把这self.CRAWL_LIMIT条数据入库，并把当前的param打印出来，另行处理
                    else:
                        for category in self.JUDGE_PROCEDURE:
                            temp_param = "{0},审判程序:{1}".format(origin_param, category)
                            yield self.yield_formrequest(temp_param, index)
                        return
                else:   # 无法再精确，先把这self.CRAWL_LIMIT条数据入库，并把当前的param打印出来，另行处理
                    print("-" * 30, "lxw_CRITICAL", param)
                    # DO NOT return.    # 继续下面的入库操作，先把这两千条入库
            else:   # total_count > 0 && total_count < self.CRAWL_LIMIT
                self.re_yield(response.request.body, next_index=True)
                # urllib.parse.unquote_plus(response.request.body.decode("utf-8"), encoding="utf-8"): "Param=裁判日期:2016-02-07 TO 2016-02-07,案件类型:刑事案件&Index=1&Page=20&Order=法院层级&Direction=asc"

                # Just continue to run the following code

            for case_dict in text_list[1:]:
                """
                case_dict: {'裁判要旨段原文': '本院认为，被告人王某为他人吸食毒品提供场所，其行为已构成容留他人吸毒罪，依法应予惩处。泰兴市人民检察院对被告人王某犯容留他人吸毒罪的指控成立，本院予以支持。被告人王某自动投案并如实供述自己的罪行，是自首，依法可以从轻处罚。被告人王某具有犯罪前科和多次吸毒劣迹，可酌情从重处罚。被告人王某主动向本院缴纳财产刑执行保证金，可酌情从轻处罚。关于辩护人提出“被告人王某具有自首、主动缴纳财产刑执行保证金等法定和酌定从轻处罚的情节，建议对被告人王某从轻处罚”的辩护意见，经查属实，本院予以采纳。依照《中华人民共和国刑法》第三百五十四条、第三百五十七条第一款、第六十七条第一款之规定，判决如下', '不公开理由': '', '案件类型': '1', '裁判日期': '2017-02-21', '案件名称': '王某容留他人吸毒罪一审刑事判决书', '文书ID': 'f42dfa1f-b5ca-4a22-a416-a74300f61906', '审判程序': '一审', '案号': '（2017）苏1283刑初44号', '法院名称': '江苏省泰兴市人民法院'}
                """
                case_dict["case_details"] = self.get_detail(case_dict["文书ID"])
                count = 0
                # 直到抓取到详细内容为止(或者重试了5次都失败了为止)， 减少数据缺失，数据缺失后期一定会重新补，更麻烦
                while not case_dict["case_details"] and count < 5:
                    case_dict["case_details"] = self.get_detail(case_dict["文书ID"])
                    count += 1
                self.into_mongo(case_dict)
        except json.JSONDecodeError as jde:
            if "<title>502</title>" in response.text:
                print("The website returns 502")
            elif "remind" in response.text:
                print("Bad news: the website block the spider")
            else:
                print("lxw_JSONDecodeError_NOTE:", jde)
            # print(response.body)
            # 针对这些抓取不成功的case, 重新yield进行抓取
            yield self.re_yield(response.request.body)  # Not working, 跳转到502页面是通过302跳转的，所以通过response.request.body无法获取到原来的request
        except Exception as e:
            print("lxw_Exception_NOTE:", e)
            # print(response.body)
            # 针对这些抓取不成功的case, 重新yield进行抓取
            yield self.re_yield(response.request.body)    # TODO: 是否好使，还需测试

    def re_yield(self, body, next_index=False):
        body = urllib.parse.unquote_plus(body.decode("utf-8"), encoding="utf-8")
        # body: "Param=裁判日期:2016-02-07 TO 2016-02-07,案件类型:刑事案件&Index=1&Page=20&Order=法院层级&Direction=asc"
        body_list = body.split("&")
        param = body_list[0]  # "Param=裁判日期:2016-02-07 TO 2016-02-07,案件类型:刑事案件"
        param = param.split("=")[1]  # "裁判日期:2016-02-07 TO 2016-02-07,案件类型:刑事案件"
        index = int(body_list[1].split("=")[1])    # body_list[1]: "Index=1"
        if next_index:
            return self.yield_formrequest(param, index+1)
        else:
            return self.yield_formrequest(param, index)

    def get_date(self):
        year_list = [year for year in range(1996, 2018)]
        # print(year_list)
        digit_dict = {1: "01", 2: "02", 3: "03", 4: "04", 5: "05", 6: "06", 7: "07", 8: "08", 9: "09"}     # 只处理单个的数字即可
        for year in year_list:
            for month in range(1, 13):  # Jan - Dec
                date_list = list(range(calendar.monthrange(year, month)[1] + 1)[1:])
                if month in digit_dict:
                    month = digit_dict[month]
                for date in date_list:
                    if date in digit_dict:
                        date = digit_dict[date]
                    # yield "{0}-{1}-{2}".format(year, month, date)
                    # yield "1996-01-10"    # 1
                    # yield "1996-02-07"    # 1
                    yield "2016-02-07"    # 4

    def get_detail(self, doc_id):
        url = "http://wenshu.court.gov.cn/CreateContentJS/CreateContentJS.aspx?DocID=" + doc_id
        # url = "http://xiujinniu.com/xiujinniu/index.php"
        headers = {"Host": "wenshu.court.gov.cn", "Referer": url}
        ua = random.choice(RotateUserAgentMiddleware.user_agent_list)
        if ua:
            headers["User-Agent"] = ua
        try:
            """
            # with proxy
            proxy = get_proxy()
            proxies = {"http": proxy, "https": proxy}  # NOTE: 这里"http"和"https"一定要都写，不能只写http或者是只写https
            req = requests.get(url=url, headers=headers, proxies=proxies, timeout=120)
            """
            # w/o proxy
            req = requests.get(url=url, headers=headers, timeout=120)

            text = req.text
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
        except Exception as e:
            return ""

    def into_mongo(self, case_dict):
        print(case_dict)
        # pass

    def join_param(self, param):
        """
        :param param: type(param) dict
        :return: str
        """
        str_list = []
        for key, value in param.items():
            str_list.append("{0}:{1}".format(key, value))
        return ",".join(str_list)
