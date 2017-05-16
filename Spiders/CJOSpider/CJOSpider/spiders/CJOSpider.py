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


class CJOSpider(scrapy.Spider):
    name = 'cjo'
    cases_per_page = 20
    stop_flag = False

    def start_requests(self):
        url = "http://wenshu.court.gov.cn/List/ListContent"
        # url = "http://xiujinniu.com/xiujinniu/index.php"   # Validating Host/Referer/User-Agent/Proxy. OK.
        index = 1
        for date in self.get_date():
            param = {}
            param["裁判日期"] = "{0} TO {0}".format(date)
            param = self.join_param(param)
            data = {
                # "Param": "案件类型:刑事案件,法院层级:高级法院",
                "Param": param,
                "Index": repr(index),
                "Page": repr(self.cases_per_page),
                "Order": "法院层级",
                "Direction": "asc",
            }

            yield scrapy.FormRequest(url=url, formdata=data, callback=self.parse)
            # yield scrapy.Request(url, method="POST", body=json.dumps(data), callback=self.parse)  # Not-working
            index += 1
            if index >= 2:
                break

    def parse(self, response):
        """
        先按序请求各个start_url， 然后才会进入到parse中(可能是异步处理的，当start_urls比较多时，可能先进入parse? 待确定, 内部实现细节和工作原理)
        """
        print("response.body:", response.body.decode("utf-8"))
        if int(json.loads(json.loads(response.body.decode("utf-8")))[0]["Count"]) > 0:
            print("here")

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
                    # yield "1996-01-10"
                    yield "1996-02-07"

    def process_response_text(self, text):
        # print(text)
        try:
            text_str = json.loads(text)
            text_list = json.loads(text_str)  # I don't know why I need json.loads() twice. ??????
            if not text_list:
                self.stop_flag = True
                return

            print("Total Page:", int(text_list[0]["Count"]))
            """
            # Count
            case_total_count = int(text_list[0]["Count"])
            quotient, remainder = divmod(case_total_count, self.cases_per_page)
            """
            for case_dict in text_list[1:]:
                """
                {'裁判要旨段原文': '本院认为，被告人王某为他人吸食毒品提供场所，其行为已构成容留他人吸毒罪，依法应予惩处。泰兴市人民检察院对被告人王某犯容留他人吸毒罪的指控成立，本院予以支持。被告人王某自动投案并如实供述自己的罪行，是自首，依法可以从轻处罚。被告人王某具有犯罪前科和多次吸毒劣迹，可酌情从重处罚。被告人王某主动向本院缴纳财产刑执行保证金，可酌情从轻处罚。关于辩护人提出“被告人王某具有自首、主动缴纳财产刑执行保证金等法定和酌定从轻处罚的情节，建议对被告人王某从轻处罚”的辩护意见，经查属实，本院予以采纳。依照《中华人民共和国刑法》第三百五十四条、第三百五十七条第一款、第六十七条第一款之规定，判决如下', '不公开理由': '', '案件类型': '1', '裁判日期': '2017-02-21', '案件名称': '王某容留他人吸毒罪一审刑事判决书', '文书ID': 'f42dfa1f-b5ca-4a22-a416-a74300f61906', '审判程序': '一审', '案号': '（2017）苏1283刑初44号', '法院名称': '江苏省泰兴市人民法院'}
                """
                # print(case_dict)
                case_dict["case_details"] = self.get_detail(case_dict["文书ID"])
                count = 0
                while not case_dict["case_details"] and count < 5:
                    case_dict["case_details"] = self.get_detail(
                        case_dict["文书ID"])  # 直到抓取到详细内容为止(或者重试了5次都失败了为止)， 减少数据缺失，数据缺失后期一定会重新补，更麻烦
                    count += 1
                self.into_mongo(case_dict)

        except json.JSONDecodeError as jde:
            print("lxw_JSONDecodeError_NOTE:", jde)
        except Exception as e:
            print("lxw_Exception_NOTE:", e)

    def get_detail(self, doc_id):
        url = "http://wenshu.court.gov.cn/CreateContentJS/CreateContentJS.aspx?DocID=" + doc_id
        headers = {"Host": "wenshu.court.gov.cn", "Referer": url}
        ua = random.choice(user_agent_list)
        if ua:
            headers["User-Agent"] = ua
        try:
            req = requests.get(url=url, headers=headers, timeout=60)
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
            print("lxw_Exception:", e)
            return ""

    def into_mongo(self, case_dict):
        print(case_dict)

    def join_param(self, param):
        """
        :param param: type(param) dict
        :return: str
        """
        str_list = []
        for key, value in param.items():
            str_list.append("{0}:{1}".format(key, value))
        return ",".join(str_list)

