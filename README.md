# fintech_spider
**_fintech(i.e. financial technology)_**

"**fintech_spider**" is a spider based on [Scrapy](https://scrapy.org/) to crawl a large number of financial data on the Internet.

The data crawled by "**fintech_spider**" has been used by [嗅金牛](http://xiujinniu.com/xiujinniu/index.php), [数知源](http://datazhiyuan.com/datazhiyuan/index.php).

### Structrue of fintech_spider

| Directory | Usage |
|------|------|
| Anti_Anti_Spider |  |
| CninfoSpider |  |
| demo | Some Demonstrations(e.g. PhantomJS/Proxies, etc.) |
| README.md | The document for this project |
| redis_IP_proxy | A rather naive IP Proxy pool based on Redis |
| Spiders | The Spiders directory to crawl data from the Internet(Crawling the data we want) |
| WenshuSpider |  |
| Spiders/NECIPSSpider | Spiders for crawling data from [国家企业信用信息公示系统](http://www.gsxt.gov.cn/corp-query-homepage.html): National Enterprise Credit Information Publicity System |


### TODO
[hee]: move the spiders into Spiders/ directory.

[lxw]: improve the policy to get the usable proxy.

