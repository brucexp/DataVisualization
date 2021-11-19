import sys, math,os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtCore
class DashBoard:

    def __init__(self):
        self.set_ui()
        self.setQTimer()  # 开一个定时器来进行自动旋转演示

    '''
    UI初始化程序
    '''
    def set_ui(self):
        #获取当前路径的上一路径
        self.path =os.path.dirname(os.getcwd())#取当前目录上一级目录
        print(self.path)
        # 创建无边框程序
        #self.setWindowFlags(Qt.FramelessWindowHint)

        #创建一个速度指针
        self.set_speedpointer()

    def setQTimer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.angle = 0
        self.timer.start(50)

    def set_background_painter(self):
        global Count
        painter = QPainter(self)
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        # __path = self.path+'/car/pic/仪表盘2.png'
        # self.playdashboard = QPixmap(__path)
        # print("dash_board:",self.playdashboard.width())
        #1024,500为窗口大小
        yibiaopan_x = self.label.x()
        yibiaopan_y = self.label.y()
        yibiaopan_width = self.label.width()
        yibiaopan_height = self.label.height()
        #print(yibiaopan_x,yibiaopan_y,yibiaopan_width,yibiaopan_height)
        dashboard = QPixmap()
        dashboard.load('D:/testpyqt5/car/pic/仪表盘2.png')
        #print("dashboard :", dashboard.size())
        if Count > 0:
            painter.drawPixmap(yibiaopan_x, 140, 196, 90, dashboard)
        if Count > 0:
            painter.drawPixmap(yibiaopan_x + yibiaopan_width, yibiaopan_y, 196, 90, dashboard)

        # size = self.geometry()
        # print("size:", size)

        painter.end()