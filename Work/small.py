'''
流程：
    1. html的页面源代码
    2. 从源代码当中抓取m3n8的url
    3. 通过m3u8的url获取ts文件的url
    4. 下载ts文件
    5. 合并ts文件
    6. 转化成mp4文件
'''
'''
import os
input_file = "c:\\Users\\67604\\Desktop\\爬虫\\mixed.m3u8"  # 输入的 m3u8 文件路径
output_file = "c:\\Users\\67604\\Desktop\\爬虫\\modified.m3u8"  # 输出的 m3u8 文件路径
base_url = "https://yzzy.play-cdn2.com/20220501/17371_bf7efd41/1000k/hls/"  # 替换的基础 URL
 # 打开 m3u8 文件并读取内容
with open(input_file, "r", encoding="utf-8") as file:
     lines = file.readlines()

 # 替换 .ts 文件路径
modified_lines = []
for line in lines:
    if line.strip().endswith(".ts"):  # 检查是否是 .ts 文件路径
         ts_file = line.strip()
         modified_lines.append(base_url + ts_file)  # 替换为完整路径
    else:
         modified_lines.append(line.strip())  # 保留其他内容

 # 将修改后的内容写入新的 m3u8 文件
with open(output_file, "w", encoding="utf-8") as file:
     file.write("\n".join(modified_lines))

print(f"替换完成，修改后的文件已保存到 {output_file}")

   #解析相关文件
n = 1
import requests
with open("modified.m3u8",mode="r",encoding="utf-8") as f:     
    for line in f:
         line = line.strip() # 去除首尾空格、空白、换行符
         if line.startswith("#"):
             continue    
         resp3 = requests.get(line)
         f = open(f"Work/video/{n}.ts",mode="wb")
         f.write(resp3.content)
         f.close()
         resp3.close()
         n += 1

'''

"""
    前面步骤，抓取m3u8文件从中获得相应的ts文件。
    补全后将其写在本地位置后，就能后面调用并且下载
    下面时将下载后的各个ts文件拼接成一个完整的mp4文件
"""


import os
import subprocess


def merge_ts_to_mp4():
    file_list = []
    # 假设文件编号从 1 到 35
    for i in range(1, 36):
        name = f"{i}.ts"
        file_path = f"Work/video/{name}"
        if os.path.exists(file_path):
            file_list.append(file_path)
        else:
            print(f"文件 {file_path} 不存在！")

    if not file_list:
        print("没有找到有效的 .ts 文件。")
        return

    # 生成包含所有 .ts 文件路径的文本文件
    with open('file_list.txt', 'w') as f:
        for file in file_list:
            f.write(f"file '{file}'\n")

    try:
        # 使用 subprocess 执行 ffmpeg 命令进行合并并转换为 MP4
        result = subprocess.run(['ffmpeg', '-f', 'concat', '-safe', '0', '-i', 'file_list.txt',
                                 '-c:v', 'libx264', '-c:a', 'aac', '-strict', 'experimental', 'movie1.mp4'],
                                capture_output=True, text=True, check=True)
        print("合并并转换为 MP4 成功！")
    except subprocess.CalledProcessError as e:
        print("合并并转换为 MP4 失败！")
        print("错误信息：")
        print(e.stderr)

    # 删除临时文件
    if os.path.exists('file_list.txt'):
        os.remove('file_list.txt')


if __name__ == '__main__':

    merge_ts_to_mp4()