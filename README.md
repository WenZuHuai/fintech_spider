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
| Spiders/CJOSpider | [lxw](https://github.com/lxw0109) | Spiders for crawling data from [中国裁判文书网](http://wenshu.court.gov.cn/)(China Judgements Online) |
| Spiders/CninfoSpider | [hee](https://github.com/hee0624) | Spiders for crawling data from [巨潮资讯](http://www.cninfo.com.cn/cninfo-new/information/companylist) |
| Spiders/NECIPSSpider | [lxw](https://github.com/lxw0109) | Spiders for crawling data from [国家企业信用信息公示系统](http://www.gsxt.gov.cn/corp-query-homepage.html)(National Enterprise Credit Information Publicity System) |
| Spiders/new_three_board | [lxw](https://github.com/lxw0109) | Spiders for crawling data from [全国中小企业股份转让系统](http://www.neeq.com.cn/nq/listedcompany.html) |
| Spiders/NECIPSSpider_wo_scrapy.py | [lxw](https://github.com/lxw0109) | Spiders(w/o Scrapy) for crawling data from [国家企业信用信息公示系统](http://www.gsxt.gov.cn/corp-query-homepage.html)(National Enterprise Credit Information Publicity System) |



### TODOs
[He Chen](https://github.com/hee0624):
1.

[Xiaowei Liu](https://github.com/lxw0109):
0. add referer to NECIPSpider_wo_scrapy.py
1. improve the policy to get the usable proxy
the free proxy is much too unstable and slow.
2. threadpool for NECIPSSpider_wo_scrapy.py
