from scrapy import cmdline

# cmdline.execute(["scrapy", "crawl", "cninfo_company", "-L", "WARNING"])
cmdline.execute(["scrapy", "crawl", "annual_report", "-L", "WARNING"])