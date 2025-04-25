#处理cookie
#使用session进行请求 --> 一连串请求
#用于在只能登陆后进行的操作

import requests
session = requests.session()
data = {
    "action": "login",
    "username": "18381927992",
    "password": "203105"
}
headers = {
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
}
url = "https://www.bibie.cc/user/action.html"
resp = session.post(url,data=data,headers=headers)

#因为访问的是个体化的故所以使用之前的session,掌握cookies.
resp = session.get("https://www.bibie.cc/user/action.html?action=bookcase&t=1744871907323")
print(resp.json())
resp.close()

'''
感觉没有成功，也可能是小网站根本没有做密码等信息。
resp = requests.get("https://www.bibie.cc/user/action.html?action=bookcase&t=1744871907323")
print(resp.json())
'''