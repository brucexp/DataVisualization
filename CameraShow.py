# -*- coding: utf-8 -*-

"""
Module implementing CameraShow.
"""
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
import cv2
import VideoRecod
import sys
import time
from Ui_renjigongxiao import Ui_MainWindow


class CameraShow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (defaults to None)
        @type QWidget (optional)
        """
        super(CameraShow, self).__init__(parent)
        self.timer_camera = QtCore.QTimer()  # 定时器
        self.cap = cv2.VideoCapture()  #初始化摄像头
        self.CAM_NUM = 0
        self.setupUi(self)
        self.slot_init() # 设置部分槽函数
    
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
        VideoRecod.videoCapture(self.CAM_NUM)
        self.timer_camera.start(30)
        self.slot_init()

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
        flag = self.cap.open(self.CAM_NUM)
        if flag == False:
            msg = QtWidgets.QMessageBox.warning(
                 self, u"Warning", u"请检测相机与电脑是否连接正确",
                buttons=QtWidgets.QMessageBox.Ok,
                defaultButton=QtWidgets.QMessageBox.Ok)
        else:
            self.timer_camera.start(30)
        self.buttonOpenCamera.setText('关闭摄像头')

    # 关闭摄像头
    def closeCamera(self):
        self.timer_camera.stop()
        self.cap.release()
        self.labelShowCamera.clear()
        self.buttonOpenCamera.setText('打开摄像头')

    def show_camera(self):

        flag, self.image = self.cap.read()

        self.image = cv2.flip(self.image, 1)  # 左右翻转
        #show = cv2.resize(self.image, (480, 320))
        show = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
        self.labelShowCamera.setPixmap(QtGui.QPixmap.fromImage(showImage))
        self.labelShowCamera.setScaledContents(True)

# True    def main(self):
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = CameraShow()
    ui.show()
    sys.exit(app.exec_())