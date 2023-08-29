import csv
import multiprocessing
import os.path
import time
from secrets import token_urlsafe

import pandas as pd
import psutil
import requests
import win32api
import win32con
from matplotlib import pyplot as plt, ticker

csv_filepath = os.path.join(os.path.dirname(__file__), "net.csv")
image_path = os.path.join(os.path.dirname(__file__), "net.jpg")


def net_plot():
    df = pd.read_csv(csv_filepath, header=None, names=["date", "time", "upload", "download"])
    df_records = df.shape[0]
    # net_data = df["date"]
    net_time = df["time"]
    # net_upload = df["upload"]
    net_down = df["download"]
    try:
        window_x = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)  # 获得屏幕分辨率X轴
        window_y = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)  # 获得屏幕分辨率Y轴
    except Exception as e:
        print(e)
    if not (window_x and window_y):
        window_x = 1920
        window_y = 1080
    fig = plt.figure(figsize=(window_x / 100 * 0.8, window_y / 100 * 0.8))  # 绘图窗口尺寸，基于当前电脑分辨率
    fig.supxlabel('Time')
    fig.supylabel('Speed MByte/s')
    fig.subplots_adjust(hspace=0.1, wspace=0.1)
    plt.rcParams["font.sans-serif"] = ["SimHei"]  # 设置字体
    plt.rcParams["axes.unicode_minus"] = False  # 该语句解决图像中的“-”负号的乱码问题
    
    ax = plt.subplot(111)
    ax.text(0.02, 0.9, c="b", s="show net speed", transform=ax.transAxes)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(base=int(df_records / 5)))  # x轴显示五个时间点
    plt.plot(net_time, net_down, color="b")
    plt.savefig(image_path, dpi=1200)
    # plt.show()


def net_watch():
    if os.path.exists(csv_filepath):
        random_string = token_urlsafe(16)
        os.rename(csv_filepath, os.path.join(os.path.dirname(csv_filepath), f"{random_string}.csv"))
    while True:
        sent_before = psutil.net_io_counters().bytes_sent  # 已发送的流量
        recv_before = psutil.net_io_counters().bytes_recv  # 已接收的流量
        time.sleep(1)
        sent_now = psutil.net_io_counters().bytes_sent
        recv_now = psutil.net_io_counters().bytes_recv
        date = time.strftime("%Y-%m-%d")
        time_info = time.strftime("%H:%M:%S")
        sent = round((sent_now - sent_before) / 1024 / 1024, 3)  # 算出1秒后的差值
        recv = round((recv_now - recv_before) / 1024 / 1024, 3)
        with open(csv_filepath, 'a+', encoding='utf_8_sig', newline='') as f:
            fieldnames = ['日期', '时间', '上传', '下载']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            print(f"time:{date} {time_info}, upload:{sent}MByte/s, download:{recv}MByte/s.")
            writer.writerow({'日期': date, '时间': time_info, '上传': sent, '下载': recv})  # 单位是 MB/S


def net_download(url: str):
    while True:
        down_filename = "net_test"
        file = requests.get(url).content
        with open(down_filename, "wb") as f:
            f.write(file)
        down_filepath = os.path.join(os.path.dirname(__file__), down_filename)
        if os.path.exists(down_filepath):
            os.remove(down_filepath)
            ...
        else:
            print(f"{time.strftime('%Y-%m-%d %H%M%S')} file download failed.")
            ...


def multi_core(download_link=None):
    if not download_link:
        raise Exception("please give download link")
    pool = multiprocessing.Pool(processes=4)
    pool.apply_async(func=net_watch)
    pool.apply_async(func=net_download, args=(download_link,))
    pool.close()
    # pool.join()
    # 这个打开会阻塞主进程（由于子进程是死循环会导致无法退出一直跑流量），所以我们选择不阻塞主进程的方式
    # 利用multiprocessing.Pool创建的是守护进程这一特性，我们可以通过终止主进程来结束其他子进程


def count_time(duration_time=0):
    if not isinstance(duration_time, int):
        raise Exception("value should be int type.")
    if duration_time < 0:
        raise Exception("value should more than zero.")
    if duration_time > 86400:
        duration_time = 86400  # 最大值限制，防止烧流量过多
    print("Countdown start.")
    count = duration_time
    while count:
        print(count)
        time.sleep(1)
        count = count - 1
    print("Countdown end.")



if __name__ == '__main__':
    # 服务器文件下载链接
    multi_core(download_link=r"http://{your_server_ip}:8080/api/public/dl/bhhzmE1t/home/ubuntu/500m.txt")
    """
    1分钟 = 60
    1小时 = 60 * 60 = 3600
    1天 = 60 * 60 * 24 = 86400
    """
    # 测试持续时间
    count_time(duration_time=60 * 3)
    # 保存绘制的图片
    net_plot()
