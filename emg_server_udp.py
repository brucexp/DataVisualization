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
from pylsl import StreamInfo, StreamOutlet
import globaval_emg as gl_emg


class SingleReceiverThread(threading.Thread):
    def __init__(self, server_socket, client_addrs, data_cache, server_cmd_start):
        """
        子进程初始化函数，创建对象时自动调用
        :param server_socket: 服务端socket
        :param client_addrs: 传递所有传感器的地址，根据需要排序过后的地址列表
        :param server_cmd_start: 传递服务端开始命令
        """
        threading.Thread.__init__(self)
        self.server_socket = server_socket
        self.client_addrs = client_addrs
        self.data_cache = data_cache
        self.server_cmd_start = server_cmd_start
        self.device_num = len(client_addrs)
        self.client_data_cnt = 0  # 所有设备接收数据计数列表
        self._running = True

    def run(self):
        """
        子线程读取每个传感器数据，并存入全局数组中
        :return: 无
        """
        self.client_data_cnt = [0] * self.device_num    # 所有设备接收数据计数列表
        for ii in range(self.device_num):
            self.server_socket.sendto(self.server_cmd_start.encode(), self.client_addrs[ii])    # 发送开始指令

        while self._running:
            client_data, client_addr = self.server_socket.recvfrom(1024)   # 接收来自所有客户端的数据
            try:
                client_data = list(struct.unpack('BbbbbbbB', client_data))  # 尝试解包数据
            except struct.error:
                print("Client data unpack error.")                          # 如果解包失败，跳过此包
                client_data, client_addr = self.server_socket.recvfrom(1024)  # 接收来自所有客户端的数据
                try:
                    client_cmd = client_data.decode()                    # 解析指令
                except UnicodeDecodeError:
                    client_cmd = ""
                if client_cmd == "ready\n":                          # 如果指令是ready
                    for ii in range(self.device_num):
                        self.data_cache[ii].append(client_cmd)
                    self.terminate()
                continue
            # 解包成功后的处理
            # 1. 判断接收包所属客户端
            try:
                client_addr_position = self.client_addrs.index(client_addr)  # 尝试查找当前客户端地址在列表中位置，地址列表提前经过排序，符合需要的顺序
            except ValueError:                                          # 如果当前地址不在客户端列表中，则抛弃当前数据包
                continue
            # 2. 根据相应客户端计数，判断是否丢包
            # self.data_cache[client_addr_position].append(client_data)
            if client_data[7] == (self.client_data_cnt[client_addr_position]):  # 如果没有丢包，直接存入对应数据缓存中
                # 2.1 如果没有丢包，存入对应位置
                self.data_cache[client_addr_position].append(client_data)       # 存入缓存中对应位置
            else:
                # 2.2 如果存在丢包，判断丢包，并补全丢包，存入对应位置
                client_data_cnt_loss = client_data[7] - self.client_data_cnt[client_addr_position]  # 计算丢包数
                if client_data_cnt_loss < 0:                # 如果丢包数小于0，说明有折回
                    client_data_cnt_loss += 100             # 丢包数校正
                # 输出丢包信息
                print("丢包传感器序号: ", client_addr_position,
                      "丢包个数: ", client_data_cnt_loss,
                      "丢包位置: ", self.client_data_cnt[client_addr_position])
                for ii in range(client_data_cnt_loss + 1):                          # 填充缺包处
                    client_data_temp = client_data[0:7]
                    client_data_temp.append((self.client_data_cnt[client_addr_position] + ii) % 100)   # 填充缺包计数
                    self.data_cache[client_addr_position].append(client_data_temp)   # 填充缺包数据包
                self.client_data_cnt[client_addr_position] += client_data_cnt_loss  # 补充计数

            # 3.数据包计数控制更新
            self.client_data_cnt[client_addr_position] += 1
            if self.client_data_cnt[client_addr_position] >= 100:
                self.client_data_cnt[client_addr_position] -= 100

    def terminate(self):
        """
        结束子进程，暂时未用到
        :return:
        """
        self._running = False


class SEmgUdpReceiver:
    def __init__(self, max_device):  # 类初始化函数
        """
        sEMG信号接收器类初始化函数
        :param max_device: 用于初始最大可连接客户端数量
        """
        # 预定义值
        self.MAX_DEVICE = max_device    # 设备数量
        self.DATA_PRINT_EN = True       # 是否在python程序中打印输出数据信息，True-打印 | False-不打印
        self.BUF_SIZE = 1024  # 缓存大小，默认1024
        # pylsl相关参数
        self.stream_info = StreamInfo('EMG_hangyi', 'EMG', 7 * self.MAX_DEVICE, 200, 'float32', 'hangyiwyz')
        self.stream_outlet = StreamOutlet(self.stream_info)
        # 服务端相关参数
        self.server_host = "192.168.137.1"  # Server IP设置
        self.server_port = 8100  # Server 端口设置
        self.server_addr = (self.server_host, self.server_port)  # Server 地址
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # 设置服务端Socket参数
        self.server_cmd_start = "start\r"           # 服务端指令，开始传输
        self.server_cmd_stop = "stop\r"             # 服务端指令，停止传输
        self.server_cmd_blink = "blink\r"           # 服务端指令，指示灯闪烁
        self.server_cmd_mac = "mac\r"               # 服务端指令，获取mac地址
        self.server_cmd_accepted = "accepted\r"     # 服务端指令，指示已获取传感器地址
        self.server_running = True          # 进程运行控制位
        self.client_running = True          # 客户端接收控制位
        # 客户端相关参数
        self.client_addrs = []      # 保存客户端ip地址
        self.client_macs = []       # 保存客户端mac地址
        # 多线程相关参数
        self.client_thread = 0      # 保存客户端接收数据线程
        # 数据相关参数
        self.data_cache = [[]for ii in range(self.MAX_DEVICE)]  # 全通道数据缓存，三维数据列表，维度分别为[MAX_DEV*LEN*8]，[通道*缓冲区长度*8个数据]

    def server_open(self):
        """
        1. 打开UDP服务端
        2. 侦听客户端连接
        :return: 0-打开服务端失败 | 1-打开服务端成功
        """
        try:
            self.server_socket.bind(self.server_addr)
        except OSError:
            print("请打开服务端WiFi，并再次尝试.")
            return 0
        print("服务端已正常开启.")
        return 1

    def clients_accept(self):
        """
        获取所有设备连接信息，依次存入列表中
        1. 可以实现对设备刚开机后的连接信息获取
        2. 可以实现在上位机程序重开后，无需重启传感器的信息获取
        :return: 无
        """
        device_connected_num = 0  # 已连接客户端数目
        print("等待客户端连接...")
        while device_connected_num < self.MAX_DEVICE:
            # 1. 依次接收所有传感器的数据，包括初始ready数据及传输数据
            client_data, client_addr = self.server_socket.recvfrom(self.BUF_SIZE)
            # 2. 判断数据类型是否为指定数据
            try:
                # 2.1 判断数据是否为字符串"ready\n"
                client_cmd = client_data.decode()
                if client_cmd == "ready\n":
                    # 2.1.1 如果字符串是"ready\n"，说明传感器初始运行，此时为上位机及传感器正常开启情况，<运行至第3步>
                    pass
                else:
                    # 2.1.2 如果字符串不是"ready\n"，说明是其他未知信息，抛弃数据包，<跳过至第1步>
                    print("未知的客户端命令:", client_cmd)
                    continue
            except UnicodeDecodeError:
                # 2.2 当接收到的数据不是字符串时引发错误，说明传感器已运行，此时为上位机重启后的情况
                try:
                    # 2.2.1 尝试解包传感器发送的数据
                    client_data_unpack = struct.unpack("B" * 8, client_data)
                    if 0 <= client_data_unpack[7] <= 99:
                        # 2.2.1.1 如果解包后的数据最后一位数据包计数在[0-99]范围内，那么可以认为是传感器发送的数据包，向传感器发送停止指令，并<跳至第1步>
                        self.server_socket.sendto(self.server_cmd_stop.encode(), client_addr)  # 停止之前的数据发送
                        continue
                    else:
                        # 2.2.1.2 如果解包后的数据最后一位数据包计数不满足计数条件，说明是未知数据包，抛弃数据包，<跳过至第1步>
                        continue
                except struct.error:
                    # 2.2.2 当尝试解包传感器数据失败后引发错误，说明数据未知，抛弃数据包，<跳过至第1步>
                    continue
            # 3. 如果判断数据类型为指定数据，则判断地址是否在列表中
            if client_addr in self.client_addrs:
                # 3.1 如果此数据地址已在传感器列表中，抛弃数据包，<跳过至第1步>
                continue
            else:
                # 3.2 如果此数据地址不在列表中，则将地址保存至列表中，<完成1个地址添加>
                self.client_addrs.append(client_addr)
                self.server_socket.sendto(self.server_cmd_accepted.encode(), client_addr)  # 向传感器发送已接受信息命令
                device_connected_num += 1  # 已连接设备计数+1
                print("地址为:", client_addr, "的传感器已连接")
        print("所有设备已连接，已连接设备个数: ", device_connected_num)

    def clients_info(self):
        """
        1. 控制列表中传感器的LED灯闪烁，指示传感器已正常连接
        2. 获取所有设备信息，目前仅实现获取MAC地址的功能
        3. 获取到的MAC地址可以用作后续的传感器定序，将对应MAC地址的传感器设定为对应序号
        :return: 无
        """
        for ii in range(self.MAX_DEVICE):
            # 1. 依次控制每个传感器LED灯闪烁一次
            self.server_socket.sendto(self.server_cmd_blink.encode(), self.client_addrs[ii])
            # 2. 依次获取每个传感器的MAC地址
            while True:
                # 2.1 发送获取MAC地址的指令
                self.server_socket.sendto(self.server_cmd_mac.encode(), self.client_addrs[ii])
                time.sleep(0.1)  # 延时等待数据回复
                # 2.2 接收传感器数据
                client_data, client_addr = self.server_socket.recvfrom(self.BUF_SIZE)
                # 2.3 尝试解码传感器数据
                try:
                    # 2.3.1 如果解码传感器数据成功，则判断解码后的字符串是否为有效的MAC地址格式，否则抛弃数据包
                    client_mac = client_data.decode()  # 解析MAC地址
                    if client_mac[2] == ':':
                        # 2.3.1.1 如果解码得到的字符串中，第3个字符为':'，可以认为字符串符合MAC地址的格式，则获取成功，有一定误判风险
                        client_mac = client_mac.strip()
                        self.client_macs.append(client_mac)  # 添加MAC地址到列表中
                        print("客户端", ii + 1, "的MAC地址为: [", client_mac, "] .")
                        break  # 跳出死循环
                    else:
                        # 2.3.1.2 如果解码的字符串不符合MAC地址格式，则继续尝试获取传感器的MAC地址
                        continue
                except UnicodeDecodeError:
                    # 3.2 尝试解码传感器数据失败，说明传感器数据并非字符串，则抛弃数据包
                    pass

    def run(self):
        """
        用于处理多传感器数据接收及转发的进程，重载run函数
        :return: 无
        """
        # 1. 打开服务端
        while not self.server_open():  # 循环检测是否可以打开服务端
            time.sleep(0.5)  # 等待服务端打开

        # 2. 获取所有传感器设备地址存入列表
        self.clients_accept()           # 获取客户端地址
        time.sleep(0.5)                 # 等待所有客户端连接稳定

        # 3. 获取所有传感器设备信息存入列表
        self.clients_info()             # 获取客户端信息
        time.sleep(0.5)                 # 等待所有客户端稳定

        # 4. 如果需要根据MAC地址确定传感器顺序，在此添加传感器地址的排序调整代码，实现基于MAC地址的传感器排序（可选）

        # 5. 启动接收传感器数据子线程并发送开始指令
        self.client_thread = SingleReceiverThread(self.server_socket,
                                                  self.client_addrs,
                                                  self.data_cache,
                                                  self.server_cmd_start)

        self.client_running = True
        self.client_thread.start()  # 开启接收UDP数据子线程

        while self.client_running:
            data_output = []                                # 输出数据缓存
            data_cache_output = 0
            for ii in range(self.MAX_DEVICE):               # 循环叠加所有通道数据
                while True:
                    if data_cache_output == "ready\n":
                        self.client_running = False
                        break
                    elif data_cache_output == []:
                        break
                    try:
                        if len(self.data_cache[ii]) >= 100:
                            self.data_cache[ii].clear()
                            data_cache_output = []
                            break
                        data_cache_output = self.data_cache[ii].pop(0)
                        data_output += data_cache_output[:7]        # 提取各通道数据
                        # data_output += data_cache_output          # 测试对齐
                    except IndexError:
                        continue
                    break
                if not self.client_running:
                    break
            if not self.client_running:
                break
            if data_cache_output == []:
                continue
            self.stream_outlet.push_sample(data_output)     # pylsl 输出数据
            if self.DATA_PRINT_EN:
                gl_emg._init()
                gl_emg.set_value("emg_data", data_output)
                print(data_output)                          # 显示输出数据

    def terminate(self):
        """
        结束运行，暂时不用
        :return: 无
        """
        self.server_running = False


if __name__ == "__main__":
    device_num = 2
    while True:
        semg_udp_receiver = SEmgUdpReceiver(device_num)
        semg_udp_receiver.run()
