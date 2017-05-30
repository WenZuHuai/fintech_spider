import requests
import json
import pymongo
import math
from urllib.parse import urljoin
import os
# response = requests.get("http://www.cninfo.com.cn/cninfo-new/js/data/szse_stock.json")


def announcement(orgId,category,code,zwjc,page="1"):
    index = 1
    url = "http://www.cninfo.com.cn/cninfo-new/announcement/query"
    post_data = {
        "stock": "{},{};".format(code,orgId),
        "searchkey": "",
        "plate": "",
        "category": "category_ndbg_szsh;",
        "trade": "",
        "column:szse": "",
        "columnTitle": "历史公告查询",
        "pageNum": page,
        "pageSize": "30",
        "tabName": "fulltext",
        "sortName": "",
        "sortType": "",
        "limit": "",
        "showTitle": "",
        "seDate": "category_ndbg_szsh/category/年度报告;{},{}/stock/{} {}".format(code,orgId,code,zwjc)
    }
    while True:
        try:
            if index>5:
                return False,None
                break
            response = requests.post(url=url, data=post_data)
            content = response.content
            content = json.loads(content)
            return True,[content["totalAnnouncement"], content['announcements']]
        except:
            index += 1

def run():
    client = pymongo.MongoClient(host="192.168.1.36", port=27017)
    db = client["scrapy"]
    col = db["companyDict"]
    col2 = db["annualReport20170516"]
    for item in col.find():
        print(item)
        tag,body= announcement(item["orgId"],item['category'],item['code'],item['zwjc'])
        if not tag:
            continue
        for page in range(math.ceil(int(body[0])/30)):
            tag,body = announcement(item["orgId"], item['category'], item['code'], item['zwjc'],page=page+1)
            if not tag:
                continue
            col2.insert(body[1])
def writeurl():
    client = pymongo.MongoClient(host="192.168.1.36", port=27017)
    db = client["scrapy"]
    col = db["annualReport20170516"]
    fp = open("urls.txt","w")
    for item in col.find():
        atype = item["adjunctType"]
        if atype !="PDF":
            continue
        aurl = item["adjunctUrl"]
        link = urljoin("http://www.cninfo.com.cn",aurl)
        print(link)
        log = "{}****{}****{}\n".format(item["secCode"],link,item["announcementTitle"])
        fp.write(log)
    fp.close()
def downpdf():
    client = pymongo.MongoClient(host="192.168.1.36", port=27017)
    db = client["scrapy"]
    col = db["annualReport20170516"]
    for item in col.find():
        atype = item["adjunctType"]
        if atype !="PDF":
            continue
        aurl = item["adjunctUrl"]
        link = urljoin("http://www.cninfo.com.cn",aurl)
        request = requests.get(link)
        file_tag = os.path.exists(item["secCode"])
        if file_tag:
            pass
        else:
            os.mkdir(item["secCode"])
        file_name = "{}/{}.pdf".format(item['secCode'],item['announcementTitle'])
        with open(file_name, "wb") as code:
            code.write(request.content)
        break


if __name__ == "__main__":
    # run()
    downpdf()