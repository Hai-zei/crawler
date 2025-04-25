#多进程 （会含有内存）
import time 
from multiprocessing import Process  #进程类
def run(a):
    for i in range(5):
        print(f"{a}_{i}")

if __name__ == "__main__":
    p = Process(target=run,args={"1",})  #创建进程对象;传参必须使用元组
    p.start()  #启动进程
    for i in range(5):
        print(f"主进程_{i}")
        time.sleep(0.1) #主进程睡眠0.1秒,让子进程有机会执行

    print("Over!")
