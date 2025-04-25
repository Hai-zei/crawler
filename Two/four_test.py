import requests
import csv
from bs4 import BeautifulSoup
#拿到数据
#使用bs4进行解析
url = "http://hksclz.com/groceries/index"
resp = requests.post(url)
resp.close()
f = open("菜价.csv",mode ="w",encoding="utf-8")
csvwriter = csv.writer(f)
#解析数据
page = BeautifulSoup(resp.text,"html.parser")#指定html解析器
div = page.find("div",class_="box_out_form box_out_form2")
trs = div.find_all("tr")[1:]
for tr in trs:
    tds = tr.find_all("td")
    year = tds[0].text #.text表示被标记的内容
    name = tds[1].text #.text表示被标记的内容
    mony = tds[2].text #.text表示被标记的内容
    csvwriter.writerow([year, name, mony])
f.close()