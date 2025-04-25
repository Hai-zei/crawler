#Beautifulsoup 解析式
import requests
import time
from bs4 import BeautifulSoup
import os

# 确保目录存在
if not os.path.exists("Two/img"):
    os.makedirs("Two/img")

headers = {
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
}
url = "https://www.bizhihui.com/yuzhou/"
resp = requests.get(url,headers=headers)
main_page = BeautifulSoup(resp.text,"html.parser")
#   只有是python关键字的才有下划线
alist = main_page.find("ul",id = "item-lists").find_all("a")

for a in alist:
    href = a.get('href')#直接通过get就可以拿到属性的值
    #获得子页面源代码
    child_page_resp = requests.get(href)
    child_page_text = child_page_resp.text
    child_page = BeautifulSoup(child_page_text,"html.parser")
    div = child_page.find("div",class_ = "article-pc")
    img = div.find("img")
    src = img.get("src")
    src = src.split("-arthumbs")[0]
    #下载图片
    img_resp = requests.get(src)
    img_name = src.split("/")[-1]#拿到最后一部分标记为名字
    with open ("img/"+img_name,mode = "wb") as f:
        f.write(img_resp.content)#内容（字节）
    print("over!",img_name)
    time.sleep(1)
    
print("all_over!")
resp.close()
