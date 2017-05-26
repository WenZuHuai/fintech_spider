#!/usr/bin/env python3
# coding: utf-8
# File: todo_iterator_test.py
# Author: lxw
# Date: 5/26/17 12:14 PM

import json
import requests
import re
import time


def get_detail(doc_id):
    url = "http://wenshu.court.gov.cn/CreateContentJS/CreateContentJS.aspx?DocID={0}".format(doc_id)
    try:
        req = requests.get(url=url, timeout=120)
        text = req.text
        # text = \
        """
        $(function() {
            var jsonHtmlData = "{\"Title\":\"孙丽娜与哈尔滨九洲电气股份有限公司劳动争议纠纷一案的民事裁定书\",\"PubDate\":\"2016-05-31\",\"Html\":\"<div style='LINE-HEIGHT: 25pt;TEXT-ALIGN:justify;TEXT-JUSTIFY:inter-ideograph; TEXT-INDENT: 30pt; MARGIN: 0.5pt 0cm;FONT-FAMILY: 仿宋; FONT-SIZE: 16pt;'><styletype=”text/css”></div><div style='LINE-HEIGHT: 25pt;TEXT-ALIGN:justify;TEXT-JUSTIFY:inter-ideograph; TEXT-INDENT: 30pt; MARGIN: 0.5pt 0cm;FONT-FAMILY: 仿宋; FONT-SIZE: 16pt;'>{C}<!--TABLE{border-collapse:collapse;border:none;mso-border-alt:solidblack.5pt;mso-yfti-tbllook:1184;mso-padding-alt:0cm5.4pt0cm5.4pt;mso-border-insideh:.5ptsolidblack;mso-border-insidev:.5ptsolidblack}TD{border:solidblack1.0pt;}--></style></div><a type='dir' name='WBSB'></a><div style='TEXT-ALIGN: center; LINE-HEIGHT: 25pt; MARGIN: 0.5pt 0cm; FONT-FAMILY: 宋体; FONT-SIZE: 22pt;'>黑龙江省高级人民法院</div><div style='TEXT-ALIGN: center; LINE-HEIGHT: 30pt; MARGIN: 0.5pt 0cm; FONT-FAMILY: 仿宋; FONT-SIZE: 26pt;'>民 事 裁 定 书</div><div style='TEXT-ALIGN: right; LINE-HEIGHT: 30pt; MARGIN: 0.5pt 0cm;  FONT-FAMILY: 仿宋;FONT-SIZE: 16pt; '>（2016）黑民申994号</div><a type='dir' name='DSRXX'></a><div style='LINE-HEIGHT: 25pt;TEXT-ALIGN:justify;TEXT-JUSTIFY:inter-ideograph; TEXT-INDENT: 30pt; MARGIN: 0.5pt 0cm;FONT-FAMILY: 仿宋; FONT-SIZE: 16pt;'>再审申请人（一审原告、二审上诉人）：孙丽娜。</div><div style='LINE-HEIGHT: 25pt;TEXT-ALIGN:justify;TEXT-JUSTIFY:inter-ideograph; TEXT-INDENT: 30pt; MARGIN: 0.5pt 0cm;FONT-FAMILY: 仿宋; FONT-SIZE: 16pt;'>委托代理人：何乃民，黑龙江贯通律师事务所律师。</div><div style='LINE-HEIGHT: 25pt;TEXT-ALIGN:justify;TEXT-JUSTIFY:inter-ideograph; TEXT-INDENT: 30pt; MARGIN: 0.5pt 0cm;FONT-FAMILY: 仿宋; FONT-SIZE: 16pt;'>被申请人（一审被告、二审被上诉人）：哈尔滨九洲电气股份有限公司。</div><div style='LINE-HEIGHT: 25pt;TEXT-ALIGN:justify;TEXT-JUSTIFY:inter-ideograph; TEXT-INDENT: 30pt; MARGIN: 0.5pt 0cm;FONT-FAMILY: 仿宋; FONT-SIZE: 16pt;'>法定代表人：李寅，该公司董事长。</div><div style='LINE-HEIGHT: 25pt;TEXT-ALIGN:justify;TEXT-JUSTIFY:inter-ideograph; TEXT-INDENT: 30pt; MARGIN: 0.5pt 0cm;FONT-FAMILY: 仿宋; FONT-SIZE: 16pt;'>委托代理人：周卓琦，该公司员工。</div><a type='dir' name='SSJL'></a><div style='LINE-HEIGHT: 25pt;TEXT-ALIGN:justify;TEXT-JUSTIFY:inter-ideograph; TEXT-INDENT: 30pt; MARGIN: 0.5pt 0cm;FONT-FAMILY: 仿宋; FONT-SIZE: 16pt;'>再审申请人孙丽娜因与被申请人哈尔滨九洲电气股份有限公司（以下简称九洲电气公司）劳动争议纠纷一案，不服哈尔滨市中级人民法院（2015）哈民一民终字第1130号民事判决，向本院申请再审。本院依法组成合议庭对本案进行了审查，现已审查终结。</div><a type='dir' name='AJJBQK'></a><div style='LINE-HEIGHT: 25pt;TEXT-ALIGN:justify;TEXT-JUSTIFY:inter-ideograph; TEXT-INDENT: 30pt; MARGIN: 0.5pt 0cm;FONT-FAMILY: 仿宋; FONT-SIZE: 16pt;'>孙丽娜申请再审称：（一）九洲电气公司已建立了工会组织，但九洲电气公司与其解除劳动关系时并未通知工会，九洲电气公司的行为违反了《中华人民共和国劳动合同法》第四十三条及《中华人民共和国工会法》第二十一条的规定，属于违法解除劳动关系，应当支付其赔偿金20042.1元。（二）其提交的证据证明九洲电气公司欠业务费5万元，九洲电气公司应予给付。依据《中华人民共和国民事诉讼法》第二百条第六项之规定申请再审。</div><a type='dir' name='CPYZ'></a><div style='LINE-HEIGHT: 25pt;TEXT-ALIGN:justify;TEXT-JUSTIFY:inter-ideograph; TEXT-INDENT: 30pt; MARGIN: 0.5pt 0cm;FONT-FAMILY: 仿宋; FONT-SIZE: 16pt;'>本院认为：《中华人民共和国劳动合同法》第四十三条规定：”用人单位单方解除劳动合同，应当事先将理由通知工会。用人单位违反法律、行政法规规定或者劳动合同约定的，工会有权要求用人单位纠正。用人单位应当研究工会的意见，并将处理结果书面通知工会。”《中华人民共和国工会法》第二十一条规定：”各级工会应当建立劳动法律监督组织，设立工会劳动法律监督员，对企业贯彻实施劳动法律、法规的情况进行监督。企业违反劳动法律、法规的，工会劳动法律监督员应当以书面形式提出意见和建议，拒不改正的，可以呈请人力资源社会保障部门依法作出处理。工会应当依法配合有关部门做好劳动法律、法规的监督检查工作。”九洲电气公司与孙丽娜签订的劳动合同书第二十五条第7项约定，乙方（孙丽娜）有无故连续旷工15天或全年累计旷工30天，或甲方（九洲电气公司）未批准其续假申请超过15天的......，甲方均可以与乙方解除劳动关系和保险关系。2013年8月20日，九洲电气公司通知孙丽娜回公司报道并给其调整工作岗位，孙丽娜以催收尾款为由未到九洲电气公司报到。因孙丽娜无证据证实其为九洲电气公司催款，亦未举示证据证明其向九洲电气公司请假，九洲电气公司以连续旷工为由解除与孙丽娜劳动关系的行为未违反双方劳动合同的约定，原判决并无不当。孙丽娜在一审中举示了两份《特殊费用（特殊业务费、返款、代理费）借款审批单》及《说明》。因上述证据形式载明的内容系孙丽娜向九洲电气公司借款，该证据不能充分证实孙丽娜的再审主张，原判决未予支持亦无不当，孙丽娜的再审事由不能成立。</div><div style='LINE-HEIGHT: 25pt;TEXT-ALIGN:justify;TEXT-JUSTIFY:inter-ideograph; TEXT-INDENT: 30pt; MARGIN: 0.5pt 0cm;FONT-FAMILY: 仿宋; FONT-SIZE: 16pt;'>综上，孙丽娜的再审申请不符合《中华人民共和国民事诉讼法》第二百条第六项规定的情形。依照《中华人民共和国民事诉讼法》第二百零四条第一款之规定，裁定如下：</div><a type='dir' name='PJJG'></a><div style='LINE-HEIGHT: 25pt;TEXT-ALIGN:justify;TEXT-JUSTIFY:inter-ideograph; TEXT-INDENT: 30pt; MARGIN: 0.5pt 0cm;FONT-FAMILY: 仿宋; FONT-SIZE: 16pt;'>驳回孙丽娜的再审申请。</div><a type='dir' name='WBWB'></a><div style='TEXT-ALIGN: right; LINE-HEIGHT: 25pt; MARGIN: 0.5pt 72pt 0.5pt 0cm;FONT-FAMILY: 仿宋; FONT-SIZE: 16pt;'>审　判　长　　刘东兴</div><div style='TEXT-ALIGN: right; LINE-HEIGHT: 25pt; MARGIN: 0.5pt 72pt 0.5pt 0cm;FONT-FAMILY: 仿宋; FONT-SIZE: 16pt;'>代理审判员　　陈春雷</div><div style='TEXT-ALIGN: right; LINE-HEIGHT: 25pt; MARGIN: 0.5pt 72pt 0.5pt 0cm;FONT-FAMILY: 仿宋; FONT-SIZE: 16pt;'>代理审判员　　赵洪波</div><br/><div style='TEXT-ALIGN: right; LINE-HEIGHT: 25pt; MARGIN: 0.5pt 72pt 0.5pt 0cm;FONT-FAMILY: 仿宋; FONT-SIZE: 16pt;'>二〇一六年五月二十六日</div><div style='TEXT-ALIGN: right; LINE-HEIGHT: 25pt; MARGIN: 0.5pt 72pt 0.5pt 0cm;FONT-FAMILY: 仿宋; FONT-SIZE: 16pt;'>书　记　员　　董国策</div>\"}";
            var jsonData = eval("(" + jsonHtmlData + ")");
            $("#contentTitle").html(jsonData.Title);
            $("#tdFBRQ").html("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;发布日期：" + jsonData.PubDate);
            var jsonHtml = jsonData.Html.replace(/01lydyh01/g, "\'");
            $("#DivContent").html(jsonHtml);
        
            //初始化全文插件
            Content.Content.InitPlugins();
            //全文关键字标红
            Content.Content.KeyWordMarkRed();
        });
        """

        """
        TODO: NOTE: run的时候能够匹配到所有的符合条件的字符串; debug的时候,并且断点加到for循环体内,则只能匹配到第一个[导致这一现象的原因需要进一步查阅]
        iterator使用心得:
        1. iterator对象只能使用一次,使用多次,就会导致没有数据可用
        2. 循环iterator对象(for item in iterator_object)时, 把断点加到循环体内部会导致iterator对象只能取到第一个数据(这个是pycharm的问题?还是所有的iterator额问题,待进一步测试)
        """
        json_data = ""
        match_result = re.finditer(r"jsonHtmlData.*?jsonData", text, re.S)

        for m in match_result:
            print("in for cyclic body")
            data = m.group(0)
            right_index = data.rfind("}")
            left_index = data.find("{")
            json_data = data[left_index+1:right_index]
            break   # this is essential. Only the first match is what we want.
        return "\"{" + json_data + "}\""
    except Exception as e:
        print(e)
        return ""

doc_id = "26286a27-bdad-4142-9479-da759996ae0f"
json_data = get_detail(doc_id)
print("json_data:", json_data)

text_str = json.loads(json_data)
text_dict = json.loads(text_str)
print(type(text_dict))  # dict
print(text_dict)
