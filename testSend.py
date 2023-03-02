"""
    文件名称: semg_host_udp.py
    程序功能:
        1. 采用UDP协议接收来自多个sEMG传感器的数据
        2. 对接收到的数据进行解包操作
        3. 采用一定的方式区分每个连接的传感器
    文件版本: v0.4（预测试版）
    程序作者: Bing
    创建时间: 2020.07.27
    修改时间: 2020.08.21
    更新记录:
        v0.1: 解决多通道数据接收混淆的问题
        v0.2: 修复了一些小问题
        v0.3: 解决数据输出流速度慢的问题
        v0.4: 解决多通道传感器数据未对齐的问题
        v0.5: 优化数据
"""

import time
import socket
import struct
import threading
import random
from pylsl import StreamInfo, StreamOutlet
stream_info = StreamInfo('EMG_hangyi', 'EMG', 10, 200, 'float32', 'hangyiwyz')
stream_outlet = StreamOutlet(stream_info)




if __name__ == "__main__":
    device_num=2
    while True:
        stream_outlet.push_sample(random.sample(range(0,100),10))
        time.sleep(0.1)
