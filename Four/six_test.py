#   使用异步操作
import asyncio
import aiohttp

urls = [
    "https://haowallpaper.com/link/common/file/previewFileImg/16254567043943808",

    "https://haowallpaper.com/link/common/file/previewFileImg/16579607989308800",

    "https://haowallpaper.com/link/common/file/previewFileImg/16546859435019648"
]
async def aidownload(url):
    name = url.split("/",7)[-1] # 提取文件名
    name = name + ".jpg"  # 添加文件扩展名
    #aiohttp.ClientSession()  # 创建一个 aiohttp 客户端会话对象    等价于requests.Session()
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:

            # aiofiles
            with open(name, "wb") as f:       # 因为异步所以需要await
                f.write(await resp.content.read())  # 异步读取响应内容并写入文件 resp.content.read()是一个异步操作等效于requests的resp.content
    print(f"{url}下载完成")
async def main():
    tasks = []
    for url in urls:
        tasks.append(aidownload(url))  # 将协程对象添加到任务列表中
    await asyncio.gather(*tasks)  # 等待所有任务完成

if __name__ == "__main__":
    asyncio.run(main())  # 使用 asyncio.run 启动事件循环