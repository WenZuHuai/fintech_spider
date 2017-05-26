### 抓取思路
抓取过程包括两个关键步骤
1.抓取案件的概要信息(尤其是DocID)
http://wenshu.court.gov.cn/List/ListContent?MmEwMD=1ludmxrjoB4YuPbh570cnpZTOfM6dAf19m2fT0AjkKB3rSkan1uIC0GG0tcYJycJZsoCViUB6USu8gUZiSHik66RvDg2ajSnvuPILVLopaNTOMP7iFm24CxKM0G.kotRU.9ryhc0dWbSW09PfPeBya5Myom9Mr85dt74kLTggN2qafVpiuN.tdwuxe1YPo0rO5zzd6jtrwYETO08.QR4bIM5k68QoPRPpC0tsxmur04zMFiFBxIWJXjUaS8GgYaXXqIGpluooABmztqzkJvlfbJ6Hobwsy9JOtUiM.QnfwK0cqRaqTlNaGgJtg6FHytKTZGfXJFTmwjSmRXcmqYX5FG7Pqt81847ALxu_ehEd6Pzh2tOi4tafV49HhlkrLJtmtJ

POST
"Param": "案件类型:刑事案件",
"Index": 5,
"Page": 20,
"Order": "法院层级",
"Direction": "asc",

本来想通过构造上面的URL来爬取,阅读Assets/js/Lawyee.CPWSW.List.js和Assets/js/Lawyee.CPWSW.ListLoad.js,发现其中应该包含URL的构建代码
但后来发现直接访问"http://wenshu.court.gov.cn/List/ListContent",然后以POST的形式提供上面的5个参数就可以实现抓取

针对这一步骤的爬取代码的具体实现参见[Spiders/CJOSpider/CJOSpider/CJOSpider.py](https://github.com/hee0624/fintech_spider/blob/master/Spiders/CJOSpider/CJOSpider/spiders/CJOSpider.py)
具体的思路如下：
1)以公司名称(简称/全称)作为"当事人"过滤条件进行爬取
2)若1)中的"当事人"超过CJOSpider.CRAWL_LIMIT，则再按照"案件类型"进行过滤("当事人"+"案件类型")
3)若2)中的"案件类型"超过CJOSpider.CRAWL_LIMIT，则再按照"法院层级"进行过滤("当事人"+"案件类型"+"法院层级")
4)若3)中的"法院层级"超过CJOSpider.CRAWL_LIMIT，则再按照"日期"(每年/每月/每天)进行过滤("当事人"+"案件类型"+"法院层级"+"日期")
每年: 裁判年份:2017    每月/每天: 裁判日期:2017-05-01 TO 2017-05-31/裁判日期:2017-05-01 TO 2017-05-01
5)若4)中的"日期"超过CJOSpider.CRAWL_LIMIT，则再按照"文书类型"进行过滤("当事人"+"案件类型"+"法院层级"+"日期"+"文书类型")
6)若5)中的"文书类型"超过CJOSpider.CRAWL_LIMIT，则再按照"审判程序"进行过滤("当事人"+"案件类型"+"法院层级"+"日期"+"文书类型"+"审判程序")

2.针对每个案件的详细内容,需要得到当前案件的DocID,然后通过http://wenshu.court.gov.cn/CreateContentJS/CreateContentJS.aspx?DocID=69f56346-9ac8-4361-bdd9-8a1a40918234获取网页的内容即可(GET)
Referer:http://wenshu.court.gov.cn/List/List?sorttype=1&conditions=searchWord+1+AJLX++%E6%A1%88%E4%BB%B6%E7%B1%BB%E5%9E%8B:%E5%88%91%E4%BA%8B%E6%A1%88%E4%BB%B6


需要注意的是处理过程:
把每页的POST请求和doc_id详情的请求分开,异步处理
每个案例的各个字段入mongo,并且将doc_id入redis
然后另一个爬虫去从redis中读取doc_id,然后爬取doc_id对应的详情, 并入另一个mongo

### 其他说明
1."案件类型"分类：
刑事案件: 1
民事案件: 2
行政案件: 3
赔偿案件: 4
执行案件: 5
