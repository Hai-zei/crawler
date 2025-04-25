#拿到页面源代码
#通过re提取信息
#正则解析式

import re
import requests
import csv

length = 50
start = 0
headers = {
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
}
results = []
while length > 0 :
    url = "https://movie.douban.com/top250?start={start}"
    resp = requests.get(url,headers=headers)
    page_content = resp.text
    obj = re.compile(r'<li>.*?<div class="item">.*?<span class="title">(?P<name>.*?)'
                 r'</span>.*?<p>.*?<br>(?P<year>.*?)&nbsp.*?' \
                 r'<span class="rating_num" property="v:average">(?P<score>.*?)</span>.*?' \
                 r'<span>(?P<num>.*?)人评价</span>',re.S)
#开始匹配
    result = obj.finditer(page_content)
    results.extend(result)
    resp.close()
    start += 25
    length -= 25

f = open("data.csv",mode = "w",encoding="utf-8",newline="")
csv_writer = csv.writer(f)

for it in results:
    dic = it.groupdict()
    dic['year'] = dic['year'].strip()
    csv_writer.writerow(dic.values())

f.close()
print("数据写入成功")
'''
    print(it.group("name"))
    print(it.group("score"))
    print(it.group("num"))
    print(it.group("year").strip())
'''