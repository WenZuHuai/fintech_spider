#!/usr/bin/env python3
# coding: utf-8
# File: CJOSpider_wo_scrapy.py
# Author: lxw
# Date: 5/11/17 5:23 PM


import json
import random
import requests
from requests import Request, Session

from Spiders.public_utils import check_proxy_alive
# from Spiders.public_utils import get_proxy
from Spiders.public_utils import get_proxy_xcdl
from Spiders.public_utils import get_proxy_xcdl_localfile
from Spiders.public_utils import user_agent_list
from Spiders.public_utils import get_proxy_dxdl


class CJOSpider():
    """
    w/o Scrapy.
    """
    cases_per_page = 20
    stop_flag = False

    def post_crawl(self, index):
        url = "http://wenshu.court.gov.cn/List/ListContent"
        # url = "http://xiujinniu.com/xiujinniu/index.php"   # Validating Host/Referer/User-Agent/Proxy. OK.
        data = {
            # "Param": "案件类型:刑事案件,裁判年份:2004",
            # "Param": "案件类型:刑事案件,裁判日期:2017-04-01 TO 2017-04-01,法院层级:高级法院",
            "Param": "裁判日期:1996-01-10 TO 1996-01-10",   # "1996-01-10": 1, "1996-02-07": 1
            "Index": index,
            "Page": self.cases_per_page,
            "Order": "法院层级",
            "Direction": "asc",
        }

        s = Session()

        try:
            # response = requests.post(url=url, data=data)
            headers = {"Host": "wenshu.court.gov.cn", "Referer": "http://wenshu.court.gov.cn/List/List"}
            ua = random.choice(user_agent_list)
            if ua:
                headers["User-Agent"] = ua

            print("headers", headers)

            req = Request("POST", url=url, data=data, headers=headers)
            prepped = s.prepare_request(req)

            """
            # with proxy
            try:
                count = 0
                while 1:
                    # proxy = get_proxy()    # proxy: "119.75.213.61:80"
                    # proxy = get_proxy_xcdl()    # proxy: "119.75.213.61:80"
                    proxy = get_proxy_xcdl_localfile()    # proxy: "119.75.213.61:80"
                    if check_proxy_alive(proxy):
                        print("proxy {0} is Available.".format(proxy))
                        break
                    count += 1
                    if count > 5:
                        raise Exception("lxw_Exception: getting proxy tried too many times")
            except Exception as e:
                print("lxw_Excetion_getting_proxy_error", e)
                response = s.send(prepped, timeout=60)
            else:
                proxies = {
                    "http": proxy,
                    "https": proxy,
                }
                response = s.send(prepped, proxies=proxies, timeout=60)    # http://blog.csdn.net/qq_18863573/article/details/52775130
            """

            """
            proxy = get_proxy_dxdl()
            proxies = {
                "http": proxy,
                "https": proxy,
            }
            response = s.send(prepped, proxies=proxies, timeout=60)    # http://blog.csdn.net/qq_18863573/article/details/52775130
            """

            # w/o proxy
            response = s.send(prepped, timeout=60)
        except Exception as e:
            print("lxw_Exception", e)
        else:
            self.process_response_text(response.text)

    def process_response_text(self, text):
        # print(text)
        try:
            text_str = json.loads(text)
            text_list = json.loads(text_str)    # I don't know why I need json.loads() twice. ??????
            if not text_list:
                self.stop_flag = True
                return

            print("Total Count:", int(text_list[0]["Count"]))
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
                    case_dict["case_details"] = self.get_detail(case_dict["文书ID"])  # 直到抓取到详细内容为止(或者重试了5次都失败了为止)， 减少数据缺失，数据缺失后期一定会重新补，更麻烦
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
            req = requests.get(url=url, headers=headers, timeout=10)
            text = req.text
            if text:
                index = text.index('{')    # $(function() {\r\n    var jsonHtmlData = "{\\"Title\\":...
                text = text[index+1:]    # \r\n    var jsonHtmlData = "{\\"Title\\":...
                index = text.index('{')
                text = text[index+1:]    # \\"Title\\":...

                index = text.index('}')    # ... </div>\\"}";\r\n    var jsonData...});
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


def no_use():
    # url = "http://wenshu.court.gov.cn/List/ListContent?MmEwMD=1JpvOqOnfbRJY.ls32KFV38zmLyBRRktcWoysenn2IJqvgfLVMpoAecg1kGJ.aGYFF2XnoT6p8s.gST9LgzK25YqA6H_5s4i_2.eQE1dDLRIZzqIWqk9Vx8wRbdHHMJUxiS_Z5QTD1_5xvWkpong96yuqp79s0DxEAujonmjd3hfauzwIH8X7KX0Ky988Ts0Zo7UsppQTPqS6N7K8oogSZxqDBiGoOl2vK19zj6eoz7BZ4UKBg_MAQQusagJ7DYvtBbenxgeGOEH_Rd2GngtWzi2z7cSgfuiNQMxGIa7bdws9hN0k6zQEloHJI.J9B6bMHkTIi5b09H1LXvFusdb951fFTe3TpP.nYYxG_FEQn9x2",
    url = "http://wenshu.court.gov.cn/List/TreeList?MmEwMD=11KKII9kwy8ZN0kP9_p.LoRQy6582Dl45sqEBPTkRqtSMvbRLlKC7PmxXQvZUBv9bmPIi3nDzrVFlXnYVvjvRf1aVSYvUF61DUMXZjx1BqaeKSR.t8KyS1H6zyZIfVf_24u4t6Vl9510i7uJyC0ZtaFaNrb0WFULUu5UkP7v7d60gMUy0DYfs6gcPkPcVKhiVn0FxYzDDtViUnzZvDhECggmyUSb1y.Y_xKYmz4Y2KG6bHJEPGKMEcOUl16ag8D6YCNjpUL5a.epQpnznE2.UHTBhdIp4KnFqPNBI6fgGRnqJkUreRyzmLFPZ9zJPlAz0oRX3.AkWSGcvWgT8r28lM24AQikr2v.jcALBhk3Brfd_"
    # url = "http://www.ip138.com/ua.asp"    # 查看当前请求的User-Agent和所使用的IP
    data = {"MmEwMD":"11KKII9kwy8ZN0kP9_p.LoRQy6582Dl45sqEBPTkRqtSMvbRLlKC7PmxXQvZUBv9bmPIi3nDzrVFlXnYVvjvRf1aVSYvUF61DUMXZjx1BqaeKSR.t8KyS1H6zyZIfVf_24u4t6Vl9510i7uJyC0ZtaFaNrb0WFULUu5UkP7v7d60gMUy0DYfs6gcPkPcVKhiVn0FxYzDDtViUnzZvDhECggmyUSb1y.Y_xKYmz4Y2KG6bHJEPGKMEcOUl16ag8D6YCNjpUL5a.epQpnznE2.UHTBhdIp4KnFqPNBI6fgGRnqJkUreRyzmLFPZ9zJPlAz0oRX3.AkWSGcvWgT8r28lM24AQikr2v.jcALBhk3Brfd_"}
    response = requests.post(url, data=data)
    print(response.text.replace("\\u0027", "'"))


if __name__ == "__main__":
    cjo = CJOSpider()
    current_page = 1
    while not cjo.stop_flag:
        cjo.post_crawl(current_page)
        current_page += 1
        break
