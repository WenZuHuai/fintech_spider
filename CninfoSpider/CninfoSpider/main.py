from scrapy import cmdline

cmdline.execute(["scrapy", "crawl", "cninfo_company", "-L", "WARNING"])