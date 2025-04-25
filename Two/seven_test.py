import requests
from lxml import etree
url = "https://hai-zei.github.io/"
resp = requests.get(url)
#print(resp.text)
html = etree.HTML(resp.text)
#所有项目
divs = html.xpath("/html/body/div[1]/section[2]/div[1]/div")
for div in divs:
    html_text = div.xpath("./p/text()")[0]
    html_href = div.xpath("./a/@href")[0]
    print(html_text)
    print(html_href)

resp.close()