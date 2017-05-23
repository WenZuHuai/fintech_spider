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
| Spiders/NECIPSSpider | [lxw](https://github.com/lxw0109) | Spiders for crawling data from [国家企业信用信息公示系统](http://www.gsxt.gov.cn/corp-query-homepage.html)(National Enterprise Credit Information Publicity System) |
| Spiders/NECIPSSpider_wo_scrapy.py | [lxw](https://github.com/lxw0109) | Spiders(w/o Scrapy) for crawling data from [国家企业信用信息公示系统](http://www.gsxt.gov.cn/corp-query-homepage.html)(National Enterprise Credit Information Publicity System) |
| Spiders/new_three_board | [lxw](https://github.com/lxw0109) | Spiders for crawling data from [全国中小企业股份转让系统](http://www.neeq.com.cn/nq/listedcompany.html) |


### TODO
**[He Chen](https://github.com/hee0624)**:
1. 在README.md中更新所提交的各个目录的用途(如果子目录中有关键的文件，也请列出)

**[Xiaowei Liu](https://github.com/lxw0109)**:
+ **CJOSpider**
 0. 代理的请求策略改成队列的形式,不要用random的形式
 1. 增加log
 2. 增加记录哪些案例应该爬取，哪些案例爬取过了，哪些没有爬取
    把所有要爬取的POST的data(Param,Index,Page)写入到log中; 把正确抓取到的POST的data也写入到log中。便于后期查看哪些data没有正确抓取到，以重新进行抓取
 3. 参考CJOAbbrFullSpider/CJOAllCompanySpider.py
    增加“当事人”字段case_parties(以股票代码code表示)
    增加“采用简称还是全称爬取”的标识字段abbr_full_category(abbr_single: 简称in全称; abbr: 使用简称; full: 使用全称)
    增加“爬取日期”字段crawl_date
+ **NECIPSSpider**
 0. add Referer to NECIPSpider_wo_scrapy.py
 1. threadpool for NECIPSSpider_wo_scrapy.py
