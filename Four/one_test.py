# 多线程
# 线程主要是执行单位、进程主要是资源单位
'''
#第一种创建线程
from threading import Thread    #线程类
def run():
    for i in range(5):
        print(f"run_{i}")
if __name__ == "__main__":
    t = Thread(target=run)   #创建线程对象
    t.start() 
    for i in range(5):
        print(f"mian_{i}")  #启动线程   #等待线程结束

    print("Over!")  

'''

from threading import Thread    #线程类
#第二种创建线程
class MyThread(Thread):  #继承Thread类
    def run(self):  #重写run方法
        for i in range(5):
            print(f"子线程_{i}")

if __name__ == "__main__":
    t = MyThread()  #创建线程对象
    #  t.run()  #直接调用run方法，子线程不会执行//等效普通类当中的函数调用
    t.start()  #启动线程
    for i in range(5):
        print(f"主线程_{i}")
    