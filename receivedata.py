import socket
import msvcrt
import struct, time
import threading
# from ctypes import *

from pynput import keyboard

#全局变量
isEnd = False
Reply = b''

def senddata(list, cmd):
    tmp = list #空列表
    indice_bytes = bytearray(tmp)
    print("--------------数据区---------------------")
    print(type(indice_bytes), "indice_bytes:",indice_bytes)
    print(indice_bytes)
    print("-------------------------------------\n")
    data_len = len(indice_bytes)
    toSe = struct.pack('<I', data_len)
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

def client(sent_pack_byteArray, length):

    print(threading.current_thread().getName(),"开始工作")

    global isEnd, Reply
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 声明socket类型，同时生成链接对象
    # 2. 链接服务器
    server_addr = ('localhost', 9264)
    # tcp_socket.settimeout(2)
    tcp_socket.connect(server_addr)
    #reply0 = recvall(tcp_socket, 14) #吸收掉有可能获取到的错误数据
    print("Client has been assigned socket name", tcp_socket.getsockname())
    tcp_socket.send(sent_pack_byteArray)  # 发送一条信息 python3 只接收btye流
    Reply = recvall(tcp_socket, length)
    print("The server said", type(Reply),Reply.hex())
    while True:
        time.sleep(1)
        if isEnd:
            print(isEnd)
            break
    tcp_socket.close()

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
        # recv_data = tcp_socket.recv(1024)  # 接收一个信息，并指定接收的大小 为1024字节

    """
    STEP1:核对是否是需要的参考模式，向主机询问参考序号，命令编号44
    """
    cmd_cankaoxuhao = 44
    list = []
    getlength = 9
    flag = False
    sent_pack_byteArray = senddata(list, cmd_cankaoxuhao)
    #监听键盘线程
    t1 = threading.Thread(target = start_key_listen)
    t1.setDaemon(True)  # 把子线程t1设置为守护线程，必须在start()之前设置
    t1.start()
    sum = 0
    time.sleep(1)
    #while not flag:
    sum = 0
    print("---开始循环--")
    #client(sent_pack_byteArray,getlength)
    t2 = threading.Thread(target = client,args = (sent_pack_byteArray,getlength))
    t2.start()
    time.sleep(1)  # 主线程停1秒
    reply_bytearray = bytearray(Reply)
    print("-------------")
    for i in range(getlength - 1):
        #print(i)
        sum = sum + reply_bytearray[i]
    if sum == reply_bytearray[getlength - 1]:
        print("校验成功，最后一位求和:",sum)
        flag = True
    else:
        print("校验失败,请按ESC结束后重新运行")

    #Reply = b''
    """
    STEP2:获取所有通道列表，核对是否所有需要通道都已满足，编号42
    """
    flag = False
    cmd_tdlb = 42
    sent_pack_2byteArray = senddata(list, cmd_tdlb)
    getlength2 = 135
    time.sleep(1)
    #while not flag:
    #sum = 0
    print("---开始核对通道--")
    # client(sent_pack_byteArray,getlength)
    t3 = threading.Thread(target=client, args=(sent_pack_2byteArray, getlength2))
    t3.start()
    time.sleep(1)  # 主线程停1秒
    reply_bytearray = bytearray(Reply)

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
    """解析通道数据
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
    print("----循环2结束----")
    flag = True
    Reply = b''

    """
    STEP3:订阅特征
    """
    flag = False
    cmd_tdlb = 23
    list_tdlb = [1,0]
    sent_pack_3byteArray = senddata(list_tdlb, cmd_tdlb)
    getlength3 = 1024
    time.sleep(1)
    print("---开始订阅指标--")
    Reply = b''
    t4 = threading.Thread(target=client, args=(sent_pack_3byteArray, getlength3))
    t4.start()
    time.sleep(2)  # 主线程停1秒
    print("------------------------------------")

    reply_bytearray = bytearray(Reply)
    print(reply_bytearray.hex())


    print("------------")
    print("主线程结束了！")
    print(threading.active_count())  # 输出活跃的线程数


if __name__ == "__main__":
    main()


"""
解析数据
"""

