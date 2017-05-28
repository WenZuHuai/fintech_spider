# fintech_spider
**_fintech(i.e. financial technology)_**

"**fintech_spider**" is a spider based on [Scrapy](https://scrapy.org/) to crawl a large number of financial data on the Internet.

The data crawled by "**fintech_spider**" has been used by [嗅金牛](http://xiujinniu.com/xiujinniu/index.php), [数知源](http://datazhiyuan.com/datazhiyuan/index.php).


### Structrue of fintech_spider

| Directory | Author | Usage |
|------|:------:|------|
| Anti_Anti_Spider | [hee](https://github.com/hee0624) |  |
| | |
| demo |  | Some Demonstrations(e.g. PhantomJS/Proxies, etc.) |
| demo/ArticleSpider | [lxw](https://github.com/hee0624) |  |
| demo/geetestcrack.py | [hee](https://github.com/hee0624) |  |
| demo/phantomjs_proxy | [lxw](https://github.com/lxw0109) | Add IP proxy in PhantomJS |
| demo/user_agent.txt | [hee](https://github.com/hee0624) | A large number of User-Agents |
| | |
| README.md | [lxw](https://github.com/lxw0109) | The document for this project |
| | |
| Spiders |  | The Spiders directory stores Python scripts that crawl data we need from the Internet) |
| Spiders/CJO_case_demo.md | [lxw](https://github.com/lxw0109) | Some case and The main idea about how to crawl data from [中国裁判文书网](http://wenshu.court.gov.cn/)(China Judgements Online) |
| Spiders/CJOSpider | [lxw](https://github.com/lxw0109) | (w/ scrapy)Spiders for crawling data from [中国裁判文书网](http://wenshu.court.gov.cn/)(China Judgements Online) |
| Spiders/CJOSpider_wo_scrapy.py | [lxw](https://github.com/lxw0109) | (w/o scrapy)Spiders for crawling data from [中国裁判文书网](http://wenshu.court.gov.cn/)(China Judgements Online) |
| Spiders/CninfoSpider | [hee](https://github.com/hee0624) | Spiders for crawling data from [巨潮资讯](http://www.cninfo.com.cn/cninfo-new/information/companylist) |
| Spiders/CNKI_Patent | [lxw](https://github.com/lxw0109) | Spiders for crawling the patent data from [中国知网](http://kns.cnki.net/kns/brief/default_result.aspx) |
| Spiders/NECIPSSpider | [lxw](https://github.com/lxw0109) | Spiders for crawling data from [国家企业信用信息公示系统](http://www.gsxt.gov.cn/corp-query-homepage.html)(National Enterprise Credit Information Publicity System) |
| Spiders/NECIPSSpider_wo_scrapy.py | [lxw](https://github.com/lxw0109) | Spiders(w/o Scrapy) for crawling data from [国家企业信用信息公示系统](http://www.gsxt.gov.cn/corp-query-homepage.html)(National Enterprise Credit Information Publicity System) |
| Spiders/new_three_board | [lxw](https://github.com/lxw0109) | Spiders for crawling data from [全国中小企业股份转让系统](http://www.neeq.com.cn/nq/listedcompany.html) |


### TODO
**[He Chen](https://github.com/hee0624)**:
1. 在README.md中更新所提交的各个目录的用途(如果子目录中有关键的文件，也请列出)

**[Xiaowei Liu](https://github.com/lxw0109)**:
+ **CJOSpider**
 0. 爬取次数记录
 1. 部署到线上,跑全部公司的数据
 1. 增加对Redis中DOC_ID_HASH的爬取代码


本地和线上区别,修改的地方
settings.py:
1. 启用proxy
2. MONGO_HOST
3. REDIS_HOST

init_tasks_hash_CJOSpider.py
REDIS_HOST



+ **NECIPSSpider**
 0. add Referer to NECIPSpider_wo_scrapy.py
 1. threadpool for NECIPSSpider_wo_scrapy.py
