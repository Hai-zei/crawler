# input()   程序是处于阻塞状态
# request.get()  在网络请求返回数据之前程序也是处于阻塞状态
# 当程序处于 IO 操作的时候，CPU 是空闲的。线程处于阻塞状态.
# 协程：当程序遇到IO操作的时候，选择性切换到其他任务上
import  asyncio
'''
async def run():
    print("hello world")
if __name__ == "__main__":
    g = run()   #此时的函数是一个异步协函数，得到的是一个协程对象
    asyncio.run(g)  #协程程序运行需要asyncio模块的支持
'''
import asyncio
import time

async def run1():
    print("hello rld1")
    await asyncio.sleep(3)  # 使用异步的 sleep
    print("hello wo1")

async def run2():
    print("hello ld2")
    await asyncio.sleep(2)  # 使用异步的 sleep
    print("hello wod2")

async def run3():
    print("hello d3")
    await asyncio.sleep(4)  # 使用异步的 sleep
    print("hello3")

async def main():
    # 创建任务
    g1 = asyncio.create_task(run1())
    g2 = asyncio.create_task(run2())
    g3 = asyncio.create_task(run3())
    list = [g1, g2, g3]
    # 等待所有任务完成
    await asyncio.gather(g1,g2,g3)    #一般await挂起操作放在协程对象前面

if __name__ == "__main__":
    t1 = time.time()
    asyncio.run(main())  # 使用 asyncio.run 启动事件循环
    t2 = time.time()
    print(f"总耗时：{t2-t1}秒")