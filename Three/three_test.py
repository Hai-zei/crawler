#代理：通过三方发送需求
#可以用于需要短时间内多次请求，高并发的场景，或者自己ip被封锁

import requests
#139.159.102.236:3128
proxies = {
    "http":"http://139.159.102.236:3128"
}
#不知道为什么要使用http
resp = requests.get("https://www.baidu.com",proxies=proxies)
resp.encoding = "utf-8"
print(resp.text)  
resp.close()