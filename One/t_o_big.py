import requests

length = eval(input("请输入你要爬取的网页长度："))
start = 0
limit = 20
url = "https://movie.douban.com/j/chart/top_list"
all_data = [] #存放所有数据
# 定义键名的中英文映射
key_mapping = {
    "rating": "评分",
    "rank": "排名",
    "cover_url": "封面链接",
    "is_playable": "是否可播放",
    "id": "电影ID",
    "types": "类型",
    "regions": "地区",
    "title": "标题",
    "url": "详情链接",
    "release_date": "上映日期",
    "actor_count": "演员数量",
    "vote_count": "投票数量",
    "score": "评分",
    "actors": "演员"
}

while length > 0:
    param = {
    "type": "24",
    "interval_id": "100:90",
    "action": "",
    "start": start,
    "limit": limit
    }
    headers = {
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
    }
    resp = requests.get(url = url,params = param,headers = headers)
    if resp.status_code == 200:
        data = resp.json()
        # 替换键名为中文
        for item in data:
            translated_item = {key_mapping.get(k, k): v for k, v in item.items()}
            all_data.append(translated_item)
    else:
        print("请求失败")
        break
    start += limit
    length -= limit
    
resp.close()
with open("douban.json",mode="w",encoding="utf-8") as f:
    import json
    json.dump(all_data,f,ensure_ascii=False,indent=4)  #将数据写入文件中，ensure_ascii=False表示不转义中文，indent=4表示缩进4个空格

print("完成作业！\n")

