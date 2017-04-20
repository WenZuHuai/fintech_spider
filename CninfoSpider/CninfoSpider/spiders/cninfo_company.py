# -*- coding: utf-8 -*-
import scrapy
from urllib import parse
from scrapy.http import Request
from scrapy.loader import ItemLoader
import datetime
from CninfoSpider.items import CninfospiderItem

class CninfoCompanySpider(scrapy.Spider):
    name = "cninfo_company"
    allowed_domains = ["cninfo.com.cn"]
    start_urls = ['http://www.cninfo.com.cn/cninfo-new/information/companylist']
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
        "Referer":"http://www.cninfo.com.cn",
    }
    def parse(self, response):
        nodes1 = response.xpath('//div[@id="con-a-1"]/ul/li/a')
        nodes2 = response.xpath('//div[@id="con-a-2"]/ul/li/a')
        nodes3 = response.xpath('//div[@id="con-a-3"]/ul/li/a')
        nodes4 = response.xpath('//div[@id="con-a-4"]/ul/li/a')
        nodes = nodes1 + nodes2 + nodes3 + nodes4
        for node in nodes:
            url = node.xpath("./@href").extract_first("")
            code = node.xpath("./text()").extract_first("")
            query = parse.urlparse(url).query
            query = query.split("?")[-1]
            url = "http://www.cninfo.com.cn/information/brief/{0}.html".format(query)
            print(url)
            yield Request(url=url, meta={"code": code}, headers=self.headers, callback=self.parse_detail)


    def parse_detail(self, response):
        cninfo_item = CninfospiderItem()
        code = response.meta.get("code", "")
        cninfo_item["code"] = code
        cninfo_item["url"] = response.url
        cninfo_item["scrapy_time"] = str(datetime.datetime.now().date())
        tmp_infos = response.xpath('//tr/td[@class="zx_data2"]/text()').extract()
        infos = [item.strip() for item in tmp_infos]
        cninfo_item["company_fullname"] = infos[0]
        cninfo_item["english_name"] = infos[1]
        cninfo_item["registered_address"] = infos[2]
        cninfo_item["company_sortname"] = infos[3]
        cninfo_item["legal_representative"] = infos[4]
        cninfo_item["board_secretariat"] = infos[5]
        cninfo_item["registered_capital"] = infos[6]
        cninfo_item["business"] = infos[7]
        cninfo_item["zip_code"] = infos[8]
        cninfo_item["phone"] = infos[9]
        cninfo_item["faxes"] = infos[10]
        cninfo_item["website"] = infos[11]
        cninfo_item["time_market"] = infos[12]
        cninfo_item["time_listing"] = infos[13]
        cninfo_item["issure_price"] = infos[14]
        cninfo_item["issure_number"] = infos[15]
        cninfo_item["issure_ratio"] = infos[16]
        cninfo_item["issure_way"] = infos[17]
        cninfo_item["underwriter"] = infos[18]
        cninfo_item["referrer"] = infos[19]
        cninfo_item["sponsor_institution"] = infos[20]
        yield cninfo_item



