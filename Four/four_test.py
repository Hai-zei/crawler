import csv
import requests
from lxml import etree
from concurrent.futures import ThreadPoolExecutor

f = open("Four\data2.csv","a",encoding="utf-8",newline="")
csv_writer = csv.writer(f)
# 检查文件是否为空，只有在文件为空时写入表头
if f.tell() == 0:  # `f.tell()` 返回文件指针位置，0 表示文件为空
    csv_writer.writerow([" 名称 ", " 产地 ", " 供应商 ", " 抑制率1 ", " 抑制率2 ", " 结果 ", " 年份 "])
def download_one_page(url):
    resp = requests.get(url)
    resp.encoding = "utf-8"
    html = etree.HTML(resp.text)
    # xpath()默认返回列表
    table = html.xpath("/html/body/div[2]/div/div[2]/div[1]/div[2]/div/table[1]")[0]
    trs = table.xpath("./tbody/tr")[1:]
    for tr in trs:
        # 处理数据
        name  = tr.xpath("./td[2]/text()")
        place = tr.xpath("./td[3]/text()")
        vendor = tr.xpath("./td[4]/text()")
        asa1 = tr.xpath("./td[5]/text()")
        asa2 = tr.xpath("./td[6]/text()")
        answer = tr.xpath("./td[7]/text()")
        year = tr.xpath("./td[8]/text()")
        #存放在文件当中
        csv_writer.writerow([name[0],place[0],vendor[0],asa1[0],asa2[0],answer[0],year[0]])
    resp.close()
    print(f"{url}下载完成")
if __name__ == "__main__":
    # for i in range(1, 200):
    #     print(f"正在下载第{i}页")
    #     download_one_page(f"http://hksclz.com/groceries/report?page={i}")
    with ThreadPoolExecutor(50) as t:
        for i in range(1,201):
            print(f"正在下载第{i}页")
            t.submit(download_one_page, f"http://hksclz.com/groceries/report?page={i}")
    print("全部下载完成")
    f.close()