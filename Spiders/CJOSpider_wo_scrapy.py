#!/usr/bin/env python3
# coding: utf-8
# File: CJOSpider_wo_scrapy.py
# Author: lxw
# Date: 5/11/17 5:23 PM

import codecs
import random
import requests
from requests import Request, Session

from Spiders.public_utils import user_agent_list
from Spiders.public_utils import get_proxy
from Spiders.public_utils import get_proxy_xcdl


def main():
    # url = "http://wenshu.court.gov.cn/List/ListContent?MmEwMD=1JpvOqOnfbRJY.ls32KFV38zmLyBRRktcWoysenn2IJqvgfLVMpoAecg1kGJ.aGYFF2XnoT6p8s.gST9LgzK25YqA6H_5s4i_2.eQE1dDLRIZzqIWqk9Vx8wRbdHHMJUxiS_Z5QTD1_5xvWkpong96yuqp79s0DxEAujonmjd3hfauzwIH8X7KX0Ky988Ts0Zo7UsppQTPqS6N7K8oogSZxqDBiGoOl2vK19zj6eoz7BZ4UKBg_MAQQusagJ7DYvtBbenxgeGOEH_Rd2GngtWzi2z7cSgfuiNQMxGIa7bdws9hN0k6zQEloHJI.J9B6bMHkTIi5b09H1LXvFusdb951fFTe3TpP.nYYxG_FEQn9x2",
    url = "http://wenshu.court.gov.cn/List/TreeList?MmEwMD=11KKII9kwy8ZN0kP9_p.LoRQy6582Dl45sqEBPTkRqtSMvbRLlKC7PmxXQvZUBv9bmPIi3nDzrVFlXnYVvjvRf1aVSYvUF61DUMXZjx1BqaeKSR.t8KyS1H6zyZIfVf_24u4t6Vl9510i7uJyC0ZtaFaNrb0WFULUu5UkP7v7d60gMUy0DYfs6gcPkPcVKhiVn0FxYzDDtViUnzZvDhECggmyUSb1y.Y_xKYmz4Y2KG6bHJEPGKMEcOUl16ag8D6YCNjpUL5a.epQpnznE2.UHTBhdIp4KnFqPNBI6fgGRnqJkUreRyzmLFPZ9zJPlAz0oRX3.AkWSGcvWgT8r28lM24AQikr2v.jcALBhk3Brfd_"
    # url = "http://www.ip138.com/ua.asp"    # 查看当前请求的User-Agent和所使用的IP
    # url = "http://xiaoweiliu.cn"    # 查看当前请求的User-Agent和所使用的IP
    # data = {"MmEwMD" : "1zNNGGMZPDfkKhZwMmXVUgbODErfFy4lr7d6AwtZbdTi93RbU4Nxsw_CpO3kLA3MR_wGSvJy15.24pJj.3Y3b8zWJ.G4Xxqns.3EIlRFFACRYsuiNKfIJgsB4tpl0Juc8U8x.xl5oN_o7vDCLWiiZQEBw5tC3fCUoW3rxzmW44A3HprFvahmwo8CaFNKY5ukv9YVplA7B5sOVR2wc0LjbMlx_uGEyVhMh.ZPGcsKQpaeyF5D8nmEwwfQncMLyPutHDZcNUnvhVoVsngQIwuHgvYezjaA5e3shBaGMt.hJ4bnzXKdjnW9UDhaFpc9yzOevHmKGlDYx31Vl2zy0yl0C9N9s3bG0Gwt0uwHAAQNQO6qM"}
    data = {"MmEwMD":"11KKII9kwy8ZN0kP9_p.LoRQy6582Dl45sqEBPTkRqtSMvbRLlKC7PmxXQvZUBv9bmPIi3nDzrVFlXnYVvjvRf1aVSYvUF61DUMXZjx1BqaeKSR.t8KyS1H6zyZIfVf_24u4t6Vl9510i7uJyC0ZtaFaNrb0WFULUu5UkP7v7d60gMUy0DYfs6gcPkPcVKhiVn0FxYzDDtViUnzZvDhECggmyUSb1y.Y_xKYmz4Y2KG6bHJEPGKMEcOUl16ag8D6YCNjpUL5a.epQpnznE2.UHTBhdIp4KnFqPNBI6fgGRnqJkUreRyzmLFPZ9zJPlAz0oRX3.AkWSGcvWgT8r28lM24AQikr2v.jcALBhk3Brfd_"}
    response = requests.post(url, data=data)
    # print(response.text.encode("utf-8"))
    print(response.text.replace("\\u0027", "'"))


def post_crawl():
    url = "http://wenshu.court.gov.cn/List/ListContent"
    data = {
        "Param": "案件类型:刑事案件,裁判年份:2004",
        # "Param": "",
        "Index": 1,
        "Page": 5,
        "Order": "法院层级",
        "Direction": "asc",
    }

    s = Session()

    try:
        # response = requests.post(url=url, data=data)
        headers = {"Referer": "http://wenshu.court.gov.cn/"}
        ua = random.choice(user_agent_list)
        if ua:
            print("Using User-Agent:", ua)
            headers["User-Agent"] = ua

        print("headers", headers)

        # req = Request("POST", url=url, data=data, headers=headers)
        req = Request("POST", url=url, data=data, headers=headers)
        prepped = s.prepare_request(req)
        # response = s.send(prepped, proxies, timeout)     # http://blog.csdn.net/qq_18863573/article/details/52775130

        # with proxy
        try:
            # proxy = get_proxy()    # proxy: "119.75.213.61:80"
            proxy = get_proxy_xcdl()    # proxy: "119.75.213.61:80"
        except Exception as e:
            print("lxw_Excetion_get_proxy_xcdl", e)
            response = s.send(prepped, timeout=60)
        else:
            proxies = {
                "http": proxy,
                "https": proxy,
            }
            response = s.send(prepped, proxies=proxies, timeout=60)

        # w/o proxy
        response = s.send(prepped, timeout=60)
    except Exception as e:
        print("lxw_Exception", e)
    else:
        print(response.text)


if __name__ == "__main__":
    # main()
    post_crawl()
