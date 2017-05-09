from scrapy import cmdline
import sys
print(sys.path)

cmdline.execute(["scrapy","crawl","gsxt","-L","WARNING"])