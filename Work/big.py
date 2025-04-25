import aiofiles
import aiohttp
import requests
import asyncio
import re
from Crypto.Cipher import AES
import os
import os
from aiohttp import ClientTimeout
import concurrent.futures
from Crypto.Util.Padding import pad
import psutil

# 确保目录存在
os.makedirs("video2", exist_ok=True)

# 确保目录存在的函数
def ensure_dir_exists(file_path):
    dir_name = os.path.dirname(file_path)
    if (dir_name and not os.path.exists(dir_name)):
        os.makedirs(dir_name, exist_ok=True)

# 通过正则表达式获取m3u8的url
def Get_first_url(url):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
    }
    resp = requests.get(url, headers=headers)
    resp.encoding = "utf-8"
    obj = re.compile(r"video: { url: '(?P<m3u8_url>.*?)'", re.S)
    m3u8_url = obj.search(resp.text).group("m3u8_url")
    resp.close()
    return m3u8_url

# 下载m3u8文件
def download_m3u8_file(m3u8_url, title):
    resp = requests.get(m3u8_url)
    with open(title, mode="wb") as f:
        f.write(resp.content)

semaphore = asyncio.Semaphore(15)  # 限制最大并发数为 10

# 检查路径是否合法的函数
def is_valid_path(path):
    try:
        os.path.normpath(path)
        return True
    except (OSError, ValueError):
        return False

# 更新 download_ts 函数，确保路径格式化并跳过非法路径
async def download_ts(url, name, session, retries=3):
    ts_path = os.path.normpath(os.path.join("video2", name.lstrip("/")))
    if not is_valid_path(ts_path):
        print(f"跳过不合法路径：{ts_path}")
        return

    for attempt in range(retries):
        try:
            async with semaphore:  # 使用信号量限制并发
                print(f"尝试下载：{name} (第 {attempt + 1} 次)")
                ensure_dir_exists(ts_path)  # 确保目录存在
                async with session.get(url) as resp:
                    async with aiofiles.open(ts_path, mode="wb") as f:
                        await f.write(await resp.read())
                print(f"下载完成：{name}")
                return
        except PermissionError as e:
            print(f"权限错误：{e} (文件路径：{ts_path})")
            return
        except asyncio.TimeoutError:
            print(f"超时：{name} (第 {attempt + 1} 次)")
            if attempt == retries - 1:
                raise

async def aio_download(up_url):
    tasks = []
    timeout = ClientTimeout(total=60)  # 设置总超时时间为 60 秒
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with aiofiles.open("不良人第1集_second_m3u8.txt", mode="r", encoding="utf-8") as f:
            async for line in f:
                if line.startswith("#"):
                    continue
                line = line.strip()
                ts_url = os.path.join(up_url, line.lstrip("/"))
                task = asyncio.create_task(download_ts(ts_url, line, session))
                tasks.append(task)
            await asyncio.gather(*tasks)
            
# 下载密钥
def download_key(key_url, key_path):
    resp = requests.get(key_url)
    with open(key_path, mode="wb") as f:
        f.write(resp.content)

# 修复 AES 密钥长度问题，使用 0 填充到 16 字节
def decrypt_ts_files(key, m3u8_path):
    key = bytes.fromhex(key)  # 使用给定的密钥字符串
    if len(key) not in [16, 24, 32]:
        key = key.ljust(16, b'\x00')  # 使用 0 填充到 16 字节

    with open(m3u8_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        if line.startswith("#") or line.strip() == "":
            continue
        ts_name = line.strip()
        ts_path = os.path.normpath(f"video2/{ts_name}")
        if not os.path.exists(ts_path):
            print(f"文件不存在，跳过：{ts_path}")
            continue
        try:
            with open(ts_path, "rb") as f:
                ts_data = f.read()
            cipher = AES.new(key, AES.MODE_CBC)
            decrypt_data = cipher.decrypt(ts_data)
            with open(ts_path, "wb") as f:
                f.write(decrypt_data)
        except ValueError as e:
            print(f"解密文件时出错：{ts_path}，错误信息：{e}")
        except PermissionError as e:
            print(f"权限错误，跳过文件：{ts_path}，错误信息：{e}")
        except Exception as e:
            print(f"解密文件时出错：{ts_path}，错误信息：{e}")

# 在合并 TS 文件时检查文件有效性
def merge_ts_files(m3u8_path, output_ts_path):
    with open(m3u8_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    with open(output_ts_path, "wb") as out_f:
        for line in lines:
            if line.startswith("#") or line.strip() == "":
                continue
            ts_name = line.strip()
            ts_path = f"video2/{ts_name}"
            if not os.path.exists(ts_path):
                print(f"文件不存在，跳过：{ts_path}")
                continue
            try:
                with open(ts_path, "rb") as in_f:
                    out_f.write(in_f.read())
            except Exception as e:
                print(f"合并文件时出错：{ts_path}，错误信息：{e}")

def force_close_file(file_path):
    """强制关闭占用文件的进程"""
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            for item in proc.open_files():
                if file_path in item.path:
                    print(f"强制关闭进程 {proc.info['name']} (PID: {proc.info['pid']}) 占用的文件: {file_path}")
                    proc.terminate()
                    proc.wait()
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            continue

# 更新 safe_remove 函数，跳过无法删除的文件
def safe_remove(file_path):
    try:
        os.remove(file_path)
    except PermissionError as e:
        print(f"文件被占用，无法删除：{file_path}，错误信息：{e}")
    except Exception as e:
        print(f"删除文件时出错：{file_path}，错误信息：{e}")

# 转换成mp4文件
def convert_to_mp4(ts_path, mp4_path):
    import subprocess
    command = f'ffmpeg -i {ts_path} -c copy {mp4_path}'
    subprocess.call(command, shell=True)


# 修改 main 函数，先解密再合并
def main(url):
    for i in range(1, 2):
        # 找出相应的html文件
        html = url.replace("-0.html", f"-0-{i}.html")

        # 再从中获得第一层的m3u8文件并且下载
        first_m3u8_url = Get_first_url(html)
        base_url = first_m3u8_url.rsplit("/", 3)[0] + "/"
        download_m3u8_file(first_m3u8_url, f"不良人第{i}集_first_m3u8.txt")

        with open(f"不良人第{i}集_first_m3u8.txt", mode="r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("#"):
                    continue
                else:
                    line = line.strip()  # 去除首尾空格、空白、换行符
                    second_m3u8_url = base_url + line
                    download_m3u8_file(second_m3u8_url, f"不良人第{i}集_second_m3u8.txt")

        # 检查 second_m3u8 文件是否存在
        second_m3u8_path = f"不良人第{i}集_second_m3u8.txt"
        if not os.path.exists(second_m3u8_path):
            print(f"文件不存在：{second_m3u8_path}，跳过处理。")
            continue

        # 下载视频
        second_m3u8_url_up = second_m3u8_url.replace("index.m3u8", "")
        # 异步协程
        asyncio.run(aio_download(second_m3u8_url_up))

        # 解密ts文件
        decrypt_ts_files("bc284e9dcfccefac", second_m3u8_path)

        # 合并ts文件
        merged_ts_path = f"merged_{i}.ts"
        merge_ts_files(second_m3u8_path, merged_ts_path)

        # 转换成mp4文件
        mp4_path = f"不良人第{i}集.mp4"
        convert_to_mp4(merged_ts_path, mp4_path)

        # 删除临时文件
        safe_remove(f"不良人第{i}集_first_m3u8.txt")
        safe_remove(second_m3u8_path)
        safe_remove(merged_ts_path)
        with open(second_m3u8_path, mode="r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("#") or line.strip() == "":
                    continue
                ts_name = line.strip()
                ts_path = f"video2/{ts_name}"
                safe_remove(ts_path)


if __name__ == "__main__":
    url = "https://hanxiucao.pages.dev/play/49027106-0.html"
    main(url)
