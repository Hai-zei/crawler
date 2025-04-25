#抓取评论

#1.找到没有加密的参数，                            #window.asrsea()函数
#2.对参数进行加密、且按照网易逻辑  params、enSeckey; params => encText,  encSecKey => encSecKey
#3.进行请求

import requests
from Crypto.Cipher import AES
from base64 import b64encode
import json
import csv

url = "https://music.163.com/weapi/comment/resource/comments/get?csrf_token="
#真实参数
data = {
    "csrf_token": "",
    "cursor": "-1",
    "offset": "0",
    "orderType": "1",
    "pageNo": "1",
    "pageSize": "20",
    "rid": "A_PL_0_879463910",
    "threadId": "A_PL_0_879463910"
}
e = "010001"
f = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
g = "0CoJUm6Qyw8W8jud"
i = "BathJPxJPtDconbC"
def get_encSecKey():
    return "9e0435fe3f3aaf4dfb46b366c8808b312742f79328d7ef0356779e256e1e54e40049c4b80a4ea5eea1ad06115ddce364d4f0dc0eb2e445ad37eca305bb5f9de55ab70036c8fb449cc89c961bb3f90f3249bc5e10ee3f91453b138f1bf3dd9714803fb256e97ac5653fb243f97dded2c85714eb6052d04d70c6ec8770a2e8f7b4"
def get_params(data):   #默认收到字符串
    first = enc_params(data,g)
    second = enc_params(first,i)
    return second   #返回paramrs

def to_16(data):
    pad = 16 - len(data)%16
    data += chr(pad) * pad
    return data

def enc_params(data,key):   #加密过程
    iv = "0102030405060708"
    aes = AES.new(key=key.encode("utf-8"),IV=iv.encode("utf-8"),mode=AES.MODE_CBC) #创建加密器
    data = to_16(data)
    bs = aes.encrypt(data.encode("utf-8"))  #传入参数必须使用字节
    return str(b64encode(bs),"utf-8")   #转化成字符串返回

#处理加密过程，从原网页当中查找相关的代码情况
'''
    function a(a) { #16位随机字符串
        var d, e, b = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", c = "";
        for (d = 0; a > d; d += 1)  #循环16次
            e = Math.random() * b.length,   #随机数
            e = Math.floor(e),  #取整
            c += b.charAt(e);   #取字符串中的相应位置字母
        return c
    }

    function b(a, b) {  #其中a是要加密的过程
        var c = CryptoJS.enc.Utf8.parse(b)  #因为c是作为密钥使用，所以传进来的b就是作为密钥使用
          , d = CryptoJS.enc.Utf8.parse("0102030405060708")
          , e = CryptoJS.enc.Utf8.parse(a)  #e是数据
          , f = CryptoJS.AES.encrypt(e, c, {    #AES加密算法
            iv: d,  #iv偏移量
            mode: CryptoJS.mode.CBC         #模式：CBC  
                                            #已经有模式、数据、还差密钥所以c是密钥
        });
        return f.toString()
    }

    function c(a, b, c) {
        var d, e;
        return setMaxDigits(131),
        d = new RSAKeyPair(b,"",c),
        e = encryptedString(d, a)
    }
    function d(d, e, f, g) { d:数据 e:010001
        var h = {} # 空对象
          , i = a(16);  # i 16位随机字符串  所有可以将i进行固定来保证数据
        return h.encText = b(d, g),     #g为密钥使用
        h.encText = b(h.encText, i),    #返回的是params i密钥
            #进行两次函数
        h.encSecKey = c(i, e, f),       #返回的是encSecKey, e、f为固定数据 ,所以当i固定时，encSecKey也固定
        h
    }

'''
resp = requests.post(url,data={
    "params":get_params(json.dumps(data)),
    "encSecKey":get_encSecKey()
})
response_data = resp.json()
hot_comments = response_data.get("data",{}).get("hotComments",{})

with open("comment.csv",mode="w",encoding="utf-8",newline="") as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(["评论内容", "用户昵称", "点赞数"])
    for comment in hot_comments:
        content = comment.get("content","")#评价内容
        nickname = comment.get("user",{}).get("nickname","")#用户昵称
        like_count = comment.get("likedCount",0)#点赞数
        csv_writer.writerow([content,nickname,like_count])

print("Over!\n")
resp.close()
