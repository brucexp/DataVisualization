import socket
import msvcrt
import struct, time
import threading
# from ctypes import *

from pynput import keyboard

#全局变量
isEnd = False
Reply = b''
Fatigue = 0
BrainLoad = 0
Attention = 0
Alert = 0


def senddata(list, cmd):
    tmp = list #空列表
    indice_bytes = bytearray(tmp)
    print("--------------数据区---------------------")
    print(type(indice_bytes), "indice_bytes:",indice_bytes)
    print(indice_bytes)
    print("-------------------------------------\n")
    data_len = len(indice_bytes)
    toSe = struct.pack('<I', data_len) #低位在前
    print("-------------数据区长度---------------")
    print(toSe,type(toSe))
    print("-------------------------------------\n")
    sent_pack_length = 7
    # sent_pack = bytes(sent_pack_length)#sent_pack_length#
    sent_pack_byteArray = bytearray(sent_pack_length)
    print("-----------------初始化发送字节数组----------------")
    print(sent_pack_byteArray)
    print("-------------------------------------------\n")
    """发送字节数组赋值
    """
    sent_pack_byteArray[0] = 0x55# 十六进制
    sent_pack_byteArray[1] = 0x00
    sent_pack_byteArray[2] = cmd # 十进制
    sent_pack_byteArray[3] = toSe[0]
    sent_pack_byteArray[4] = toSe[1]
    sent_pack_byteArray[5] = toSe[2]
    sent_pack_byteArray[6] = toSe[3]
    print("-------字节数组包头赋值----------------")
    print(sent_pack_byteArray)
    print("------------------------------------\n")

    print("-----------------包头字节数据与数据字节数组组合成发送字节数组---------")
    sent_pack_byteArray = sent_pack_byteArray + indice_bytes
    print(sent_pack_byteArray)
    print("------------------------------------\n")

    sent_pack_length = sent_pack_length + len(indice_bytes)
    print("-----------发送字节数组长度-------------")
    print(sent_pack_length)
    print("------------------------------------\n")
    toCheck = 0
    '''校验位求和和
    '''
    for i in range(sent_pack_length):
        print("sent_pack_byteArray[" + str(i) + "]", sent_pack_byteArray[i])
        toCheck = toCheck + sent_pack_byteArray[i]
        print("tocheck:",toCheck)
    print(toCheck)
    if toCheck > 256:
        toCheck = toCheck -256 #忽略溢出
    print(toCheck)
    sent_pack_byteArray.append(toCheck)
    sent_pack = sent_pack_byteArray.hex()
    print("-------------sent_pack--------------")
    print(sent_pack)
    print("----------------------------------\n")
    return sent_pack_byteArray

def recvall(tcp_socket,length):
    data = b''
    while len(data) < length:
        more = tcp_socket.recv(length - len(data))
        if not more:
            raise EOFError('was expecting %d bytes but only received' '%d bytes before the socket closed')
        data += more

    return data

# def client(sent_pack_byteArray, length):
#
#     print(threading.current_thread().getName(),"开始工作")
#
#     global isEnd, Reply
#     tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 声明socket类型，同时生成链接对象
#     # 2. 链接服务器
#     server_addr = ('localhost', 9264)
#     # tcp_socket.settimeout(2)
#     tcp_socket.connect(server_addr)
#     #reply0 = recvall(tcp_socket, 14) #吸收掉有可能获取到的错误数据
#     print("Client has been assigned socket name", tcp_socket.getsockname())
#     tcp_socket.send(sent_pack_byteArray)  # 发送一条信息 python3 只接收btye流
#     Reply = recvall(tcp_socket, length)
#     print("The server said", type(Reply),Reply.hex())
#     while True:
#         time.sleep(1)
#         if isEnd:
#             print(isEnd)
#             break
#     tcp_socket.close()

def keyboard_on_press(key):
    global isEnd
    try:
        print('字母键{0} press'.format(key.char))
    except AttributeError:
        print('特殊键{0} press'.format(key))
        if key == keyboard.Key.esc:
            isEnd = True
            return False
# 开启键盘监听的线程函数
def start_key_listen():

    print(threading.current_thread().getName(), "开始工作")
    with keyboard.Listener(on_press=keyboard_on_press) as KeyboardListener:
        KeyboardListener.join()


def main():
    global Reply
    global Fatigue
    global BrainLoad
    global Attention
    global Alert
        # recv_data = tcp_socket.recv(1024)  # 接收一个信息，并指定接收的大小 为1024字节

    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 声明socket类型，同时生成链接对象
    # 2. 链接服务器
    server_addr = ('localhost', 9264)
    # tcp_socket.settimeout(2)
    tcp_socket.connect(server_addr)
    reply0 = recvall(tcp_socket, 3996) #吸收掉有可能获取到的错误数据 3996字节
    print(reply0.hex())
    print("Client has been assigned socket name", tcp_socket.getsockname())


    """
      STEP1:核对是否是需要的参考模式，向主机询问参考序号，命令编号44
    """
    cmd_cankaoxuhao = 44
    list = []
    getlength = 9
    flag = False
    sent_pack_byteArray = senddata(list, cmd_cankaoxuhao)

    tcp_socket.send(sent_pack_byteArray)  # 发送一条信息 python3 只接收btye流
    Reply = recvall(tcp_socket, getlength)
    print("The server said", type(Reply),Reply.hex())

    #监听键盘线程
    t1 = threading.Thread(target = start_key_listen)
    t1.setDaemon(True)  # 把子线程t1设置为守护线程，必须在start()之前设置
    t1.start()
    sum = 0
    time.sleep(1)
    sum = 0
    print("---开始核对参考模式--")
    #client(sent_pack_byteArray,getlength)
    # t2 = threading.Thread(target = client,args = (sent_pack_byteArray,getlength))
    # t2.start()
    time.sleep(1)  # 主线程停1秒
    reply_bytearray = bytearray(Reply)
    print("-------------")
    while not flag:
        sum = 0
        for i in range(getlength - 1):
            #print(i)
            sum = sum + reply_bytearray[i]
        if sum == reply_bytearray[getlength - 1]:
            print("校验成功，最后一位求和:",sum)

            flag = True
        else:
            print("校验失败,重新获取")
            tcp_socket.send(sent_pack_byteArray)
            Reply = recvall(tcp_socket, getlength)
            reply_bytearray = bytearray(Reply)
            print("The server said", type(Reply), Reply.hex())
    Reply = b''
    """
    STEP2:获取所有通道列表，核对是否所有需要通道都已满足，编号42
    """
    flag = False
    cmd_tdlb = 42
    getlength2 = 135
    sent_pack_2byteArray = senddata(list, cmd_tdlb)
    time.sleep(1)
    #while not flag:
    #sum = 0
    print("---开始核对通道--")
    tcp_socket.send(sent_pack_2byteArray)  # 发送一条信息 python3 只接收btye流
    Reply = recvall(tcp_socket, getlength2)
    time.sleep(1)  # 主线程停1秒
    reply_bytearray = bytearray(Reply)
    print("The server said", type(Reply), Reply.hex())

    while not flag:
        sum = 0
        for i in range(14):
            #print(i)
            sum = sum + reply_bytearray[i]
        while sum > 256 :
            sum = sum - 256
            print(sum)
        if sum == reply_bytearray[14]:
            print("校验成功，最后一位求和:",sum)

            flag = True
        else:
            print("校验失败,重新获取")
            tcp_socket.send(sent_pack_2byteArray)
            print(sent_pack_2byteArray.hex())
            Reply = b''
            print("The server said", type(Reply), Reply.hex())
            Reply = recvall(tcp_socket, getlength2)
            reply_bytearray = bytearray(Reply)
            print("The server said", type(Reply), Reply.hex())

    """
    55 00 29 07 00 00 00 00 41 31 2D 41 56 47 02 
    55 00 29 07 00 00 00 01 41 32 2D 41 56 47 04 
    55 00 29 07 00 00 00 02 46 33 2D 41 56 47 0B 
    55 00 29 07 00 00 00 03 46 34 2D 41 56 47 0D 
    55 00 29 07 00 00 00 04 50 33 2D 41 56 47 17 
    55 00 29 07 00 00 00 05 50 34 2D 41 56 47 19 
    55 00 29 07 00 00 00 06 50 7A 2D 41 56 47 60 
    55 00 29 07 00 00 00 07 4F 7A 2D 41 56 47 60 
    55 00 29 07 00 00 00 08 43 7A 2D 41 56 47 55 
    """
    """
    解析通道数据
    """
    td_list = []  # 先创建列表
    sum_data = 0
    for i in range(9): # 9个通道
        k = []
        td_list.append(k)
        for j in range(8, 14):  # 每个通道15个bit
            k.append(reply_bytearray[j + sum_data])
        #print(k)
        sum_data = (i+1) * 15
        #print(sum_data)
    """
    打印所选通道
    """
    for i in range(9):
        td = [chr(j) for j in td_list[i]]
        td_str = "".join(td)
        print(td_str)
    print("---------核对通道结束---------")

    flag = False
    Reply = b''

    """
    STEP3:订阅特征
    """
    flag = False
    cmd_tdlb = 23
    list_tdlb = [1,0] #订阅relative_power
    sent_pack_3byteArray = senddata(list_tdlb, cmd_tdlb)
    '''
    send = 5500170200000001006f
    '''
    getlength3 = 298
    time.sleep(1)
    print("-------开始订阅指标--------")
    Reply = b''
    tcp_socket.send(sent_pack_3byteArray)  # 发送一条信息 python3 只接收btye流
    time.sleep(2)  # 主线程停1秒
    Reply = recvall(tcp_socket, getlength3)
    reply_bytearray = bytearray(Reply)
    print("The server said", type(Reply), Reply)
    time.sleep(2)  # 主线程停1秒
    print("------------------------------------")
    #
    # reply_bytearray = bytearray(Reply)
    print(reply_bytearray.hex())
    while not flag:
        sum = 0
        for i in range(297):
            #print(i)
            sum = sum + reply_bytearray[i]
        while sum > 256 :
            sum = sum - 256
            print(sum)
        if sum == reply_bytearray[297]:
            print("校验成功，最后一位求和:",sum)
            flag = True
    """
    55 00 16 22 01 00 00 01 00 
    00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
    00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
    97 16 C2 3E B2 01 B0 3E 11 42 4C 3D 2E 90 EA 3D 8E BA DF 3C 48 BE 8C 3D B1 24 FF 3D F7 D3 1B 3D 
    39 BF 93 3E 5E 66 AE 3E FC 3A B5 3D 2F 4E 3F 3E 8F 5D 80 3D 36 0D E1 3D 18 5D 21 3E 61 4C D8 3C 
    95 FC AB 3E 0F 95 F9 3E A3 76 C7 3C 27 55 76 3D 9D E1 DE 3C 59 06 55 3D 23 D5 BE 3D DF E6 BE 3C 
    2C 0D 91 3E 58 9B FA 3E 51 A6 5C 3D BF D2 D9 3D 04 72 28 3C CF 72 5D 3D 3E 2A BD 3D D2 83 E9 3C 
    68 1F 01 3F D7 96 9C 3E 0E 7E 86 3D 91 BE C4 3D 57 AF 1A 3C 03 83 1C 3D 77 19 91 3D 71 45 BB 3C 
    05 C0 F5 3E 99 04 BD 3E AD 7F A5 3C 12 1E 30 3D 21 50 A7 3C FD E1 3E 3D F7 C3 AE 3D 22 6A B8 3C 
    D2 C4 E9 3E C9 8A 82 3E E4 2B 6C 3D F2 20 B4 3D 02 A3 92 3C 01 06 9C 3D FE 0A F3 3D A1 95 A7 3D 
    42 
    """
    td_list2 = []  # 先创建列表
    count_tz = 0   # 特征数量
    for i in range(9): # 9个通道
        k = []
        td_list2.append(k)
        for j in range(8):  # 每个通道8个特征
            #print(reply_bytearray[9 + count_tz * 4:13 + count_tz * 4])
            templeData = struct.unpack('<f',reply_bytearray[9 + count_tz * 4:13 + count_tz * 4])
            k.append(templeData[0])
            #print(count_tz)
            count_tz += 1

    print(td_list2)




    print("------------")
    print("主线程结束了！")
    print(threading.active_count())  # 输出活跃的线程数


if __name__ == "__main__":
    main()


"""
解析数据
"""

