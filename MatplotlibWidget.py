import sys
import random
import matplotlib
import threading
matplotlib.use("Qt5Agg")
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QSizePolicy, QWidget
from numpy import arange, sin, pi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import globalvar as gl

#import globavar_eeg as gl_eeg
# from matplotlib.pyplot import hold

#全局变量
# eeg_data = 0


# def receive_eeg_data():
#     global eeg_data
#     streams = resolve_stream('type', 'EEG')
#     inlet = StreamInlet(streams[0])
#     while True:
#         eeg_data, timestamp_ = inlet.pull_sample()



class MyMplCanvas(FigureCanvas):
    """FigureCanvas的最终的父类其实是QWidget。"""
    def __init__(self, parent=None, width=5, height=4, dpi=100):

        # 配置中文显示
        plt.rcParams['font.family'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

        self.fig = Figure(figsize=(width, height), dpi=dpi)  # 新建一个figure
        self.axes = self.fig.add_subplot(4,1,1)  # 建立一个子图，如果要建立复合图，可以在这里修改
        self.bxes = self.fig.add_subplot(4,1,2)  # 建立一个子图，如果要建立复合图，可以在这里修改
        self.cxes = self.fig.add_subplot(4,1,3)  # 建立一个子图，如果要建立复合图，可以在这里修改
        self.dxes = self.fig.add_subplot(4,1,4)  # 建立一个子图，如果要建立复合图，可以在这里修改

        # 给定一个参数，用来标识是不是第一次创建
        self.aline = None
        self.bline = None
        self.cline = None
        self.dline = None
        # 给定一个X轴和Y轴的参数列表，用作后面承载数据
        self.aX = []
        self.aY = []

        self.bX = []
        self.bY = []

        self.cX = []
        self.cY = []

        self.dX = []
        self.dY = []

        #X轴的开始位置，用作后面累加
        self.i = 1

        #self.axes.hold(False)  # 每次绘图的时候不保留上一次绘图的结果

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        '''定义FigureCanvas的尺寸策略，这部分的意思是设置FigureCanvas，使之尽可能的向外填充空间。'''
        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)


    '''绘制静态图，可以在这里定义自己的绘图逻辑'''

    def start_static_plot(self):
        self.fig.suptitle('测试静态图')
        t = arange(0.0, 3.0, 0.01)
        s = sin(2 * pi * t)
        self.axes.plot(t, s)
        self.axes.set_ylabel('静态图：Y轴')
        self.axes.set_xlabel('静态图：X轴')
        self.axes.grid(True)

    '''启动绘制动态图'''

    def start_dynamic_plot(self, *args, **kwargs):
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)  # 每隔一段时间就会触发一次update_figure函数。
        timer.start(250)  # 触发的时间间隔为1秒。

    '''动态图的绘图逻辑可以在这里修改'''
    def update_figure(self):

        self.fig.suptitle('脑电信号原始特征')
        # Build a list of 4 random integers between 0 and 10 (both inclusive)
        # l = [random.randint(0, 10) for i in range(10)]
        # self.axes.cla()
        # self.axes.plot([0,1,2,3,4], l, 'r')
        F3_theta = gl.get_value('F3_theta')
        P3_alpha = gl.get_value('P3_alpha')
        Cz_beta = gl.get_value('Cz_beta')
        P3_beta = gl.get_value('P3_beta')
        # print("---------------画图线程---------------")
        # print(F3_theta,P3_alpha,Cz_beta,P3_beta)
        self.aX.append(self.i)
        self.aY.append(F3_theta)
        self.bX.append(self.i)
        self.bY.append(P3_alpha)
        self.cX.append(self.i)
        self.cY.append(Cz_beta)
        self.dX.append(self.i)
        self.dY.append(P3_beta)
        if self.aline is None:
            # -代表用横线画，g代表线的颜色是绿色，.代表，画图的关键点，用点代替。也可以用*，代表关键点为五角星
            self.aline = self.axes.plot(self.aX, self.aY, '-g', marker='.')[0]
        if self.bline is None:
            self.bline = self.bxes.plot(self.bX, self.bY, '-r', marker='.')[0]
        if self.cline is None:
            self.cline = self.cxes.plot(self.cX, self.cY, '-g', marker='.')[0]
        if self.dline is None:
            self.dline = self.dxes.plot(self.dX, self.dY, '-r', marker='.')[0]

        # 这里插入需要画图的参数，由于图线，是由很多个点组成的，所以这里需要的是一个列表
        self.aline.set_xdata(self.aX)
        self.aline.set_ydata(self.aY)
        self.bline.set_xdata(self.bX)
        self.bline.set_ydata(self.bY)
        self.cline.set_xdata(self.cX)
        self.cline.set_ydata(self.cY)
        self.dline.set_xdata(self.dX)
        self.dline.set_ydata(self.dY)

        # 给表的Y轴位置加上标签，rotation代表让文字横着展示，labelpad代表文字距表格多远了
        self.axes.set_ylabel('F3-theta',rotation=0,labelpad=20)
        self.axes.set_xlabel('时间X')
        self.bxes.set_ylabel('P3-alpha',rotation=0,labelpad=20)
        self.bxes.set_xlabel('时间X')
        self.cxes.set_ylabel('Cz_beta',rotation=0,labelpad=20)
        self.cxes.set_xlabel('时间X')
        self.dxes.set_ylabel('P3-beta',rotation=0,labelpad=20)
        self.dxes.set_xlabel('时间X')

        self.axes.grid(True)
        self.bxes.grid(True)
        self.cxes.grid(True)
        self.dxes.grid(True)

        #当X轴跑了100次的时候，则让X坐标的原点动起来
        if len(self.aX) < 100:
            self.axes.set_xlim([min(self.aX), max(self.aX) + 30])
        else:
            self.axes.set_xlim([self.aX[-80], max(self.aX) * 1.2])
        #加10，防止顶到天花板
        self.axes.set_ylim([min(self.aY), max(self.aY) + 10])

        if len(self.bX) < 100:
            self.bxes.set_xlim([min(self.bX), max(self.bX) + 30])
        else:
            self.bxes.set_xlim([self.bX[-80], max(self.bX) * 1.2])
        self.bxes.set_ylim([min(self.bY), max(self.bY) + 10])

        if len(self.cX) < 100:
            self.cxes.set_xlim([min(self.cX), max(self.cX) + 30])
        else:
            self.cxes.set_xlim([self.cX[-80], max(self.cX) * 1.2])
        self.cxes.set_ylim([min(self.cY), max(self.cY) + 10])

        if len(self.dX) < 100:
            self.dxes.set_xlim([min(self.dX), max(self.dX) + 30])
        else:
            self.dxes.set_xlim([self.dX[-80], max(self.dX) * 1.2])
        self.dxes.set_ylim([min(self.dY), max(self.dY) + 10])

        self.i += 1
        self.draw()

class MatplotlibWidget(QWidget):
    def __init__(self, parent=None):
        super(MatplotlibWidget, self).__init__(parent)
        self.initUi()


    def initUi(self):
        self.layout = QVBoxLayout(self)
        self.mpl = MyMplCanvas(self, width=5, height=4, dpi=100)
        #self.mpl.start_static_plot() # 如果你想要初始化的时候就呈现静态图，请把这行注释去掉
        #self.mpl.start_dynamic_plot() # 如果你想要初始化的时候就呈现动态图，请把这行注释去掉
        self.mpl_ntb = NavigationToolbar(self.mpl, self)  # 添加完整的 toolbar

        self.layout.addWidget(self.mpl)
        self.layout.addWidget(self.mpl_ntb)
        # t_receiveData = threading.Thread(target=receive_eeg_data)
        # t_receiveData.setDaemon(True)  # 把子线程t_receiveData设置为守护线程，必须在start()之前设置
        # t_receiveData.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = MatplotlibWidget()
    # ui.mpl.start_static_plot()  # 测试静态图效果
    ui.mpl.start_dynamic_plot() # 测试动态图效果
    ui.show()
    sys.exit(app.exec_()) 
