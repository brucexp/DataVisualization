import socket
import msvcrt
import struct, time
import threading
import globalvar as gl
# from ctypes import *
from pynput import keyboard

#全局变量
isEnd = False
Reply = b''
FatigueData = 0
BrainLoadData = 0
AttentionData = 0
AlertData = 0


def senddata(list, cmd):
    tmp = list #空列表
    indice_bytes = bytearray(tmp)
    # print("--------------数据区---------------------")
    # print(type(indice_bytes), "indice_bytes:",indice_bytes)
    # print(indice_bytes)
    # print("-------------------------------------\n")
    data_len = len(indice_bytes)
    toSe = struct.pack('<I', data_len) #低位在前
    # print("-------------数据区长度---------------")
    # print(toSe,type(toSe))
    # print("-------------------------------------\n")
    sent_pack_length = 7
    sent_pack = bytes(sent_pack_length)#sent_pack_length#
    sent_pack_byteArray = bytearray(sent_pack_length)
    # print("-----------------初始化发送字节数组----------------")
    # print(sent_pack_byteArray)
    # print("-------------------------------------------\n")
    """发送字节数组赋值
    """
    sent_pack_byteArray[0] = 0x55# 十六进制
    sent_pack_byteArray[1] = 0x00
    sent_pack_byteArray[2] = cmd # 十进制
    sent_pack_byteArray[3] = toSe[0]
    sent_pack_byteArray[4] = toSe[1]
    sent_pack_byteArray[5] = toSe[2]
    sent_pack_byteArray[6] = toSe[3]
    # print("-------字节数组包头赋值----------------")
    # print(sent_pack_byteArray)
    # print("------------------------------------\n")

    # print("-----------------包头字节数据与数据字节数组组合成发送字节数组---------")
    sent_pack_byteArray = sent_pack_byteArray + indice_bytes
    # print(sent_pack_byteArray)
    # print("------------------------------------\n")

    sent_pack_length = sent_pack_length + len(indice_bytes)
    # print("-----------发送字节数组长度-------------")
    # # print(sent_pack_length)
    # print("------------------------------------\n")
    toCheck = 0
    '''校验位求和和
    '''
    for i in range(sent_pack_length):
        # print("sent_pack_byteArray[" + str(i) + "]", sent_pack_byteArray[i])
        toCheck = toCheck + sent_pack_byteArray[i]
        # print("tocheck:",toCheck)
    if toCheck > 256:
        toCheck = toCheck -256 #忽略溢出
    # print(toCheck)
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

def build_socket():
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 声明socket类型，同时生成链接对象
    # 2. 链接服务器
    server_addr = ('localhost', 9264)
    # tcp_socket.settimeout(2)
    tcp_socket.connect(server_addr)
    reply0 = recvall(tcp_socket, 3996) #吸收掉有可能获取到的错误数据 3996字节



def main():
    global Reply
    global FatigueData
    global BrainLoadData
    global AttentionData
    global AlertData
    global isEnd
    gl._init()
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 声明socket类型，同时生成链接对象
    # 2. 链接服务器
    server_addr = ('localhost', 9264)
    # tcp_socket.settimeout(2)
    tcp_socket.connect(server_addr)
    reply0 = recvall(tcp_socket, 3996) #吸收掉有可能获取到的错误数据 3996字节

    """
    订阅特征
    """
    flag = False
    cmd_tdlb = 23
    '''
       [0,0,70,51] #订阅abslutute_power,F3通道  F字符对应70， 3字符对应51   (46 33) 16进制
       [0,0,70,52] #订阅abslutute_power,F4通道  F字符对应70， 4字符对应52   (46 34) 16进制
       [0,0,80,51] #订阅abslutute_power,P3通道  P字符对应80， 3字符对应51   (50 33) 16进制
       [0,0,80,52] #订阅abslutute_power,P4通道  P字符对应80， 4字符对应52   (50 34) 16进制
       [0,0,67,122] #订阅abslutute_power,Cz通道  C字符对应67，z字符对应122  (43 7A) 16进制
    '''
    list_tdlb = [0,0,70,51] #订阅abslutute_power,F3通道  F字符十进制对应70， 3字符对应51
    list_tdlb2 = [0,0,70,52]  #F4通道
    list_tdlb3 = [0,0,80,51]  #P3通道
    list_tdlb4 = [0,0,80,52]  #P4通道
    list_tdlb5 = [0,0,67,122] #Cz通道
    sent_pack_byteArray = senddata(list_tdlb, cmd_tdlb)
    sent_pack_byteArray2 = senddata(list_tdlb2, cmd_tdlb)
    sent_pack_byteArray3 = senddata(list_tdlb3, cmd_tdlb)
    sent_pack_byteArray4 = senddata(list_tdlb4, cmd_tdlb)
    sent_pack_byteArray5 = senddata(list_tdlb5, cmd_tdlb)
    #Reply = b''
    tcp_socket.send(sent_pack_byteArray)  # 发送一条信息 python3 只接收btye流
    tcp_socket.send(sent_pack_byteArray2)
    tcp_socket.send(sent_pack_byteArray3)
    tcp_socket.send(sent_pack_byteArray4)
    tcp_socket.send(sent_pack_byteArray5)
    time.sleep(2)  # 主线程停1秒
    getlength3 = 620  # 124*5 = 620
    Reply = b''
    Reply = recvall(tcp_socket, getlength3)
    reply_bytearray = bytearray(Reply)
    print("The server said", type(Reply), Reply)
    time.sleep(2)  # 主线程停1秒
    print("--------------单次测试----------------------")

    reply_bytearray = bytearray(Reply)
    print(reply_bytearray.hex())
    #print("开始循环")
    # while not flag:
    #     sum = 0
    #     for i in range(getlength3-1):
    #         print(i)
    #         sum = sum + reply_bytearray[i]
    #     while sum > 256 : #忽略溢出
    #         sum = sum - 256
    #         print(sum)
    #     if sum == reply_bytearray[getlength3 -1 ]:
    #         print("校验成功，最后一位求和:",sum)
    #         flag = True
    '''
 
    55 00 17 04 00 00 00 00 00 46 33 e9 #F3通道
    55 00 17 04 00 00 00 00 00 46 34 ea #F4通道
    55 00 17 04 00 00 00 00 00 50 33 f3 #P3通道
    55 00 17 04 00 00 00 00 00 50 34 f4 #P4通道
    55 00 17 04 00 00 00 00 00 43 7a 2d #Cz通道
    -------数据样例------------
    55 00 16 74 00 00 00 00 00 
    6A FF 97 27 19 28 C7 41 
    92 1E 55 07 8C A9 8C 41 
    F9 70 5F 7A 4C AB 75 41 
    06 A8 6C C3 FB 01 4E 41 
    C9 9E A5 94 AD 51 7B 41 
    3A 90 D4 C1 7F AA 65 41 
    1E AB 89 6F B2 A5 60 41 
    B3 CA 3B 9E F3 C1 6D 41 
    FB 26 4F 3B 15 5B 42 41 
    89 96 FF 33 6C 25 46 41 
    33 56 0A 38 85 49 4D 41 
    9F 04 5B 93 EC F2 60 41 
    0F F8 C0 97 3B 32 1E 41 
    00 00 00 00 00 00 24 40 
    46 33 F2 
    '''
    count_print = 0  # 打印次数
    while True:  #不断获取发过来数据
        #time.sleep(1)
        Reply = b''
        Reply = recvall(tcp_socket, getlength3)
        reply_bytearray = bytearray(Reply)
        # print("The server said", type(Reply), Reply)
        #time.sleep(2)  # 主线程停1秒
        #print("----------------主循环-------------------")
        reply_bytearray = bytearray(Reply)
        #print(reply_bytearray.hex())
        # print("开始循环")
        td_list1 = []  # 先创建列表 原始特征
        td_list2 = []  # 先创建列表
        count_tz = 0   # 特征数量
        for i in range(5): # 5个通道
            k = []
            count_tz = 0
            new_k = []
            for j in range(8):  # 每个通道14个特征,取前8个特征delta, theta, lo alpha, hi alpha, lo beta, hi beta, lo gamma, hi gamma
                #print("-------------11111--------------")
                #print(reply_bytearray[9 + count_tz * 8+i * 124:17 + count_tz * 8+ i * 124].hex())
                templeData = struct.unpack('<d', reply_bytearray[9 + count_tz * 8 + i * 124 :17 + count_tz * 8 + i * 124])
                k.append(templeData[0])
                #print(count_tz)
                count_tz += 1
            td_list1.append(k)
            new_k = [x/sum(k) for x in k] #前8项特征归一化
            # print(sum(new_k))
            td_list2.append(new_k)
        #print(td_list1)
        """
        疲劳Fatigue：F3和F4通道theta功率的平均值 = (td_list2[0][1] + td_list2[1][1]) /2
        脑负荷BrainLoad：P3和P4通道alpha功率的平均值 = (td_list2[2][2] + td_list2[2][3] +td_list2[3][2]+ td_list2[3][3]) /2
        注意力Attention：Cz通道beta功率 = td_list2[4][4]+td_list2[4][5]
        警戒Alert：P3和P4通道beta功率的平均值 = (td_list2[2][4] + td_list2[2][5]+td_list2[3][4] + td_list2[3][5]) /2
        0-F3 1-F4 2-P3 3-P4 4-Cz
        relative_power[8] = [delta,theta,lo_alpha,hi_alpha,lo_beta,hi_beta,lo_gamma,hi_gamma]
        """
        FatigueData = (td_list2[0][1] + td_list2[1][1]) /2
        BrainLoadData = (td_list2[2][2] + td_list2[2][3] +td_list2[3][2]+ td_list2[3][3]) /2
        AttentionData = td_list2[4][4]+td_list2[4][5]
        AlertData = (td_list2[2][4] + td_list2[2][5]+td_list2[3][4] + td_list2[3][5]) /2
        gl.set_value('FatigueData',FatigueData)
        gl.set_value('BrainLoadData', BrainLoadData)
        gl.set_value('AttentionData', AttentionData)
        gl.set_value('AlertData', AlertData)
        gl.set_value('F3_theta',td_list1[0][1])
        gl.set_value('P3_alpha', td_list1[2][2])
        gl.set_value('Cz_beta', td_list1[4][4])
        gl.set_value('P3_beta', td_list1[2][4])
        print("------------子线程中原始解析出数据----------------------")
        count_print += 1
        print(count_print)
        print(AttentionData,FatigueData, BrainLoadData, AlertData)
        # print(td_list1[0][1],td_list1[2][2], td_list1[4][4], td_list1[2][4])

    tcp_socket.close()
    # print("------------")
    # print("主线程结束了！")
    # print(threading.active_count())  # 输出活跃的线程数
if __name__ == "__main__":
    main()
