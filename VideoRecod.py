import time
import cv2
from PyQt5 import QtCore, QtGui
from Ui_renjigongxiao import Ui_MainWindow
import numpy
import matplotlib.pyplot as plot
import Ui_renjigongxiao
def videoCapture(CAM_NUM):
    #timer_camera = QtCore.QTimer()
    camera = cv2.VideoCapture(CAM_NUM) #获取摄像头
    fps = camera.get(cv2.CAP_PROP_FPS) #获取帧率
    width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH)) #一定要转int 否则是浮点数
    height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
    size = (width,height) #大小
    fourcc = cv2.VideoWriter_fourcc('I', '4', '2', '0')



    out = cv2.VideoWriter('123asd.avi', fourcc, fps, size) #初始化文件写入 文件名 编码解码器 帧率 文件大小
    while True:
        ret, frame = camera.read()
        if ret == True:
            frame = cv2.flip(frame, 1)
            out.write(frame)
            cv2.imshow("frame", frame)

            # show = cv2.resize(self.image, (480, 320))
            # show = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
            # self.labelShowCamera.setPixmap(QtGui.QPixmap.fromImage(showImage))
            # self.labelShowCamera.setScaledContents(True)
            #numFramesRemaining-=1
            if cv2.waitKey(1) & 0xFF == ord('q'):  # 若检测到按键 ‘q’，退出
                break
        else:
            break
    time.sleep(1) #y延迟一秒关闭摄像头 否则会出现 terminating async callback 异步处理错误
    camera.release() #释放摄像头
    out.release()
    print('ok')
