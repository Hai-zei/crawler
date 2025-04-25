#   都是寻找m3u8文件
'''
# 流程：
    1. 找到iframe的src属性
    2. 通过src属性获取m3u8的url
    3. 下载视频
    4. 下载密钥
    5. 解密ts文件
    6. 合并ts文件
    7. 转化成mp4文件0
'''
from Crypto.Cipher import AES
import aiofiles
import aiohttp
import requests
import asyncio
import re

from Crypto.Util.Padding import unpad

# 通过正则表达式获取m3u8的url
def Get_first_url(url):
    headers = {
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
    }
    resp = requests.get(url,headers=headers)
    resp.encoding = "utf-8"
    obj = re.compile(r"video: { url: '(?P<m3u8_url>.*?)'",re.S)
    m3u8_url = obj.search(resp.text).group("m3u8_url")
    resp.close()
    return m3u8_url

# 下载m3u8文件
def download_m3u8_file(m3u8_url,tile):
   resp = requests.get(m3u8_url)
   with open(tile,mode="wb") as f:
         f.write(resp.content)

async def download_ts(url,name,session):
    async with session.get(url) as resp:
        async with aiofiles.open(f"video2/{name}",mode="wb") as f:
            await f.write(await resp.read())    #异步写入文件
    print(f"下载完成：{name}")
    


async def aio_downlaod(up_url):# https://ukzy.ukubf4.com/20250327/TjaCNYrL/2000kb/hls/
    tasks = []
    async with aiohttp.ClientSession() as session:
        async with aiofiles.open("不良人第1集_second_m3u8.txt",mode="r",encoding="utf-8") as f:
            async for line in f:
                if line.startswith("#"):
                    continue
                line = line.strip() #去除首尾空格、空白、换行符
                ts_url = up_url  + line
                name  = line.split("/")[-1] #拿到最后一部分标记为名字
                task = asyncio.create_task(download_ts(ts_url,name,session))   #创建任务
                tasks.append(task)
            await asyncio.gather(*tasks)

def get_key(url):
    resp = requests.get(url)
    key = resp.text.strip().encode("utf-8")
    return key

# 保留原有代码并注释掉
# async def dec_ts(name,key):
#     aes = AES.new(key=key,IV=b"0000000000000000",mode=AES.MODE_CBC)
#     async with aiofiles.open(f"video2/{name}",mode="rb") as f1,\
#         aiofiles.open(f"video2/temp_{name}",mode="wb") as f2:
#         bs = await f1.read()    #读文件
#         await f2.write(aes.decrypt(bs))
#
#     print(f"{name}处理完毕")

# 修复后的解密函数
async def dec_ts(name, key):
    aes = AES.new(key=key, IV=b"0000000000000000", mode=AES.MODE_CBC)
    async with aiofiles.open(f"video2/{name}", mode="rb") as f1, \
        aiofiles.open(f"video2/temp_{name}", mode="wb") as f2:
        bs = await f1.read()  # 读取文件
        try:
            decrypted_data = aes.decrypt(bs)  # 解密数据
            unpadded_data = unpad(decrypted_data, AES.block_size)  # 移除填充
            await f2.write(unpadded_data)  # 写入解密后的数据
            print(f"{name}处理完毕")
        except ValueError as e:
            print(f"{name}解密失败: {e}")

# 保留原有代码并注释掉
# async def aio_dec(key):
#     tasks = []
#     async with aiofiles.open("不良人第1集_second_m3u8.txt",mode="r",encoding="utf-8") as f:
#         async for line in f:
#             if line.startswith("#"):
#                 continue
#             line = line.strip()
#             name  = line.split("/")[-1]
#             task = asyncio.create_task(dec_ts(name,key))
#             tasks.append(task)
#         await asyncio.wait(tasks)

# 修复后的异步解密函数
async def aio_dec(key):
    tasks = []
    async with aiofiles.open("不良人第1集_second_m3u8.txt", mode="r", encoding="utf-8") as f:
        async for line in f:
            if line.startswith("#"):
                continue
            line = line.strip()
            name = line.split("/")[-1]
            task = asyncio.create_task(dec_ts(name, key))
            tasks.append(task)
        await asyncio.gather(*tasks)  # 使用 gather 替代 wait，提高效率

def merge_ts():

    pass

def main(url):
    for i in range(1, 2):

        # 找出相应的 html 文件
        # html = url.replace("-0.html", f"-0-{i}.html")

        # 再从中获得第一层的 m3u8 文件并且下载
        # first_m3u8_url = Get_first_url(html)
        # base_url = first_m3u8_url.rsplit("/", 3)[0] + "/"
        # download_m3u8_file(first_m3u8_url, f"不良人第{i}集_first_m3u8.txt")

        # with open(f"不良人第{i}集_first_m3u8.txt", mode="r", encoding="utf-8") as f:
        #     for line in f:
        #         if line.startswith("#"):
        #             continue
        #         else:
        #             line = line.strip()  # 去除首尾空格、空白、换行符
        #             second_m3u8_url = base_url + line
        #             download_m3u8_file(second_m3u8_url, f"不良人第{i}集_second_m3u8.txt")

        # 下载视频
        # second_m3u8_url_up = second_m3u8_url.replace("index.m3u8", "")
        # 异步协程
        # asyncio.run(aio_downlaod(second_m3u8_url_up))
        # 拿到密钥
        key_url = "https://ukzy.ukubf4.com/20250327/TjaCNYrL/2000kb/hls/key.key"  # 替换为实际的 key URL
        key = get_key(key_url)

        # 解密
        asyncio.run(aio_dec(key))
        
        # merge_ks():

    
if __name__ == "__main__":
    
    url = "https://hanxiucao.pages.dev/play/49027106-0.html"
    main(url)