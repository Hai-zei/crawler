# 线程池：一次性开辟一些线程，直接给线程池提交任务
# 线程任务的调度交给线程池来完成

from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor

def fn(name):
    for i in range(5):
        print(f"{name}_{i}")

if __name__ == "__main__":
    #创建线程池
    #with 表示会自动开关
    with ThreadPoolExecutor(2) as t:  #最大线程数为5
        for i  in range(2):
            t.submit(fn,name = f"线程{i}")  #提交任务
    #后面内容会等线程池中的所有任务完成后再执行
    #注意换行符的堆积
    print("Over!")