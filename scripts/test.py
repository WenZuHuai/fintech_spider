#!/usr/bin/env python3
# coding: utf-8
# File: test.py
# Author: lxw
# Date: 5/26/17 12:14 PM

import json
import requests
import re
import time


def get_detail():
    url = "http://wenshu.court.gov.cn/CreateContentJS/CreateContentJS.aspx?DocID=26286a27-bdad-4142-9479-da759996ae0f"
    try:
        req = requests.get(url=url, timeout=120)
        text = req.text
        json_data = ""
        match_result = re.finditer(r"jsonHtmlData.*?jsonData", text, re.S)
        for m in match_result:
            data = m.group(0)
            right_index = data.rfind("}")
            left_index = data.find("{")
            json_data = data[left_index+1:right_index]
        return "\"{" + json_data + "}\""
    except Exception as e:
        print(e)
        return ""

json_data = get_detail()
print("json_data:", json_data)
exit(0)




print("--"*20, json_data)
text_str = json.loads(json_data)
text_dict = json.loads(text_str)
print(type(text_dict))  # dict
print(text_dict)



"""
 if text:
            index = text.index('{')  # $(function() {\r\n    var jsonHtmlData = "{\\"Title\\":...
            text = text[index + 1:]  # \r\n    var jsonHtmlData = "{\\"Title\\":...
            index = text.index('{')
            text = text[index + 1:]  # \\"Title\\":...

            index = text.index('}')  # ... </div>\\"}";\r\n    var jsonData...});
            text = text[:index]
            text = "\"{" + text + "}\""
            # print(text)
            # text_str = json.loads(text)
            # text_dict = json.loads(text_str)
        return text
"""