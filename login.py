# -*- coding: utf-8 -*-

"""
Module implementing Login.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox


from Ui_login import Ui_Form
from CameraShow import CameraShow
from renjigongxiao import MainWindow
PassWord = "aptx4869"
Username = "admin"

class Login(QWidget, Ui_Form):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (defaults to None)
        @type QWidget (optional)
        """
        super(Login, self).__init__(parent)
        self.setupUi(self)
        self.passwordLineEdit.editingFinished.connect(self.openMain) # 输入密码后按回车键执行登录操作
    
    @pyqtSlot()
    def on_loginButton_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.openMain()

    def openMain(self):
        global PassWord, Username
        password = self.passwordLineEdit.text()
        username = self.nameLineEdit.text()
        if password != "" and username != "":
            if password == PassWord and username == Username:
                self.mainWindow = MainWindow() # 创建主窗体对象
                self.mainWindow.show()
                lg.hide()
            else:
                self.nameLineEdit.setText("") # 清空用户名文本
                self.passwordLineEdit.setText("") # 清空密码文本框
                QMessageBox.warning(None, '警告', '请输入正确的用户名和密码！', QMessageBox.Ok)
        else:
            QMessageBox.warning(None, '警告', '请输入用户名和密码！', QMessageBox.Ok)
    
    @pyqtSlot()
    def on_checkBox_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.nameLineEdit.setText(Username)
    
    @pyqtSlot(str)
    def on_label_linkActivated(self, link):
        """
        Slot documentation goes here.
        
        @param link DESCRIPTION
        @type str
        """
        # TODO: not implemented yet
        QMessageBox.warning(None, '警告', '请输入用户名和密码！', QMessageBox.Ok)

if __name__ == "__main__":
    import sys
    app1 = QApplication(sys.argv)
    app1.setWindowIcon(QIcon('D:/testpyqt5/renjigongxiao/jsq.ico'))
    lg = Login()
    lg.setWindowTitle('登录系统')
    lg.setWindowFlags(QtCore.Qt.MSWindowsFixedSizeDialogHint)  # 只显示最小化和关闭按钮
    #lg.status = lg.statusBar()
    #lg.status.showMessage('欢迎系统')
    lg.show()
    sys.exit(app1.exec_())