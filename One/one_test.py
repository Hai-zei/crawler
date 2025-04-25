#需求:用程序模拟浏览器，输入网站，从该网址获取网页内容

from urllib.request import urlopen

url = 'https://www.baidu.com/'
resp = urlopen(url)

# open()在windows上面默认是gbk编码，linux上面是utf-8编码0
with open("mybadu.html",mode="w",encoding = "utf-8") as f:
    f.write(resp.read().decode("utf-8"))
print("over!")

#服务器渲染：在服务器那边直接将数据和html整合在一起，同一返回给浏览器
#客户端渲染：第一次请求只得到一个html骨架，第二吃请求数据、进行数据展示
#熟练使用浏览器抓包工具
''''
import requests
query = input("请输入")
url = f'https://baike.baidu.com/item/{query}'

dic = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
}
#简单反爬虫机制

resp = requests.get(url,headers=dic)
print(resp.text)  # 打印网页内容
'''