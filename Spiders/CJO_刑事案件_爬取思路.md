1. 抓取案件的概要信息(包括DocID)
http://wenshu.court.gov.cn/List/ListContent?MmEwMD=1ludmxrjoB4YuPbh570cnpZTOfM6dAf19m2fT0AjkKB3rSkan1uIC0GG0tcYJycJZsoCViUB6USu8gUZiSHik66RvDg2ajSnvuPILVLopaNTOMP7iFm24CxKM0G.kotRU.9ryhc0dWbSW09PfPeBya5Myom9Mr85dt74kLTggN2qafVpiuN.tdwuxe1YPo0rO5zzd6jtrwYETO08.QR4bIM5k68QoPRPpC0tsxmur04zMFiFBxIWJXjUaS8GgYaXXqIGpluooABmztqzkJvlfbJ6Hobwsy9JOtUiM.QnfwK0cqRaqTlNaGgJtg6FHytKTZGfXJFTmwjSmRXcmqYX5FG7Pqt81847ALxu_ehEd6Pzh2tOi4tafV49HhlkrLJtmtJ
MmEwMD=1UvtEFYItZBG5Sn5udG6dcLqXnHcnkTvNKSVgvlIim4zWPUmdrvj4v0YyRKGqjKgSqskRwkF_l2Ds.kxkPM4i9OzhWR1sWT2rT47DdMoWm.2MrgAvDem4K4rLj0zVRkk_bsPxBnkG5Coox6whZ5XHrenXE2Kwp4MILZt683MIIv3dgWUpHDwUMBdmMq5KNxGPm2zNARcSZf2D2Dlpz8cZYd2Bd59RrSuaigduwstHe7Q2mxOpm3IYVUpBHRwsWwWWlmhm0emHJNEbLbgOl6hOJkyN9DmRbXHTxBQQNsC4FTkpyyFoT6KlJ8eGblLCntfKcqEH_CjUu9NdHjqIYYc7voUYBeSIkbqqQr7VDzVQl0jW_OOtAosefHWHe.3prM9.62

POST
"Param": "案件类型:刑事案件",
"Index": 5,
"Page": 20,
"Order": "法院层级",
"Direction": "asc",
本来想通过构造这个URL来爬取(阅读Assets/js/Lawyee.CPWSW.List.js和Assets/js/Lawyee.CPWSW.ListLoad.js)，发现应该可以

通过直接访问"http://wenshu.court.gov.cn/List/ListContent"，然后增加

2. 针对每个案件的详细内容，需要得到当前案件的DocID然后通过http://wenshu.court.gov.cn/CreateContentJS/CreateContentJS.aspx?DocID=69f56346-9ac8-4361-bdd9-8a1a40918234获取网页的内容即可(GET)







Referer:http://wenshu.court.gov.cn/List/List?sorttype=1&conditions=searchWord+1+AJLX++%E6%A1%88%E4%BB%B6%E7%B1%BB%E5%9E%8B:%E5%88%91%E4%BA%8B%E6%A1%88%E4%BB%B6
