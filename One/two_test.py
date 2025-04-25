#爬取百度翻译的内容
#One
import requests
url = 'https://fanyi.baidu.com/sug'
s = input("请输入要翻译的内容：")
dat = {"kw":s}
headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
}
# 伪装成浏览器,百度翻译有一定的反爬机制，需要使用cookies
cookies = {
    "BIDUPSID": "24A41791095F2811EF5FA1FB17FA42BC",
    "PSTM": "1720789606",
    "H_WISE_SIDS": "61027_62325_62340_62347_62372_62382_62420_62422_62476_62493_62517_62457_62454_62453_62450_62538",
    "BA_HECTOR": "2g000l8000a0a4ag0ga02l2489anvu1jv72k322",
    "ZFY": "JUC1B9ua9GNaKF7i49kZAKtw8Ib6OHyK2TDjwNK9:B1M:C",
    "BAIDUID": "7DD7EB4A35CBCA8F95034BE73C097FA7:FG=1",
    "BAIDUID_BFESS": "7DD7EB4A35CBCA8F95034BE73C097FA7:FG=1",
    "H_PS_PSSID": "61027_61676_62325_62342_62700_62746_62330_62849_62862",
    "ab_sr": "1.0.1_ZGMzZmJlYmVhYzAyNTljY2MzMWQwODgzYmU2MjIzNDYyOGQxZDhhYjBkZmMyNTZhN2FhOTg1OWMzYjU1Y2U5ZGMxYTgwYjg2NzM2MTEwYWM3NDcxZWY4MDZmYzhmN2U5ZTQ4YzEyMmI3ZmIxODE1Y2Y0YzE3NzIzYTZiN2UwMTM1NGIwYTM3ZWFjNzJmMGM5ZDNlZDExMDgyZTEwZjU1ZQ==",
    "RT": "z=1&dm=baidu.com&si=d9f636c9-af68-4c4a-bef5-ba4e62b91d21&ss=m9831ao9&sl=d&tt=uph&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=ad1u"
}

#发送post请求,发送的数据必须放在字典当中，通过data是参数传入
resp = requests.post(url,data = dat,cookies=cookies)
print(resp.json())  # resp.json()将响应体转换为json格式

#Two
#url = https://movie.douban.com/j/chart/top_list?type=24&interval_id=100%3A90&action=&start=0&limit=20   后面参数太长

url = "https://movie.douban.com/j/chart/top_list"
#重新封装参数
param = {
    "type": "24",
    "interval_id": "100:90",
    "action": "",
    "strat": "0",
    "limit0": "20"
}
headers = {
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
}
#这样如果没有数据输出，有地址、参数，说明被反爬虫了
#resp = requests.get(url = url,params = param)
resp = requests.get(url = url,params = param,headers = headers)
print(resp.json())