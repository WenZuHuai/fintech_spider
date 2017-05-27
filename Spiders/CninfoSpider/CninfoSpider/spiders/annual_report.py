# -*- coding: utf-8 -*-
import scrapy
import requests
import json


class AnnualReportSpider(scrapy.Spider):
    name = 'annual_report'
    allowed_domains = ['cninfo.com.cn']

    def start_requests(self):
        post_url = "http://www.cninfo.com.cn/cninfo-new/announcement/query"
        for page_num in range(1,2):
            print(page_num)
            post_data = {
                "stock":"",
                "searchkey":"",
                "plate":"",
                "category:category_ndbg_szsh":"",
                "trade":"",
                "column:szse":"",
                "columnTitle": "历史公告查询",
                "pageNum": page_num,
                "pageSize": "30",
                "tabName": "fulltext",
                "sortName":"",
                "sortType":"",
                "limit":"",
                "showTitle":"",
                "seDate": "请选择日期"
            }
            print(post_data)
            # yield requests.post(
            #     url=post_url,
            #     data=post_data)
    def parse(self, response):
        content = response.content
        content = json.loads(content)
        print(content)
        print("hhhhhh")




