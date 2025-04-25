
# 'https://dushu.baidu.com/api/pc/getCatalog?data={"book_id":"4306340004"}'  === > 章节的内容(icd)
# 章节内部内容
# https://dushu.baidu.com/api/pc/getChapterContent?data={"book_id":"4306340004","cid":"4306340004|1568936898","need_bookinfo":1}
  
import requests
import aiohttp
import asyncio
import json
import time
import aiofiles

"""
1.同步操作：访问所有章节的cid和名称
2.异步操作：访问所有章节的内容
"""
async def aidownload(cid,b_id,title):
    data = {
        "book_id":b_id,
        "cid":f"{b_id}|{cid}",
        "need_bookinfo":1
    }
    data = json.dumps(data)
    url = f"https://dushu.baidu.com/api/pc/getChapterContent?data={data}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            dic = await resp.json()
            async with aiofiles.open(f"{title}.txt",mode="w",encoding="utf-8") as f:
                await f.write(dic['data']['novel']['content'])  # 异步写入文件

async def getCatalog(url):
    resp = requests.get(url)
    dic = resp.json()
    tasks = []  # 创建一个任务列表后面对每个章节的cid进行异步操作
    for item in dic['data']['novel']['items']:
        title = item['title']  # 章节名称
        cid = item['cid']  # 章节id
        '''所以可以在这里使用异步操作，更快'''
        tasks.append(asyncio.create_task(aidownload(cid,b_id,title)))

    await asyncio.wait(tasks)

if __name__ == "__main__":
    b_id = "4306340004"
    url = 'https://dushu.baidu.com/api/pc/getCatalog?data={"book_id":"'+ b_id +'"}'
    asyncio.run(getCatalog(url))