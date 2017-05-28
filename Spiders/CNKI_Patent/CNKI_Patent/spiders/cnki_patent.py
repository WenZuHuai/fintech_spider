#!/usr/bin/env python3
# coding: utf-8
# File: test.py
# Author: lxw
# Date: 5/26/17 4:03 PM

import scrapy
import time


class CnkiPatentSpider(scrapy.Spider):
    name = "cnki_patent"
    current_time = int(time.time() * 1000)
    # url = 'http://www.cnki.net/'
    # url = "http://www.ip138.com/ua.asp"    # 查看当前请求的User-Agent和所使用的IP
    # url = "http://xiujinniu.com/xiujinniu/index.php"
    # url = "http://kns.cnki.net/kns/brief/brief.aspx?pagename=ASP.brief_default_result_aspx&dbPrefix=SCOD&dbCatalog=%e4%b8%ad%e5%9b%bd%e5%ad%a6%e6%9c%af%e6%96%87%e7%8c%ae%e7%bd%91%e7%bb%9c%e5%87%ba%e7%89%88%e6%80%bb%e5%ba%93&ConfigFile=SCDBINDEX.xml&research=off&t={0}&keyValue=%E5%B9%B3%E5%AE%89%E9%93%B6%E8%A1%8C%E8%82%A1%E4%BB%BD%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8&S=1".format(current_time)
    # url = "http://kns.cnki.net/kns/brief/default_result.aspx"   # No
    url = "http://kns.cnki.net/kns/brief/brief.aspx?pagename=ASP.brief_default_result_aspx&dbPrefix=SCOD&dbCatalog=%e4%b8%ad%e5%9b%bd%e5%ad%a6%e6%9c%af%e6%96%87%e7%8c%ae%e7%bd%91%e7%bb%9c%e5%87%ba%e7%89%88%e6%80%bb%e5%ba%93&ConfigFile=SCDBINDEX.xml&research=off&t={0}&keyValue=%E5%B9%B3%E5%AE%89%E9%93%B6%E8%A1%8C%E8%82%A1%E4%BB%BD%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8&S=1".format(current_time)

    def start_requests(self):
        """         
        post_data = {
            "Param": param,
            "Index": repr(index),
            "Page": repr(self.cases_per_page),
            "Order": "法院层级",
            "Direction": "asc",
        }

        yield scrapy.FormRequest(url=self.url, formdata=post_data, callback=lambda response: self.parse(response, data))
        
        
        pagename:ASP.brief_default_result_aspx
        dbPrefix:SCOD
        dbCatalog:中国学术文献网络出版总库
        ConfigFile:SCDBINDEX.xml
        research:off
        t:1495859089275
        keyValue:平安银行股份有限公司
        S:1
        """
        headers = {
            "Connection": "Keep-Alive",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Host": "kns.cnki.net",
            "Referer": "http://kns.cnki.net/kns/brief/default_result.aspx",
        }
        post_data = {
            "pagename": "ASP.brief_default_result_aspx",
            "dbPrefix": "SCOD",
            "dbCatalog": "中国学术文献网络出版总库",
            "ConfigFile": "SCDBINDEX.xml",
            "research": "off",
            "t": repr(self.current_time),
            "keyValue": "平安银行股份有限公司",
            "S": "1"
        }

        # 通过selenium获取的cookie. 参见test/get_cnki_cookie_by_selenium.py
        cookies = {'SID_klogin': '125143', 'Ecp_LoginStuts': '{"IsAutoLogin":false,"UserName":"zky311060","ShowName":"%e4%b8%ad%e5%9b%bd%e7%a7%91%e5%ad%a6%e9%99%a2%e8%bd%af%e4%bb%b6%e7%a0%94%e7%a9%b6%e6%89%80","UserType":"bk","r":"3eFaYv"}', 'c_m_expire': '2017-05-27 16:03:20', 'c_m_LinID': 'LinID=WEEvREcwSlJHSldRa1FhdXNXYXJwZC9ZcG03TlNHejBXSVh2Z2s2N29yTT0=$9A4hF_YAuvQ5obgVAqNKPCYcEjKensW4ggI8Fm4gTkoUKaID8j8gFw!!&ot=05/27/2017 16:03:20', 'LID': 'WEEvREcwSlJHSldRa1FhdXNXYXJwZC9ZcG03TlNHejBXSVh2Z2s2N29yTT0=$9A4hF_YAuvQ5obgVAqNKPCYcEjKensW4ggI8Fm4gTkoUKaID8j8gFw!!', 'SID_kns': '123116', 'Ecp_ClientId': '5170527153401539983', 'ASP.NET_SessionId': 'ztf4mga35r3foj43hd0n2xto'}

        yield scrapy.Request(url=self.url, callback=self.parse, method="GET", headers=headers, cookies=cookies)
        # yield scrapy.FormRequest(url=self.url, callback=self.parse, headers=headers, formdata=post_data, method="GET")


    def parse(self, response):
        print(response.text)

    def check_user_agent_proxy(self, response):
        tbody_list = response.xpath('//table')
        print(type(tbody_list), tbody_list)
        # [2]
        trs = tbody_list[2]
        td_list = trs.xpath('./tr/td')
        for td in td_list:
            print(td.xpath("string(.)").extract_first().replace("\n", " ").replace("  ", ""))

    """
    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
    <HTML>
    <HEAD>
    <meta http-equiv="Content-Type" content="text/html; charset=gb2312">
    <meta http-equiv="mobile-agent" content="format=html5; url=http://m.ip138.com/ip.html"/>
    <TITLE>UserAgent查询 --IP地址查询 | 手机号码查询归属地 | 邮政编码查询 | 长途电话区号 | 身份证号码验证在线查询网</TITLE>
    <META NAME="Generator" CONTENT="UA,UserAgent查询,ip138,网址之家">
    <META NAME="Author" CONTENT="ip138,网址之家">
    <META NAME="Keywords" CONTENT="UA,UserAgent查询,ip138,网址之家">
    <META NAME="Description" CONTENT="UA,UserAgent查询,IP地址查询,ip138,网址之家">
    <STYLE type="text/css">
    p,td {font-size:16px}
    A:link {
        COLOR: #1c5f82; TEXT-DECORATION: none
    }
    A:visited {
        COLOR: #1c5f82; TEXT-DECORATION: none
    }
    A:hover {
        COLOR: #cc5533; TEXT-DECORATION: underline
    }
    A.green:link {COLOR: #008000;}
    A.green:visited {COLOR: #008000;}
    A.green:hover {COLOR: #008000;}
    
    BODY {
        SCROLLBAR-HIGHLIGHT-COLOR: #f7f7f7; SCROLLBAR-SHADOW-COLOR: #f7f7f7; SCROLLBAR-ARROW-COLOR: #EFF1F3; SCROLLBAR-TRACK-COLOR: #EFF1F3; SCROLLBAR-BASE-COLOR: #f7f7f7
    }
    .ul1{
        width:400px;
        text-align:left;
    }
    li{
        color:green;
        }
    </STYLE>
    </HEAD>
    <BODY>
    <div align="center"><center>
    <table cellSpacing="0" cellPadding="0" width="760" align="center" border="0">
        <tr vAlign="bottom">
            <td align="left"><a href="http://www.ip138.com"><b>www.ip138.com 查询网</b></a></td>
            <td align="middle"></td>
            <td align="right"><strong>手机上网查询:wap.ip138.com</strong></td>
        </tr>
        <tr vAlign="top" align="left">
            <td colSpan="3"><hr width="100%" SIZE="1">
            </td>
        </tr>
    </table>
    </center></div>
    
    <div align="center"><center>
    <table height="22" cellSpacing="0" cellPadding="0" width="710" border="0">
        <tr align="middle">
            <td width="179"><b><font color="#008000">→</font></b><a href="http://www.ip138.com/ips1388.asp" target="_blank">ip地址所在地查询</a></td>
            <td width="177"><b><font color="#008000">→</font></b><a href="http://qq.ip138.com/train/" target="_blank">国内列车时刻表查询</a></td>
            <td width="177"><b><font color="#008000">→</font></b><a href="http://www.ip138.com/sj/" target="_blank">手机号码所在地区查询</a></td>
            <td width="177"><b><font color="#008000">→</font></b><a href="http://qq.ip138.com/weather/" target="_blank">天气预报-预报五天</a></td>
        </tr>
        <tr align="middle">
            <td><b><font color="#008000">→</font></b><a href="http://www.ip138.com/gb.htm" target="_blank">汉字简体繁体转换</a></td>
            <td><b><font color="#008000">→</font></b><a href="http://www.ip138.com/jb.htm" target="_blank">国内国际机票查询</a></td>
            <td><b><font color="#008000">→</font></b><a href="http://10.ip138.com/" target="_blank">品牌排行榜</a></td>
            <td><b><font color="#008000">→</font></b><a href="http://qq.ip138.com/wb/wb.asp" target="_blank">五笔编码拼音查询</a></td>
        </tr>
        <tr align="middle">
            <td><b><font color="#008000">→</font></b><a href="http://qq.ip138.com/tran.htm" target="_blank">在线翻译</a></td>
            <td><b><font color="#008000">→</font></b><a href="http://qq.ip138.com/hl.asp" target="_blank">货币汇率兑换</a></td>
            <td><b><font color="#008000">→</font></b><a href="http://qq.ip138.com/day/" target="_blank">阴阳转换万年历</a></td>
            <td><b><font color="#008000">→</font></b><a href="http://www.ip138.com/post/" target="_blank">邮编查询区号查询</a></td>
        </tr>
        <tr align="middle">
            <td><a href="http://qq.ip138.com/idsearch/" target="_blank">身份证号码查询验证</a></td>
            <td><a href="http://www.ip138.com/ems/" target="_blank">快递查询</a> <a href="http://www.ip138.com/ems/" target="_blank">EMS查询</a></td>
            <td><a href="http://www.ip138.com/carlist.htm" target="_blank">全国各地车牌查询表</a></td>
            <td><a href="http://www.ip138.com/weizhang.htm" target="_blank">车辆交通违章查询</a></td>
        </tr>
    </table>
    </center></div>
    <br/>
    <table width="760"  border="0" align="center" cellpadding="0" cellspacing="0">
        <tr>
            <td align="center"><h3>ip138.com UA查询(显示用户UserAgent)</h3></td>
        </tr>
        <tr>
            <td align="left" height="20">您请求CDN的IP是：[171.13.73.220] 河南省平顶山市 电信</td>
        </tr>
        </tr>
        <tr>
            <td align="left" height="20">客户端IP（REMOTE_ADDR）：[111.178.234.52] 湖北省黄石市 电信</td>
        </tr>
        </tr>
        <tr>
            <td align="left" height="20">代理IP列表是（HTTP_VIA）：[] </td>
        </tr>
        </tr>
        <tr>
            <td align="left" height="20">代理用户的真实IP（HTTP_X_FORWARDED_FOR）：[] </td>
        </tr>
        <tr>
            <td align="left">服务端获取的Useragent：Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)</td>
        </tr>
        <tr>
            <td align="left">客户端获取的Useragent：<script type="text/javascript">
            <!--
                document.write(navigator.userAgent)
            //-->
            </script></td>
        </tr>
        <tr>
            <td align="center">
    <br/>
    <p align="center">
    <div align="center">
    <script type="text/javascript">
    var cpro_id = "u2962614";
    </script>
    <script type="text/javascript" src="http://cpro.baidustatic.com/cpro/ui/c.js"></script>
    </div>
    </p></td>
        </tr>
    </table>
    <p align="center">
    <div align="center">
    <script type="text/javascript">
    var cpro_id = "u2962622";
    </script>
    <script type="text/javascript" src="http://cpro.baidustatic.com/cpro/ui/c.js"></script>
    </div>
    </p>
    <p align="center">如发现小部分ip查询结果不正确请到官方网站<a
    href="http://www.apnic.net" rel="nofollow" target="_blank">http://www.apnic.net</a>查询,以apnic为准</p>
    <p align="center"></a>联系我们.请<a href="mail.htm" rel="nofollow" target="_blank">发email</a>.或给<a
    href="http://qq.3533.com:8080/book.asp?siteid=7" rel="nofollow" target="_blank">我们留言</a>谢谢!</p>
    <p align="center">沪ICP备10013467号-1号</p>
    <div style="display:none"><script type="text/javascript" src="http://tajs.qq.com/stats?sId=36241650" charset="UTF-8"></script></div>
    </body>
    </html>
    """