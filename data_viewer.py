import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import time
from matplotlib.ticker import MultipleLocator
from multiprocessing import Process
import random

from pylsl import StreamInfo, StreamOutlet, resolve_stream, StreamInlet

# streams = resolve_stream('type', 'EMG')
stream_info = StreamInfo('EMG_hangyi', 'EMG', 10, 200, 'float32', 'hangyiwyz')
inlet = StreamInlet(stream_info)

def plot_emg2xk(data = None):
  '''eg: index=[1,2,3]'''
  def init():
    axs.set_title('emg_data')
    axs.set_ylim(0, 60)
    axs.set_xlim(0, T)
    axs.set_ylabel('hahaha')

    lines[0].set_data([], [])
    return lines

  def amimate(i):
    # data= random.sample(range(0,100),10)
    data, timestamp_ = inlet.pull_sample()
    lines[0].set_data(range(T), data)
    return lines


  # T = len(data)
  T = 10
  fig, axs = plt.subplots(1, 1)

  lines = []
  lines.append(axs.plot([], [])[0])

  ani = animation.FuncAnimation(fig, amimate, init_func=init, blit=True, interval=15, repeat=False)
  plt.show()

if __name__=='__main__':
  print('data viewer is runing')
  # data = [0]*10
  plot_emg2xk()
  
  
    # p1=Process(target=plot_emg)
    # p1.start()
    # p2 = Process(target=plot_gmean,args=[[0,3],])
    # p2.start()

    # p4 = Process(target=plot_g,args=[[0,3],])
    # p4.start()
    # p5 = Process(target=plot_a)
    # p5.start()
