#1.定位目标
#2.进入子网页
#3.获取数据
import requests
import re

domain = "https://www.dytt8899.com/"
resp = requests.get(domain)#,verify=False将去掉安全验证
resp.encoding = "gb2312" 
resp.close()
#print(resp.text)
obj1 = re.compile(r"2025必看热片.*?<ul>(?P<ul>.*?)</ul>",re.S)
obj2 = re.compile(r"<a href='(?P<url>.*?)'",re.S)
obj3 = re.compile(
    r'◎片　　名　(?P<name>.*?)<br />.*?'
    r'<td style="WORD-WRAP: break-word" bgcolor="#fdfddf"><a href="(?P<download>.*?)">', 
    re.S
)
child_hrefs = []
result1 = obj1.finditer(resp.text)
#拿到位置
for it in result1:
    ul = it.group("ul")
    
    result2 = obj2.finditer(ul)
    for att in result2:
        #拿到子网页的链接并且进行拼接
        child_href = domain + att.group("url").strip('/')
        child_hrefs.append(child_href)
#提取子页面内容
for href in child_hrefs:
    child_resp = requests.get(href)
    child_resp.encoding = "gb2312"
    result3 = obj3.search(child_resp.text)
    print(result3.group("name"))
    print(result3.group("download"))
