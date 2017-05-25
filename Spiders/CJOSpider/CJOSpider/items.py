# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CjospiderItem(scrapy.Item):
    # define the fields for your item here like:
    """
    {
    '裁判要旨段原文': '本院认为：被告党旭向在此纠纷中，只起了介绍人的作用，不应承担责任。被告建设三矿售给原告褚海英的石棉确属不合格，但原告褚海英知道卖主为建设三矿，在石棉检验结果出来后，在未与卖方取得一致意见情况下，即单方将石棉出售，应视为其接受石棉质量。依照《中华人民共和国民事诉讼法》第140条之规定，判决如下',
    '不公开理由': '',
    '案件类型': '2',
    '裁判日期': '1996-01-10',
    '案件名称': '褚海英与党旭向石棉买卖纠纷一审民事判决书',
    '文书ID': '7befa561-ecac-4d91-b3fe-a71a0096c3fb',
    '审判程序': '一审',
    '案号': $（1996）阿民初字第16号',
    '法院名称': '阿克塞哈萨克族自治县人民法院',
    'case_details': '"{\\"Title\\":\$
"褚海英与党旭向石棉买卖纠纷一审民事判决书\\",
    \\"PubDate\\": \\"2017-02-23\\",
    \\"Html\\": \\"<atype=\'d$r\'name=\'WBSB\'></a><divstyle=\'TEXT-ALIGN: center;LINE-HEIGHT: 25pt;MARGIN: 0.5pt0cm;F[
        47/242$LY: 宋体;FONT-SIZE: 22pt;\'>甘肃省阿克塞哈萨克族自治县人民法院</div><divstyle=\'TEXT-ALIGN: center;LINE-HEIGHT: 30pt;MARGIN: 0.5pt0cm;FONT-FAMILY: 仿宋;FONT-SIZE: 26pt;\'>民事判决书</div><divstyle=\'TEXT-ALIGN: right;LINE-HEIGHT: 30pt;MARGIN: 0.5pt0cm;FONT-FAMILY: 仿宋;FONT-SIZE: 16pt;\'>（1996）阿民初字第16号</div><atype=\'dir\'name=\'DSRXX\'></a><divstyle=\'LINE-HEIGHT: 25pt;TEXT-ALIGN: justify;TEXT-JUSTIFY: inter-ideograph;TEXT-INDENT: 30pt;MARGIN: 0.5pt0cm;FONT-FAMILY: 仿宋;FONT-SIZE: 16pt;\'>原告：褚海英，男。</div><divstyle=\'LINE-HEIGHT: 25pt;TEXT-ALIGN: justify;TEXT-JUSTIFY: inter-ideograph;TEXT-INDENT: 30pt;MARGIN: 0.5pt0cm;FONT-FAMILY: 仿宋;FONT-SIZE: 16pt;\'>委托代理人：王作周，敦煌市律师事务所律师。</div><divstyle=\'LINE-HEIGHT: 25pt;TEXT-ALIGN: justify;TEXT-JUSTIFY: inter-ideograph;TEXT-INDENT: 30pt;MARGIN: 0.5pt0cm;FONT-FAMILY: 仿宋;FONT-SIZE: 16pt;\'>被告：党旭向，男。</div><divstyle=\'LINE-HEIGHT: 25pt;TEXT-ALIGN: justify;TEXT-JUSTIFY: inter-ideograph;TEXT-INDENT: 30pt;MARGIN: 0.5pt0cm;FONT-FAMILY: 仿宋;FONT-SIZE: 16pt;\'>被告；阿克塞县建设乡第三石棉矿（以下简称建设三矿）。</div><divstyle=\'LINE-HEIGHT: 25pt;TEXT-ALIGN: justify;TEXT-JUSTIFY: inter-ideograph;TEXT-INDENT: 30pt;MARGIN: 0.5pt0cm;FONT-FAMILY: 仿宋;FONT-SIZE: 16pt;\'>法定代表人：常松柏，矿长。</div><atype=\'dir\'name=\'SSJL\'></a><divstyle=\'LINE-HEIGHT: 25pt;TEXT-ALIGN: justify;TEXT-JUSTIFY: inter-ideograph;TEXT-INDENT: 30pt;MARGIN: 0.5pt0cm;FONT-FAMILY: 仿宋;FONT-SIZE: 16pt;\'>原告褚海英诉被告党旭向石棉买卖纠纷一案，本院受理后，追加建设三矿为共同被告，依法组成合议庭，公开开庭进行了审理。原告及诉讼代理人，二被告均到庭参加了诉讼。本案现已审理终结。</div><divstyle=\'LINE-HEIGHT: 25pt;TEXT-ALIGN: justify;TEXT-JUSTIFY: inter-ideograph;TEXT-INDENT: 30pt;MARGIN: 0.5pt0cm;FONT-FAMILY: 仿宋;FONT-SIZE: 16pt;\'>原告褚海英诉称：我所在工商所职工集资2万元通过被告党旭向，于1993年9月12日以每吨1800元的价格购买4-10级石棉11吨。石棉拉至敦煌，经化验，质量达不到事先约定标准，因而多付货款11200元。现起诉法院，要求被告党旭向返还多付货款。</div><divstyle=\'LINE-HEIGHT: 25pt;TEXT-ALIGN: justify;TEXT-JUSTIFY: inter-ideograph;TEXT-INDENT: 30pt;MARGIN: 0.5pt0cm;FONT-FAMILY: 仿宋;FONT-SIZE: 16pt;\'>被告党旭向辩称：原告所买石棉是通过我介绍购买建设三矿的，我未得任何利益，原告诉我无理。且本案已超过诉讼时效。</div><divstyle=\'LINE-HEIGHT: 25pt;TEXT-ALIGN: justify;TEXT-JUSTIFY: inter-ideograph;TEXT-INDENT: 30pt;MARGIN: 0.5pt0cm;FONT-FAMILY: 仿宋;FONT-SIZE: 16pt;\'>被告建设三矿辩称：我方经党旭向介绍卖给原告褚海英的11吨石棉是主机棉，而在敦煌化验的石棉是6一40级的下角料，证明所化验石棉不是从我矿拉的。况且我与原告事先也未约定购买的石棉为4-10级。</div><divstyle=\'LINE-HEIGHT: 25pt;TEXT-ALIGN: justify;TEXT-JUSTIFY: inter-ideograph;TEXT-INDENT: 30pt;MARGIN: 0.5pt0cm;FONT-FAMILY: 仿宋;FONT-SIZE: 16pt;\'>经审理查明：1993年9月初，原告褚海英所在工商所职工集资2万元，交由褚海英贩卖石棉。原告褚海英向被告党旭向联系石棉，党旭向答应为其找卖主。后被告党旭向找到被告建设三矿矿长常松柏联系石棉，常松柏同意出售石棉。1993年9月12日，原告褚海英委托本所职工牛西龙及李万寿携带现金2万元，随车到阿克塞县红柳沟石棉矿拉运石棉。车到阿克塞20公里岔路口，牛西龙将现金交给党旭向，党旭向将现金以被告建设三矿矿长常松柏的姓名存入阿克塞县工商银行二十公里分理处，后随车上山。在阿克塞县红柳沟石棉矿党旭向等人找到常松柏，党旭向将双方作了介绍，常松柏与拉棉按商定以矿山价格每吨1800元拉运11吨4级棉。晚12时，车装好后，常松柏、党旭向随车下山，回到县城，党旭向将存单交给常松柏，由常松柏之妻崔爱琴打下收条。牛西龙、李万寿于13日早将棉拉至敦煌后，请懂行的王志杰看验石棉。发现石棉质量存在问题，原告即打电话告诉党旭向，并将石棉卸至敦煌硫化碱厂院内。9月14日，原告用车将党旭向及常松柏拉到卸棉地点，并委托敦煌矿产品公司化验石棉。经化验，石棉级别为6一40级，常松柏以化验石棉不是其矿所产为由，拒绝在化验单上签名，党旭向、褚海英在化验单上签了名。石棉放置半年后，原告褚海英将其出售。后原告褚海英与孙绪明因债务纠纷一案引起纷争，原告起诉法院，要求被告党旭向偿付售出的此车石棉的质量差价。</div><divstyle=\'LINE-HEIGHT: 25pt;TEXT-ALIGN: justify;TEXT-JUSTIFY: inter-ideograph;TEXT-INDENT: 30pt;MARGIN: 0.5pt0cm;FONT-FAMILY: 仿宋;FONT-SIZE: 16pt;\'>本院确认的上述事实，有原、被告双方的陈述，证人牛西龙、苏小虎的证言，银行存款存单及崔爱琴写的收条，敦煌市矿产品公司化验室化验单等证据在案为凭。</div><atype=\'dir\'name=\'CPYZ\'></a><divstyle=\'LINE-HEIGHT: 25pt;TEXT-ALIGN: justify;TEXT-JUST$FY: inter-ideograph;TEXT-INDENT: 30pt;MARGIN: 0.5pt0cm;FONT-FAMILY: 仿宋;FONT-SIZE: 16pt;\'>本院认为：被告党旭向在此纠纷中，只起了介绍人的作用，不应承担责任。被告建设三矿售给原告褚海英的石棉确属不合格，但原告褚海英知道卖主为建设三矿，在石棉检验结果出来后，在未与卖方取得一致意见情况下，即单方将石棉出售，应视为其接受石棉质量。依照《中华人民共和国民事诉讼法》第140条之规定，判决如下：</div><atype=\'dir\$name=\'PJJG\'></a><divstyle=\'LINE-HEIGHT: 25pt;TEXT-ALIGN: justify;TEXT-JUSTIFY: inter-ideograph;TE$T-INDENT: 30pt;MARGIN: 0.5pt0cm;FONT-FAMILY: 仿宋;FONT-SIZE: 16pt;\'>一、驳回原告褚海英的诉讼请求。</div><divstyle=\'LINE-HEIGHT: 25pt;TEXT-ALIGN: justify;TEXT-JUSTIFY: inter-ideograph;TEXT-INDENT: 30$t;MARGIN: 0.5pt0cm;FONT-FAMILY: 仿宋;FONT-SIZE: 16pt;\'>二、案件受理费400元，其他诉讼费用200元，由原告承担。</div><divstyle=\'LINE-HEIGHT: 25pt;TEXT-ALIGN: justify;TEXT-JUSTIFY: inter-ideograph;TEXT-$NDENT: 30pt;MARGIN: 0.5pt0cm;FONT-FAMILY: 仿宋;FONT-SIZE: 16pt;\'>如不服本判决，可在接到判决书的第$日起15日内，向本院递交上诉状正本1份、副本3份，上诉于甘肃省酒泉地区中级人民法院。</div><atype=\'dir\'name=\'WBWB\'></a><divstyle=\'TEXT-ALIGN: right;LINE-HEIGHT: 25pt;MARGIN: 0.5pt72pt0.5pt0cm;FON$-FAMILY: 仿宋;FONT-SIZE: 16pt;\'>审判长\u3000申国勤</div><divstyle=\'TEXT-ALIGN: right;LINE-HEIG$T: 25pt;MARGIN: 0.5pt72pt0.5pt0cm;FONT-FAMILY: 仿宋;FONT-SIZE: 16pt;\'>审判员\u3000康秀琴</div$<divstyle=\'TEXT-ALIGN: right;LINE-HEIGHT: 25pt;MARGIN: 0.5pt72pt0.5pt0cm;FONT-FAMILY: 仿宋;FO$T-SIZE: 16pt;\'>审判员\u3000段晓明</div><br/><divstyle=\'TEXT-ALIGN: right;LINE-HEIGHT: 25pt;MAR$IN: 0.5pt72pt0.5pt0cm;FONT-FAMILY: 仿宋;FONT-SIZE: 16pt;\'>一九九六年一月十日</div><divstyle=\'T$XT-ALIGN: right;LINE-HEIGHT: 25pt;MARGIN: 0.5pt72pt0.5pt0cm;FONT-FAMILY: 仿宋;FONT-SIZE: 16pt;\$>书记员\u3000阿尔斯坦</div>\\"
    }"'}
    """
    abstract = scrapy.Field()   # 1.裁判要旨段原文
    reason_not_public = scrapy.Field()  # 2.不公开理由
    case_category = scrapy.Field()  # 3.案件类型
    judge_date = scrapy.Field() # 4.裁判日期
    case_name = scrapy.Field()  # 5.案件名称
    doc_id = scrapy.Field() # 6.文书ID
    judge_procedure = scrapy.Field()    # 7.审判程序
    case_num = scrapy.Field()   # 8.案号
    court_name = scrapy.Field() # 9.法院名称
    case_details = scrapy.Field()   # 10.案件详细内容
    case_parties = scrapy.Field()   # 11.当事人
    abbr_full_category = scrapy.Field() # 12.采用简称还是全称爬取 (标识字段)
    crawl_date = scrapy.Field()     # 13.爬取日期


