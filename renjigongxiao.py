# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""
import random
import matplotlib.pyplot as plt
import qimage2ndarray
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot, QPoint, Qt, QTimer, QThread, pyqtSignal
from PyQt5.QtGui import QPixmap, QPainter, QColor, QPolygonF, QFont
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QLabel, QSplashScreen
from memory_pic import *
import cv2
import base64
import sys, os
import time
from Ui_renjigongxiao import Ui_MainWindow
import matplotlib
import threading
import globalvar as gl
#import receivedata
import testredata
import callForData
import globavar_com as gl_com

matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

#全局变量

Attention = False
MentalFatigue = False
BrainLoad = False
Alert = False
Emotion = False
BrainMuscleCoordination = False
ComprehensiveCognition = False

FatigueData = 0
BrainLoadData = 0
AttentionData = 0
AlertData = 0

Count = 0
Angle = -90
Cap = cv2.VideoCapture(0)  #初始化摄像头
S_flag = 0

# g_img = cv2.imread('D:\\testpyqt5\\renjigongxiao\\camera_not_open.png')

Fps = Cap.get(cv2.CAP_PROP_FPS)  # 获取帧率
width = int(Cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # 一定要转int 否则是浮点数
height = int(Cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
# width = 640
# height = 480
size = (width, height)  # 大小
#print("Size:", size)
#Fourcc = cv2.VideoWriter_fourcc('I', '4', '2', '0')
Fourcc = cv2.VideoWriter_fourcc('X','V','I','D')
filename = time.strftime("%m-%d-%H-%M-%S") + '.avi'

Out = None


def get_pic(pic_code, pic_name):
    image = open(pic_name, 'wb')
    image.write(base64.b64decode(pic_code))
    image.close()

get_pic(camera_not_open_png,'camera_not_open.png')
get_pic(yibiaopan2_png,'yibiaopan2.png')
get_pic(Pointer_png,'Pointer.png')
get_pic(start_png,'start.png')

g_img = cv2.imread('camera_not_open.png')


class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (defaults to None)
        @type QWidget (optional)
        """
        super(MainWindow, self).__init__(parent)

        self.timer_camera = QtCore.QTimer()  # 定时器
        # self.cap = cv2.VideoCapture()  #初始化摄像头
        # self.s_flag = 0     #摄像头打开标志
        self.count_time = 0 #摄像头打开时间
        self.CAM_NUM = 0
        self.setupUi(self)
        self.set_ui()
        self.slot_init() # 设置部分槽函数
        self.setQTimer()  # 开一个定时器来进行自动刷新屏幕
        self.dashboardList = [0, 0, 0, 0, 0, 0, 0]
        self.widget_2.setVisible(True)
        self.angle = 0
        self.angle2 = 0
        self.angle3 = 0
        self.angle4 = 0
        self.eeg_com = ''
        #self.mat

        # 显示"打开摄像头"前的图像
        global g_img
        g_img = cv2.cvtColor(g_img, cv2.COLOR_BGR2RGB)
        qimg = qimage2ndarray.array2qimage(g_img)
        self.labelShowCamera.setPixmap(QPixmap(qimg))



    def setQTimer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.angle = 0
        self.timer.start(50)

    '''
    UI初始化程序
    '''
    def set_ui(self):
        #获取当前路径的上一路径
        self.path =os.path.dirname(os.getcwd())#取当前目录上一级目录
        #self.x = self.frame.pos().x()
        #self.y = self.frame.pos().y()
        print(self.path)
        # 创建无边框程序
        #self.setWindowFlags(Qt.FramelessWindowHint)
        #创建一个指针
        self.set_pointer()

    '''
    设置仪表盘背景
    '''
    def set_background_painter(self):
        global Attention
        global MentalFatigue
        global BrainLoad
        global Alert
        global Emotion
        global BrainMuscleCoordination
        global ComprehensiveCognition
        global Angle
        global Count


        painter = QPainter(self)
        # self.scrollAreaWidgetContents.render(painter)
        painter.begin(self)
        side = min(self.width(), self.height())
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        #print(painter.device())
        yibiaopan_x = 160 #窗体位置
        yibiaopan_y = 810
        # yibiaopan_x = 0#窗体位置
        # yibiaopan_y = 0
        yibiaopan_width = self.label.width()
        yibiaopan_height = self.label.height()
        #print(yibiaopan_x,yibiaopan_y,yibiaopan_width,yibiaopan_height)
        dashboard = QPixmap()
        dashboard.load('yibiaopan2.png')
        #print("dashboard :", dashboard.size())
        Count = 0
        self.dashboardList = [0, 0, 0, 0, 0, 0, 0]
        if Attention:
            self.dashboardList[0] = 1
        if MentalFatigue:
            self.dashboardList[1] = 1
        if BrainLoad:
            self.dashboardList[2] = 1
        if Alert:
            self.dashboardList[3] = 1
        if Emotion:
            self.dashboardList[4] = 1
        if BrainMuscleCoordination:
            self.dashboardList[5] = 1
        if ComprehensiveCognition:
            self.dashboardList[6] = 1
        for i in self.dashboardList:
            if i:
                painter.drawPixmap(yibiaopan_x + (yibiaopan_width + 10) * Count, yibiaopan_y , yibiaopan_width, yibiaopan_height, dashboard)
                #self.drawspeedPoniter(Angle)
                #Angle = Angle + 0.1
                # if Angle > 90:
                #     Angle = -90 #零值
                Count += 1
        #print("Count",Count)

        # size = self.geometry()
        # print("size:", size)

        painter.end()

    '''
    设置指针图片
    '''
    def set_pointer(self):
        # self.label.setAttribute(Qt.WA_TranslucentBackground, True)  # 设置窗口真透明
        self.pointer = QPixmap()  #创建一个pixmap对象
        self.pointer.load('Pointer.png')
        self.pointer_w =self.pointer.width()/6  #重新计算指针大小以匹配表盘大小,缩放比例为X倍
        #print("pointer_w :",self.pointer_w)
        self.pointer_h =self.pointer.height()/6

    def drawPointer(self):
        #print(angle)
        global Count
        global FatigueData
        global BrainLoadData
        global AttentionData
        global AlertData
        # FatigueData = 0
        # BrainLoadData = 0
        # AttentionData = 0
        # AlertData = 0
        #print("--------------------传回主函数值--------------------------")
        FatigueData = gl.get_value('FatigueData')
        BrainLoadData = gl.get_value('BrainLoadData')
        AttentionData = gl.get_value('AttentionData')
        AlertData = gl.get_value('AlertData')
        #print( AttentionData,FatigueData, BrainLoadData,AlertData)
        self.fatigueAngle = -90 + (FatigueData-0.064)* 150/ (1 / 180)
        self.brainLoadAngle = -90 + (BrainLoadData-0.026) * 120/ (1 / 180)
        self.attentionAngle = -90 + (AttentionData-0.040) *150/ (1 / 180)
        self.alertAngle = -90 + (AlertData- 0.039)*100 / (1 / 180)
        # print('-------------------角度---------------')
        # print( self.attentionAngle + 90,self.fatigueAngle + 90, self.brainLoadAngle + 90, self.alertAngle+90)


        hourPoint = [QPoint(7,8), QPoint(-7,8), QPoint(0, -80)]
        #时钟指针颜色
        hourColor = QColor(200, 100, 0, 200)
        side = min(self.width(), self.height())
        #print("side:",side)
        # 计算大小以及坐标
        self.pointerList = [0, 0, 0, 0, 0, 0, 0] #存储指针中心坐标
        for i in range(Count):
            self.pointerList[i] = 160 + (self.label.width() + 10) * i + self.label.width() / 2
            #print(self.pointerList[i])
        pointer_x = 160 + (self.label.width() + 10) * (Count - 1) + self.label.width() / 2
        #print("pointer_x",pointer_x)
        pointer_y = 810 + self.label.height()

        if Count == 1:
            if Attention:
                self.angle = self.attentionAngle
                self.label_2.setText("注意力")
            if MentalFatigue:
                self.angle = self.fatigueAngle
                self.label_2.setText("精神疲劳")
            if BrainLoad:
                self.angle = self.brainLoadAngle
                self.label_2.setText("脑负荷")
            if Alert:
                self.angle = self.alertAngle
                self.label_2.setText("警戒")
            self.label_3.setText("")
            self.label_5.setText("")
            self.label_6.setText("")
            painter = QPainter(self)
            painter.setPen(Qt.NoPen)  # 无轮廓线
            painter.setBrush(hourColor)  # 填充色
            painter.setRenderHint(QPainter.Antialiasing)  # 绘制图像反锯齿
            painter.translate(self.pointerList[0], pointer_y)  # 将坐标放在表盘中间
            # painter.scale(side / 200, side / 200)
            painter.save()  # 保存坐标系状态
            painter.rotate(self.angle)  # roate()函数就是坐标的旋转函数。参数为顺时针角度
            painter.drawConvexPolygon(QPolygonF(hourPoint))
            painter.drawPixmap(-self.pointer_w / 2, -self.pointer_h, self.pointer_w, self.pointer_h, self.pointer)
            painter.restore()  # //恢复以前的坐标系状态
            #painter.drawText(self.pointerList[0], 600,"脑负荷")
            # drawPixmap(int x, int y, int width, int height, const QPixmap &pixmap)
            # This is an overloaded function.Draws the pixmap into the rectangle at position (x, y) with the given width and height.
            # print("hello")

        if Count == 2:
            if Attention:
                self.angle = self.attentionAngle
                self.label_2.setText("注意力")
                if MentalFatigue:
                    self.angle2 = self.fatigueAngle
                    self.label_3.setText("精神疲劳")
                if BrainLoad:
                    self.angle2 = self.brainLoadAngle
                    self.label_3.setText("脑负荷")
                if Alert:
                    self.angle2 = self.alertAngle
                    self.label_3.setText("警戒")
            if not Attention and MentalFatigue:

                self.angle = self.fatigueAngle
                self.label_2.setText("精神疲劳")

                if BrainLoad:
                    self.angle2 = self.brainLoadAngle
                    self.label_3.setText("脑负荷")
                if Alert:
                    self.angle2 = self.alertAngle
                    self.label_3.setText("警戒")
            if BrainLoad and Alert:
                self.angle = self.brainLoadAngle
                self.angle2 = self.alertAngle
                self.label_2.setText("脑负荷")
                self.label_3.setText("警戒")
            self.label_5.setText("")
            self.label_6.setText("")


            painter = QPainter(self)
            painter.setPen(Qt.NoPen)  # 无轮廓线
            painter.setBrush(hourColor)  # 填充色
            painter.setRenderHint(QPainter.Antialiasing)  # 绘制图像反锯齿
            painter.translate(self.pointerList[0], pointer_y)  # 将坐标放在表盘中间
            # painter.scale(side / 200, side / 200)
            painter.save()  # 保存坐标系状态
            painter.rotate(self.angle)  # roate()函数就是坐标的旋转函数。参数为顺时针角度
            painter.drawConvexPolygon(QPolygonF(hourPoint))
            painter.drawPixmap(-self.pointer_w / 2, -self.pointer_h, self.pointer_w, self.pointer_h, self.pointer)
            painter.restore()  # //恢复以前的坐标系状态

            #指针2
            painter2 = QPainter(self)
            painter2.setPen(Qt.NoPen)        #无轮廓线
            painter2.setBrush(hourColor)     #填充色
            painter2.setRenderHint(QPainter.Antialiasing)  # 绘制图像反锯齿
            painter2.translate(self.pointerList[1], pointer_y)  # 将坐标放在表盘中间
            #painter.scale(side / 200, side / 200)
            painter2.save()  # 保存坐标系状态
            painter2.rotate(self.angle2)#roate()函数就是坐标的旋转函数。参数为顺时针角度
            painter2.drawConvexPolygon(QPolygonF(hourPoint))
            painter2.drawPixmap(-self.pointer_w/2 , -self.pointer_h, self.pointer_w, self.pointer_h, self.pointer)
            painter2.restore()  #//恢复以前的坐标系状态

        if Count == 3:
            if not Attention:
                self.angle = self.fatigueAngle
                self.angle2 = self.brainLoadAngle
                self.angle3 = self.alertAngle
                self.label_2.setText("精神疲劳")
                self.label_3.setText("脑负荷")
                self.label_5.setText("警戒")
            if not MentalFatigue:
                self.angle = self.attentionAngle
                self.angle2 = self.brainLoadAngle
                self.angle3 = self.alertAngle
                self.label_2.setText("注意力")
                self.label_3.setText("脑负荷")
                self.label_5.setText("警戒")
            if not BrainLoad:
                self.angle = self.attentionAngle
                self.angle2 = self.fatigueAngle
                self.angle3 = self.alertAngle
                self.label_2.setText("注意力")
                self.label_3.setText("精神疲劳")
                self.label_5.setText("警戒")
            if not Alert:
                self.angle = self.attentionAngle
                self.angle2 = self.fatigueAngle
                self.angle3 = self.brainLoadAngle
                self.label_2.setText("注意力")
                self.label_3.setText("精神疲劳")
                self.label_5.setText("脑负荷")
            self.label_6.setText("")
            painter = QPainter(self)
            painter.setPen(Qt.NoPen)  # 无轮廓线
            painter.setBrush(hourColor)  # 填充色
            painter.setRenderHint(QPainter.Antialiasing)  # 绘制图像反锯齿
            painter.translate(self.pointerList[0], pointer_y)  # 将坐标放在表盘中间
            # painter.scale(side / 200, side / 200)
            painter.save()  # 保存坐标系状态
            painter.rotate(self.angle)  # roate()函数就是坐标的旋转函数。参数为顺时针角度
            painter.drawConvexPolygon(QPolygonF(hourPoint))
            painter.drawPixmap(-self.pointer_w / 2, -self.pointer_h, self.pointer_w, self.pointer_h, self.pointer)
            painter.restore()  # //恢复以前的坐标系状态

            #指针2
            painter2 = QPainter(self)
            painter2.setPen(Qt.NoPen)        #无轮廓线
            painter2.setBrush(hourColor)     #填充色
            painter2.setRenderHint(QPainter.Antialiasing)  # 绘制图像反锯齿
            painter2.translate(self.pointerList[1], pointer_y)  # 将坐标放在表盘中间
            #painter.scale(side / 200, side / 200)
            painter2.save()  # 保存坐标系状态
            painter2.rotate(self.angle2)#roate()函数就是坐标的旋转函数。参数为顺时针角度
            painter2.drawConvexPolygon(QPolygonF(hourPoint))
            painter2.drawPixmap(-self.pointer_w/2 , -self.pointer_h, self.pointer_w, self.pointer_h, self.pointer)
            painter2.restore()  #//恢复以前的坐标系状态
            #指针3
            painter3 = QPainter(self)
            painter3.setPen(Qt.NoPen)        #无轮廓线
            painter3.setBrush(hourColor)     #填充色
            painter3.setRenderHint(QPainter.Antialiasing)  # 绘制图像反锯齿
            painter3.translate(self.pointerList[2], pointer_y)  # 将坐标放在表盘中间
            #painter.scale(side / 200, side / 200)
            painter3.save()  # 保存坐标系状态
            painter3.rotate(self.angle3)#roate()函数就是坐标的旋转函数。参数为顺时针角度
            painter3.drawConvexPolygon(QPolygonF(hourPoint))
            painter3.drawPixmap(-self.pointer_w/2 , -self.pointer_h, self.pointer_w, self.pointer_h, self.pointer)
            painter3.restore()  #//恢复以前的坐标系状态

        if Count == 4:
            self.angle = self.attentionAngle
            self.angle2 = self.fatigueAngle
            self.angle3 = self.brainLoadAngle
            self.angle4 = self.alertAngle
            self.label_2.setText("注意力")
            self.label_3.setText("精神疲劳")
            self.label_5.setText("脑负荷")
            self.label_6.setText("警戒")
            painter = QPainter(self)
            painter.setPen(Qt.NoPen)  # 无轮廓线
            painter.setBrush(hourColor)  # 填充色
            painter.setRenderHint(QPainter.Antialiasing)  # 绘制图像反锯齿
            painter.translate(self.pointerList[0], pointer_y)  # 将坐标放在表盘中间
            # painter.scale(side / 200, side / 200)
            painter.save()  # 保存坐标系状态
            painter.rotate(self.angle)  # roate()函数就是坐标的旋转函数。参数为顺时针角度
            painter.drawConvexPolygon(QPolygonF(hourPoint))
            painter.drawPixmap(-self.pointer_w / 2, -self.pointer_h, self.pointer_w, self.pointer_h, self.pointer)
            painter.restore()  # //恢复以前的坐标系状态
            # 指针2
            painter2 = QPainter(self)
            painter2.setPen(Qt.NoPen)  # 无轮廓线
            painter2.setBrush(hourColor)  # 填充色
            painter2.setRenderHint(QPainter.Antialiasing)  # 绘制图像反锯齿
            painter2.translate(self.pointerList[1], pointer_y)  # 将坐标放在表盘中间
            # painter.scale(side / 200, side / 200)
            painter2.save()  # 保存坐标系状态
            painter2.rotate(self.angle2)  # roate()函数就是坐标的旋转函数。参数为顺时针角度
            painter2.drawConvexPolygon(QPolygonF(hourPoint))
            painter2.drawPixmap(-self.pointer_w / 2, -self.pointer_h, self.pointer_w, self.pointer_h, self.pointer)
            painter2.restore()  # //恢复以前的坐标系状态
            # 指针3
            painter3 = QPainter(self)
            painter3.setPen(Qt.NoPen)  # 无轮廓线
            painter3.setBrush(hourColor)  # 填充色
            painter3.setRenderHint(QPainter.Antialiasing)  # 绘制图像反锯齿
            painter3.translate(self.pointerList[2], pointer_y)  # 将坐标放在表盘中间
            # painter.scale(side / 200, side / 200)
            painter3.save()  # 保存坐标系状态
            painter3.rotate(self.angle3)  # roate()函数就是坐标的旋转函数。参数为顺时针角度
            painter3.drawConvexPolygon(QPolygonF(hourPoint))
            painter3.drawPixmap(-self.pointer_w / 2, -self.pointer_h, self.pointer_w, self.pointer_h, self.pointer)
            painter3.restore()  # //恢复以前的坐标系状态
            #指针4
            painter4 = QPainter(self)
            painter4.setPen(Qt.NoPen)        #无轮廓线
            painter4.setBrush(hourColor)     #填充色
            painter4.setRenderHint(QPainter.Antialiasing)  # 绘制图像反锯齿
            painter4.translate(self.pointerList[3], pointer_y)  # 将坐标放在表盘中间
            #painter.scale(side / 200, side / 200)
            painter4.save()  # 保存坐标系状态
            painter4.rotate(self.angle4)#roate()函数就是坐标的旋转函数。参数为顺时针角度
            painter4.drawConvexPolygon(QPolygonF(hourPoint))
            painter4.drawPixmap(-self.pointer_w/2 , -self.pointer_h, self.pointer_w, self.pointer_h, self.pointer)
            painter4.restore()  #//恢复以前的坐标系状态

        if Count == 5:
            painter = QPainter(self)
            painter.setPen(Qt.NoPen)  # 无轮廓线
            painter.setBrush(hourColor)  # 填充色
            painter.setRenderHint(QPainter.Antialiasing)  # 绘制图像反锯齿
            painter.translate(self.pointerList[0], pointer_y)  # 将坐标放在表盘中间
            # painter.scale(side / 200, side / 200)
            painter.save()  # 保存坐标系状态
            painter.rotate(self.angle)  # roate()函数就是坐标的旋转函数。参数为顺时针角度
            painter.drawConvexPolygon(QPolygonF(hourPoint))
            painter.drawPixmap(-self.pointer_w / 2, -self.pointer_h, self.pointer_w, self.pointer_h, self.pointer)
            painter.restore()  # //恢复以前的坐标系状态
            # 指针2
            painter2 = QPainter(self)
            painter2.setPen(Qt.NoPen)  # 无轮廓线
            painter2.setBrush(hourColor)  # 填充色
            painter2.setRenderHint(QPainter.Antialiasing)  # 绘制图像反锯齿
            painter2.translate(self.pointerList[1], pointer_y)  # 将坐标放在表盘中间
            # painter.scale(side / 200, side / 200)
            painter2.save()  # 保存坐标系状态
            painter2.rotate(self.angle)  # roate()函数就是坐标的旋转函数。参数为顺时针角度
            painter2.drawConvexPolygon(QPolygonF(hourPoint))
            painter2.drawPixmap(-self.pointer_w / 2, -self.pointer_h, self.pointer_w, self.pointer_h, self.pointer)
            painter2.restore()  # //恢复以前的坐标系状态
            # 指针3
            painter3 = QPainter(self)
            painter3.setPen(Qt.NoPen)  # 无轮廓线
            painter3.setBrush(hourColor)  # 填充色
            painter3.setRenderHint(QPainter.Antialiasing)  # 绘制图像反锯齿
            painter3.translate(self.pointerList[2], pointer_y)  # 将坐标放在表盘中间
            # painter.scale(side / 200, side / 200)
            painter3.save()  # 保存坐标系状态
            painter3.rotate(self.angle)  # roate()函数就是坐标的旋转函数。参数为顺时针角度
            painter3.drawConvexPolygon(QPolygonF(hourPoint))
            painter3.drawPixmap(-self.pointer_w / 2, -self.pointer_h, self.pointer_w, self.pointer_h, self.pointer)
            painter3.restore()  # //恢复以前的坐标系状态
            # 指针4
            painter4 = QPainter(self)
            painter4.setPen(Qt.NoPen)  # 无轮廓线
            painter4.setBrush(hourColor)  # 填充色
            painter4.setRenderHint(QPainter.Antialiasing)  # 绘制图像反锯齿
            painter4.translate(self.pointerList[3], pointer_y)  # 将坐标放在表盘中间
            # painter.scale(side / 200, side / 200)
            painter4.save()  # 保存坐标系状态
            painter4.rotate(self.angle)  # roate()函数就是坐标的旋转函数。参数为顺时针角度
            painter4.drawConvexPolygon(QPolygonF(hourPoint))
            painter4.drawPixmap(-self.pointer_w / 2, -self.pointer_h, self.pointer_w, self.pointer_h, self.pointer)
            painter4.restore()  # //恢复以前的坐标系状态
            # 指针5
            painter5 = QPainter(self)
            painter5.setPen(Qt.NoPen)  # 无轮廓线
            painter5.setBrush(hourColor)  # 填充色
            painter5.setRenderHint(QPainter.Antialiasing)  # 绘制图像反锯齿
            painter5.translate(self.pointerList[4], pointer_y)  # 将坐标放在表盘中间
            # painter.scale(side / 200, side / 200)
            painter5.save()  # 保存坐标系状态
            painter5.rotate(self.angle)  # roate()函数就是坐标的旋转函数。参数为顺时针角度
            painter5.drawConvexPolygon(QPolygonF(hourPoint))
            painter5.drawPixmap(-self.pointer_w / 2, -self.pointer_h, self.pointer_w, self.pointer_h, self.pointer)
            painter5.restore()  # //恢复以前的坐标系状态

        if Count == 6:
            painter = QPainter(self)
            painter.setPen(Qt.NoPen)  # 无轮廓线
            painter.setBrush(hourColor)  # 填充色
            painter.setRenderHint(QPainter.Antialiasing)  # 绘制图像反锯齿
            painter.translate(self.pointerList[0], pointer_y)  # 将坐标放在表盘中间
            # painter.scale(side / 200, side / 200)
            painter.save()  # 保存坐标系状态
            painter.rotate(self.angle)  # roate()函数就是坐标的旋转函数。参数为顺时针角度
            painter.drawConvexPolygon(QPolygonF(hourPoint))
            painter.drawPixmap(-self.pointer_w / 2, -self.pointer_h, self.pointer_w, self.pointer_h, self.pointer)
            painter.restore()  # //恢复以前的坐标系状态
            # 指针2
            painter2 = QPainter(self)
            painter2.setPen(Qt.NoPen)  # 无轮廓线
            painter2.setBrush(hourColor)  # 填充色
            painter2.setRenderHint(QPainter.Antialiasing)  # 绘制图像反锯齿
            painter2.translate(self.pointerList[1], pointer_y)  # 将坐标放在表盘中间
            # painter.scale(side / 200, side / 200)
            painter2.save()  # 保存坐标系状态
            painter2.rotate(self.angle)  # roate()函数就是坐标的旋转函数。参数为顺时针角度
            painter2.drawConvexPolygon(QPolygonF(hourPoint))
            painter2.drawPixmap(-self.pointer_w / 2, -self.pointer_h, self.pointer_w, self.pointer_h, self.pointer)
            painter2.restore()  # //恢复以前的坐标系状态
            # 指针3
            painter3 = QPainter(self)
            painter3.setPen(Qt.NoPen)  # 无轮廓线
            painter3.setBrush(hourColor)  # 填充色
            painter3.setRenderHint(QPainter.Antialiasing)  # 绘制图像反锯齿
            painter3.translate(self.pointerList[2], pointer_y)  # 将坐标放在表盘中间
            # painter.scale(side / 200, side / 200)
            painter3.save()  # 保存坐标系状态
            painter3.rotate(self.angle)  # roate()函数就是坐标的旋转函数。参数为顺时针角度
            painter3.drawConvexPolygon(QPolygonF(hourPoint))
            painter3.drawPixmap(-self.pointer_w / 2, -self.pointer_h, self.pointer_w, self.pointer_h, self.pointer)
            painter3.restore()  # //恢复以前的坐标系状态
            # 指针4
            painter4 = QPainter(self)
            painter4.setPen(Qt.NoPen)  # 无轮廓线
            painter4.setBrush(hourColor)  # 填充色
            painter4.setRenderHint(QPainter.Antialiasing)  # 绘制图像反锯齿
            painter4.translate(self.pointerList[3], pointer_y)  # 将坐标放在表盘中间
            # painter.scale(side / 200, side / 200)
            painter4.save()  # 保存坐标系状态
            painter4.rotate(self.angle)  # roate()函数就是坐标的旋转函数。参数为顺时针角度
            painter4.drawConvexPolygon(QPolygonF(hourPoint))
            painter4.drawPixmap(-self.pointer_w / 2, -self.pointer_h, self.pointer_w, self.pointer_h, self.pointer)
            painter4.restore()  # //恢复以前的坐标系状态
            # 指针5
            painter5 = QPainter(self)
            painter5.setPen(Qt.NoPen)  # 无轮廓线
            painter5.setBrush(hourColor)  # 填充色
            painter5.setRenderHint(QPainter.Antialiasing)  # 绘制图像反锯齿
            painter5.translate(self.pointerList[4], pointer_y)  # 将坐标放在表盘中间
            # painter.scale(side / 200, side / 200)
            painter5.save()  # 保存坐标系状态
            painter5.rotate(self.angle)  # roate()函数就是坐标的旋转函数。参数为顺时针角度
            painter5.drawConvexPolygon(QPolygonF(hourPoint))
            painter5.drawPixmap(-self.pointer_w / 2, -self.pointer_h, self.pointer_w, self.pointer_h, self.pointer)
            painter5.restore()  # //恢复以前的坐标系状态
            #指针6
            painter6 = QPainter(self)
            painter6.setPen(Qt.NoPen)        #无轮廓线
            painter6.setBrush(hourColor)     #填充色
            painter6.setRenderHint(QPainter.Antialiasing)  # 绘制图像反锯齿
            painter6.translate(self.pointerList[5], pointer_y)  # 将坐标放在表盘中间
            #painter.scale(side / 200, side / 200)
            painter6.save()  # 保存坐标系状态
            painter6.rotate(self.angle)#roate()函数就是坐标的旋转函数。参数为顺时针角度
            painter6.drawConvexPolygon(QPolygonF(hourPoint))
            painter6.drawPixmap(-self.pointer_w/2 , -self.pointer_h, self.pointer_w, self.pointer_h, self.pointer)
            painter6.restore()  #//恢复以前的坐标系状态
        if Count == 7:
            painter = QPainter(self)
            painter.setPen(Qt.NoPen)  # 无轮廓线
            painter.setBrush(hourColor)  # 填充色
            painter.setRenderHint(QPainter.Antialiasing)  # 绘制图像反锯齿
            painter.translate(self.pointerList[0], pointer_y)  # 将坐标放在表盘中间
            # painter.scale(side / 200, side / 200)
            painter.save()  # 保存坐标系状态
            painter.rotate(self.angle)  # roate()函数就是坐标的旋转函数。参数为顺时针角度
            painter.drawConvexPolygon(QPolygonF(hourPoint))
            painter.drawPixmap(-self.pointer_w / 2, -self.pointer_h, self.pointer_w, self.pointer_h, self.pointer)
            painter.restore()  # //恢复以前的坐标系状态
            # 指针2
            painter2 = QPainter(self)
            painter2.setPen(Qt.NoPen)  # 无轮廓线
            painter2.setBrush(hourColor)  # 填充色
            painter2.setRenderHint(QPainter.Antialiasing)  # 绘制图像反锯齿
            painter2.translate(self.pointerList[1], pointer_y)  # 将坐标放在表盘中间
            # painter.scale(side / 200, side / 200)
            painter2.save()  # 保存坐标系状态
            painter2.rotate(self.angle)  # roate()函数就是坐标的旋转函数。参数为顺时针角度
            painter2.drawConvexPolygon(QPolygonF(hourPoint))
            painter2.drawPixmap(-self.pointer_w / 2, -self.pointer_h, self.pointer_w, self.pointer_h, self.pointer)
            painter2.restore()  # //恢复以前的坐标系状态
            # 指针3
            painter3 = QPainter(self)
            painter3.setPen(Qt.NoPen)  # 无轮廓线
            painter3.setBrush(hourColor)  # 填充色
            painter3.setRenderHint(QPainter.Antialiasing)  # 绘制图像反锯齿
            painter3.translate(self.pointerList[2], pointer_y)  # 将坐标放在表盘中间
            # painter.scale(side / 200, side / 200)
            painter3.save()  # 保存坐标系状态
            painter3.rotate(self.angle)  # roate()函数就是坐标的旋转函数。参数为顺时针角度
            painter3.drawConvexPolygon(QPolygonF(hourPoint))
            painter3.drawPixmap(-self.pointer_w / 2, -self.pointer_h, self.pointer_w, self.pointer_h, self.pointer)
            painter3.restore()  # //恢复以前的坐标系状态
            # 指针4
            painter4 = QPainter(self)
            painter4.setPen(Qt.NoPen)  # 无轮廓线
            painter4.setBrush(hourColor)  # 填充色
            painter4.setRenderHint(QPainter.Antialiasing)  # 绘制图像反锯齿
            painter4.translate(self.pointerList[3], pointer_y)  # 将坐标放在表盘中间
            # painter.scale(side / 200, side / 200)
            painter4.save()  # 保存坐标系状态
            painter4.rotate(self.angle)  # roate()函数就是坐标的旋转函数。参数为顺时针角度
            painter4.drawConvexPolygon(QPolygonF(hourPoint))
            painter4.drawPixmap(-self.pointer_w / 2, -self.pointer_h, self.pointer_w, self.pointer_h, self.pointer)
            painter4.restore()  # //恢复以前的坐标系状态
            # 指针5
            painter5 = QPainter(self)
            painter5.setPen(Qt.NoPen)  # 无轮廓线
            painter5.setBrush(hourColor)  # 填充色
            painter5.setRenderHint(QPainter.Antialiasing)  # 绘制图像反锯齿
            painter5.translate(self.pointerList[4], pointer_y)  # 将坐标放在表盘中间
            # painter.scale(side / 200, side / 200)
            painter5.save()  # 保存坐标系状态
            painter5.rotate(self.angle)  # roate()函数就是坐标的旋转函数。参数为顺时针角度
            painter5.drawConvexPolygon(QPolygonF(hourPoint))
            painter5.drawPixmap(-self.pointer_w / 2, -self.pointer_h, self.pointer_w, self.pointer_h, self.pointer)
            painter5.restore()  # //恢复以前的坐标系状态
            #指针6
            painter6 = QPainter(self)
            painter6.setPen(Qt.NoPen)        #无轮廓线
            painter6.setBrush(hourColor)     #填充色
            painter6.setRenderHint(QPainter.Antialiasing)  # 绘制图像反锯齿
            painter6.translate(self.pointerList[5], pointer_y)  # 将坐标放在表盘中间
            #painter.scale(side / 200, side / 200)
            painter6.save()  # 保存坐标系状态
            painter6.rotate(self.angle)#roate()函数就是坐标的旋转函数。参数为顺时针角度
            painter6.drawConvexPolygon(QPolygonF(hourPoint))
            painter6.drawPixmap(-self.pointer_w/2 , -self.pointer_h, self.pointer_w, self.pointer_h, self.pointer)
            painter6.restore()  #//恢复以前的坐标系状态
            #指针7
            painter7 = QPainter(self)
            painter7.setPen(Qt.NoPen)        #无轮廓线
            painter7.setBrush(hourColor)     #填充色
            painter7.setRenderHint(QPainter.Antialiasing)  # 绘制图像反锯齿
            painter7.translate(self.pointerList[6], pointer_y)  # 将坐标放在表盘中间
            #painter.scale(side / 200, side / 200)
            painter7.save()  # 保存坐标系状态
            painter7.rotate(self.angle)#roate()函数就是坐标的旋转函数。参数为顺时针角度
            painter7.drawConvexPolygon(QPolygonF(hourPoint))
            painter7.drawPixmap(-self.pointer_w/2 , -self.pointer_h, self.pointer_w, self.pointer_h, self.pointer)
            painter7.restore()  #//恢复以前的坐标系状态

    '''
    绘制事件
    '''
    def paintEvent(self,event):
        #print('执行hjjjj')
        #paintEvent(event)
        #self.set_img_on_label()
        global Angle
        self.set_background_painter()
        self.drawPointer()
        # for i in self.dashboardList:
        #     if i:
        #         self.drawspeedPoniter(Angle)
        #         Angle = Angle + 1
        #         if Angle > 90:
        #             Angle = -90

    
    @pyqtSlot()
    def on_pushButton_3_clicked(self):
        """
        Slot documentation goes here.
        """
        global Attention
        global MentalFatigue
        global BrainLoad
        global Alert
        global Emotion
        global BrainMuscleCoordination
        global ComprehensiveCognition
        global Count
        # TODO: not implemented yet
        if self.checkBox.isChecked():
            Attention = True
            print("Attention")
        else:
            Attention = False
            print("No Attention")
        if self.checkBox_2.isChecked():
            MentalFatigue = True
            print("MentalFatigue")
        else:
            MentalFatigue = False
        if self.checkBox_3.isChecked():
            BrainLoad = True
            print("BrainLoad ")
        else:
            BrainLoad = False
        if self.checkBox_4.isChecked():
            Alert = True
            print("Alert")
        else:
            Alert = False
        if self.checkBox_5.isChecked():
            Emotion = True
            print("Emotion")
        else:
            Emotion = False
        if self.checkBox_6.isChecked():
            BrainMuscleCoordination = True
            print("BrainMuscleCoordination")
        else:
            BrainMuscleCoordination = False
        if self.checkBox_7.isChecked():
            ComprehensiveCognition = True
            print("ComprehensiveCognition")
        else:
            ComprehensiveCognition = False
        # receivedata.main()


    """
    视频显示及录屏功能
    """
    @pyqtSlot()
    def on_buttonOpenCamera_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.slotCameraButton()
    
    @pyqtSlot()
    def on_buttonVideoCapture_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.save_video()
        #self.timer_camera.start(30)
        #self.slot_init()

    # def slotVideoButtn(self):
    #     if self.timer_camera.isActive() == False:
    #         # 打开摄像头并录屏
    #         self.save_video()
    #     else:
    #         # 关闭摄像头并清空显示信息
    #         self.stopVideoCapture()


    # def videoCapture(self):
    #     # timer_camera = QtCore.QTimer()
    #     #self.camera = cv2.VideoCapture(self.CAM_NUM)  # 获取摄像头
    #     flag = self.cap.open(self.CAM_NUM)
    #     if flag == False:
    #         msg = QtWidgets.QMessageBox.warning(
    #              self, u"Warning", u"请检测相机与电脑是否连接正确",
    #             buttons=QtWidgets.QMessageBox.Ok,
    #             defaultButton=QtWidgets.QMessageBox.Ok)
    #     else:
    #         #self.timer_camera.start(30)
    #         self.buttonVideoCapture.setText("按q键结束")
    #
    #     fps = self.cap.get(cv2.CAP_PROP_FPS)  # 获取帧率
    #     print("fps:",fps)
    #     width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # 一定要转int 否则是浮点数
    #     height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    #     size = (width, height)  # 大小
    #     fourcc = cv2.VideoWriter_fourcc('I', '4', '2', '0')
    #     self.out = cv2.VideoWriter('123asd.avi', fourcc, fps, size)  # 初始化文件写入 文件名 编码解码器 帧率 文件大小
    #     while True:
    #         ret, frame = self.cap.read()
    #
    #         if ret == True:
    #             frame = cv2.flip(frame, 1)
    #             self.out.write(frame)
    #             show = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #             showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
    #             self.labelShowCamera.setPixmap(QtGui.QPixmap.fromImage(showImage))
    #             # if cv2.waitKey(1) & 0xFF ==ord('q'):  # 若检测到按键 ‘q’，退出
    #             #     break
    #         else:
    #             break
    #     time.sleep(1)  # y延迟一秒关闭摄像头 否则会出现 terminating async callback 异步处理错误
    #     self.cap.release()  # 释放摄像头
    #     self.out.release()
    #     self.labelShowCamera.clear()
    #     self.buttonVideoCapture.setText("开始录像")
    #     print('ok')

    # def stopVideoCapture(self):
    #     time.sleep(1)
    #     self.timer_video.stop()
    #     self.cap.release()  # 释放摄像头
    #     self.out.release()
    #     self.labelShowCamera.clear()
    #     self.buttonVideoCapture.setText("开始录像")

    def slot_init(self):
        self.timer_camera.timeout.connect(self.show_camera)

    def slotCameraButton(self):
        if self.timer_camera.isActive() == False:
            # 打开摄像头并显示图像信息
            self.openCamera()
        else:
            # 关闭摄像头并清空显示信息
            self.closeCamera()

    # 打开摄像头
    def openCamera(self):
        global Cap, width, height
        Cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)  # 设置宽度
        Cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)  # 设置长度
        flag = Cap.open(self.CAM_NUM)
        if flag == False:
            msg = QtWidgets.QMessageBox.warning(
                 self, u"Warning", u"请检测相机与电脑是否连接正确",
                buttons=QtWidgets.QMessageBox.Ok,
                defaultButton=QtWidgets.QMessageBox.Ok)
        else:
            self.timer_camera.start(10) #time_camera 定时器开始计时30ms，周期性发出timeout()信号，连接到show_camera()
            self.buttonOpenCamera.setText('关闭摄像头')


    # 关闭摄像头
    def closeCamera(self):
        global Cap, g_img
        time.sleep(2)
        Cap.release()
        self.count_time = 0
        self.timer_camera.stop()   #停止计时器
        self.labelShowCamera.clear()
        self.buttonOpenCamera.setText('打开摄像头')
        # g_img = cv2.imread('D:\\testpyqt5\\renjigongxiao\\camera_not_open.png')
        g_img = cv2.imread('camera_not_open.png')
        g_img = cv2.cvtColor(g_img, cv2.COLOR_BGR2RGB)
        qimg = qimage2ndarray.array2qimage(g_img)
        self.labelShowCamera.setPixmap(QPixmap(qimg))

    def save_video(self):
        global S_flag
        if self.count_time == 0:
            msg = QtWidgets.QMessageBox.warning(
                self, u"Warning", u"请先打开摄像头",
                buttons=QtWidgets.QMessageBox.Ok,
                defaultButton=QtWidgets.QMessageBox.Ok)
        if self.count_time > 0:  # 相机打开后才能录像
            S_flag = 1
            self.label_4.setText(" 正在录像")
            CameraWorkThread.start()
            #self.count_time = 0
        # cv2.imshow('img', g_img)
        # fps = self.cap.get(cv2.CAP_PROP_FPS)  # 获取帧率
        # #print("fps:",fps)
        # width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # 一定要转int 否则是浮点数
        # height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        # size = (width, height)  # 大小
        # # fourcc = cv2.VideoWriter_fourcc('I', '4', '2', '0')
        # # self.out = cv2.VideoWriter('123asd.avi', fourcc, fps, size)  # 初始化文件写入 文件名 编码解码器 帧率 文件大小
        #
        # fourcc = cv2.VideoWriter_fourcc('X','V','I','D')
        # self.out = cv2.VideoWriter('output.avi', fourcc, fps, (640, 480))

        print("s_flag:", S_flag)


    def stop_save_video(self):
        global Out, S_flag
        if S_flag == 1:
            S_flag = 0
            self.label_4.setText(" 录像停止")
            print("停止录像")
            time.sleep(1)
            Out.release()

    # def show_camera(self):
    #
    #     flag, self.image = self.cap.read()
    #
    #     self.image = cv2.flip(self.image, 1)  # 左右翻转
    #     #show = cv2.resize(self.image, (480, 320))
    #     show = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
    #     showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
    #     self.labelShowCamera.setPixmap(QtGui.QPixmap.fromImage(showImage))
    #     self.labelShowCamera.setScaledContents(True)

    def show_camera(self):
        global g_img, Cap
        self.count_time += 1
        #print("count_time", self.count_time)
        success, g_img = Cap.read()
        g_img = cv2.cvtColor(g_img, cv2.COLOR_BGR2RGB)
        qimg = qimage2ndarray.array2qimage(g_img)
        self.labelShowCamera.setPixmap(QPixmap(qimg))
        self.labelShowCamera.show()

    
    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
    
    @pyqtSlot(int)
    def on_horizontalScrollBar_valueChanged(self, value):
        """
        Slot documentation goes here.
        
        @param value DESCRIPTION
        @type int
        """
        # TODO: not implemented yet
        self.frame.move(self.x - self.horizontalScrollBar.value(), 0)
    
    @pyqtSlot()
    def on_pushButton_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        # eeg_receiveData = threading.Thread(target = callForData.main)
        # eeg_receiveData.setDaemon(True)  # 把子线程t_receiveData设置为守护线程，必须在start()之前设置
        # eeg_receiveData.start()

        self.widget_2.setVisible(True)
        self.widget_2.mpl.start_dynamic_plot()
    
    @pyqtSlot()
    def on_pushButton_4_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.stop_save_video()
    
    @pyqtSlot(str)
    def on_comboBox_activated(self, p0):
        """
        Slot documentation goes here.
        
        @param p0 DESCRIPTION
        @type str
        """
        # TODO: not implemented yet
        self.eeg_com = p0
    
    @pyqtSlot()
    def on_pushButton_5_clicked(self):
        """
        Slot documentation goes here.
        """

        # TODO: not implemented yet
        gl_com._init()
        gl_com.set_value("COM", self.eeg_com)
        print(gl_com.get_value("COM"))
        # t_callEegData = threading.Thread(target = callForData.callfordata)
        # t_callEegData.setDaemon(True)  # 把子线程t_receiveData设置为守护线程，必须在start()之前设置
        # t_callEegData.start()
    
    @pyqtSlot()
    def on_pushButton_6_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        # t_callEegData = threading.Thread(target = callForData.callfordata)
        # t_callEegData.setDaemon(True)  # 把子线程t_receiveData设置为守护线程，必须在start()之前设置
        # t_callEegData.start()

class CameraWorkThread(QThread):

    trigger = pyqtSignal()
    def __init__(self):
        super(CameraWorkThread, self).__init__()

    def run(self):
        global g_img, Cap, Out
        Out = cv2.VideoWriter(filename, Fourcc, Fps, size, True)  # 初始化文件写入 文件名 编码解码器 帧率 文件大小
        #ret, frame = Cap.read()
        while True:
            #cv2.imshow('img', g_img)
            ret, frame = Cap.read()
            if ret == True:
                print("多线程：正在录像")
                #frame = cv2.flip(frame, 1)
                #cv2.imshow("frame", frame)
                Out.write(frame)
            if S_flag == 0:
                break
            if cv2.waitKey(1) & 0xFF == ord('q'):  # 若检测到按键 ‘q’，退出
                break
        self.trigger.emit()

if __name__ == "__main__":
    import sys
    t_receiveData = threading.Thread(target = testredata.main)
    t_receiveData.setDaemon(True)  # 把子线程t_receiveData设置为守护线程，必须在start()之前设置
    t_receiveData.start()
    app = QApplication(sys.argv)
    '''
    启动画面-预先与脑电建立数据传输链接
    '''
    # get_pic(start_png, 'start.png')
    splash = QSplashScreen(QPixmap("start.png"))
    # 设置画面中的文字的字体
    splash.setFont(QFont('Microsoft YaHei UI', 12))
    # 显示画面
    splash.show()
    # 显示信息
    splash.showMessage("程序初始化中... 0%", QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom, QtCore.Qt.black)
    time.sleep(2)  # 模拟运算的时间
    splash.showMessage("加载配置...30%", QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom, QtCore.Qt.black)
    time.sleep(2)  # 模拟运算的时间
    splash.showMessage("加载配置...60%", QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom, QtCore.Qt.black)
    time.sleep(1)  # 模拟运算的时间
    splash.showMessage("加载配置...90%", QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom, QtCore.Qt.black)
    time.sleep(1)
    splash.showMessage("加载配置...100%", QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom, QtCore.Qt.black)
    time.sleep(10)  # 必须先获取到数据才能启用界面程序，否则崩溃
    ui = MainWindow()
    ui.setFixedSize(1745,1058)
    ui.setWindowTitle('认知力_V1.0.1')#标题栏
    ui.show()
    CameraWorkThread = CameraWorkThread()
    sys.exit(app.exec_())
