#1.拿到contID
#2.拿到videoStatus返回的json. ->srcURL
#3.因为srcURL被简单加密，所以需要修整
#4.下载

import requests
url = "https://www.pearvideo.com/video_1799524"
cont_ID = url.split("_")[1]

#在字符串中使用变量一定要使用f""
videoStatus = f"https://www.pearvideo.com/videoStatus.jsp?contId={cont_ID}&mrd=0.08881654845430054"
headers = {
    "user-agent":
    "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/135.0.0.0 Mobile Safari/537.36 Edg/135.0.0.0",
    #防盗链：判断父网页是否正常。
    "referer": url

}

#一般步骤：headers、cookies、refer
resp = requests.get(videoStatus,headers=headers)
dic = resp.json()
srcUrl = dic['videoInfo']['videos']['srcUrl']
systemTime = dic['systemTime']
srcUrl = srcUrl.replace(systemTime,f"cont-{cont_ID}")
#   https://video.pearvideo.com/mp4/short/20250417/cont-1799524-16049685-hd.mp4
#   https://video.pearvideo.com/mp4/short/20250417/cont-1799524-16049685-hd.mp4
#   https://video.pearvideo.com/mp4/short/20250417/1744875378405-16049685-hd.mp4

#下载视频
with open("test.mp4",mode="wb") as f:
    f.write(requests.get(srcUrl).content)