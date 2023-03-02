#!/usr/bin/env python
import serial  
import string
import random
import time
from pylsl import StreamInfo, StreamOutlet
import globavar_com as gl_com
import globavar_eeg as gl_eeg
def callfordata():
  gl_eeg._init()
  COM = gl_com.get_value('COM')
  # COM = 'COM5'
  rawData = serial.Serial(COM,4800)
  info = StreamInfo('EDUduino', 'EEG', 1, 512, 'float32', 'myuid34234')
  outlet = StreamOutlet(info)
  i=1
  j=0
  raw = []
  processed = []
  second = 1200 #how many second?
  #file1 = open("result.csv", mode='w', encoding='utf-8')
  while(i==1):
    #print(t.read())
    if(rawData.read()==b'\xaa'):
      if(rawData.read()==b'\xaa'):
        #print("sss")
        c = rawData.read()
        if(c==b'\x04'):
          if(rawData.read()==b'\x80'):
            if(rawData.read()==b'\x02'):
              rawdata1=ord(rawData.read())*256+ord(rawData.read())
              if(rawdata1>32768):
                rawdata1=rawdata1-65536
                # gl_eeg.set_value('eeg_data',rawdata1)
                outlet.push_sample([rawdata1])
                # print("-----------------callfordata--------")
                # print(rawdata1)
              # outlet.push_sample([rawdata1])
              # print("-----------------callfordata--------")
              # print(rawdata1)
              # raw.append(rawdata1)#+'\n'
              # print(raw)
              # j = j + 1
              # if(j==512*second):
              #   i = 2
        #
        #
        # elif(c==b' '):
        #   #print("ssssssssss")
        #   if(rawData.read()==b'\x02'):
        #     #print("bbbbbbb")
        #     rawData.read()
        #     #if(t.read()==b'\xc8'):
        #     #print("ssssssssss")
        #     if(rawData.read()==b'\x83'):
        #       if(rawData.read()==b'\x18'):
        #         print("start to read big bao")
        #         #ii=1
        #         #while(ii<=8):
        #
        #         delta = ord(rawData.read())*256*256+ord(rawData.read())*256+ord(rawData.read())
        #         print("delta=")
        #         print(delta)
        #         processed.append(delta)
        #
        #         theta = ord(rawData.read())*256*256+ord(rawData.read())*256+ord(rawData.read())
        #         print("theta=")
        #         print(theta)
        #         processed.append(theta)
        #
        #         lowalpha = ord(rawData.read())*256*256+ord(rawData.read())*256+ord(rawData.read())
        #         print("lowalpha=")
        #         print(lowalpha)
        #         processed.append(lowalpha)
        #
        #         highalpha = ord(rawData.read())*256*256+ord(rawData.read())*256+ord(rawData.read())
        #         print("highalpha=")
        #         print(highalpha)
        #         processed.append(highalpha)
        #
        #         lowbeta = ord(rawData.read())*256*256+ord(rawData.read())*256+ord(rawData.read())
        #         print("lowbeta=")
        #         print(lowbeta)
        #         processed.append(lowbeta)
        #
        #         highbeta = ord(rawData.read())*256*256+ord(rawData.read())*256+ord(rawData.read())
        #         print("highbeta=")
        #         print(highbeta)
        #         processed.append(highbeta)
        #
        #         lowgamma = ord(rawData.read())*256*256+ord(rawData.read())*256+ord(rawData.read())
        #         print("lowgamma=")
        #         print(lowgamma)
        #         processed.append(lowgamma)
        #
        #         middlegamma = ord(rawData.read())*256*256+ord(rawData.read())*256+ord(rawData.read())
        #         print("middlegamma=")
        #         print(middlegamma)
        #         processed.append(middlegamma)
        #
        #             #  ii=ii+1
        #         #x=rawData.read()
        #         if(rawData.read()==b'\x04'):
        #               #print ("1")
        #               #x=rawData.read()#zzd
        #               #print(x)
        #               #y = x and '0x0f'
        #           attention = ord(rawData.read())#16转10进制
        #               #attention = str(attention)
        #               #attention = y
        #               #ssss.y = y
        #           print("专注度为：")
        #           print(attention)
        #           processed.append(attention)
        #           if(rawData.read()==b'\x05'):
        #             meditation = ord(rawData.read())#16转10进制
        #             print("放松度为：")
        #             print(meditation)
        #             processed.append(meditation)
        #             #raw = raw.append('B')+processed
        #             for k in range(len(processed),len(raw)):
        #               processed.append('NAN')
        #             #file1.write("{}\n".format(raw))
        #             #file1.write("{}\n".format(processed))
        #             #raw = []
        #             #processed = []
def main():
  callfordata()

if __name__ == "__main__":
    main()

#with open('result3.csv','w') as file:
#file1.write('raw,processed\n')
#for r,p in zip(raw,processed):
  #file1.write("{},{}\n".format(r,p))
                  
#file1.write("{}\n".format(raw))
#file1.write("{}\n".format(processed))
                  
#file1.write(raw)
#file2 = open("result2.csv", mode='w', encoding='utf-8')
#file2.write(attention)           
# file1.close()
#file2.close()
