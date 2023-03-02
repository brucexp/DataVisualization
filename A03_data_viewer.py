import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
# import memcache
import time
from matplotlib.ticker import MultipleLocator
from multiprocessing import Process
# shared = memcache.Client(['127.0.0.1:11211'], debug=True)




def plot_emg(index=None):
  '''eg: index=[1,2,3]'''
  def init():
    axs[0].set_title('emg_data')
    for ii in range(axs.shape[0]):
      axs[ii].set_ylim(-60, 60)
      axs[ii].set_xlim(0, T)
      axs[ii].set_ylabel(index[ii])

    for line in lines:
      line.set_data([], [])
    return lines

  def amimate(i):
    emg_filter = shared.get('emg_filter')
    if emg_filter is None:
      for ii in range(axs.shape[0]):
        lines[ii].set_data(1, 2)
      print('emg_filter is None, waiting for data')
      return lines

    for ii in range(axs.shape[0]):
      lines[ii].set_data(range(T), emg_filter[:, index[ii]])

    return lines


  emg_filter = shared.get('emg_filter')
  T, N = emg_filter.shape[0],emg_filter.shape[1]

  if index is None:
    index = range(0,emg_filter.shape[1])
    fig, axs = plt.subplots(N, 1)
  else:
    fig, axs = plt.subplots(len(index), 1)


  lines = []
  for ii in range(axs.shape[0]):
    lines.append(axs[ii].plot([], [])[0])

  ani = animation.FuncAnimation(fig, amimate, init_func=init, blit=True, interval=5, repeat=False)
  plt.show()

def plot_emgfeat(index=None):
  '''eg: index=[1,2,3]
  此函数只画emg和eeg， 不画每个通道对应的阈值分割线
  适用于想查看所有通道的feature
  '''
  def init():
    axs[0].set_title('emg_feat')
    k=0
    for ii in index:
      axs[k].set_ylim(0, 100)
      axs[k].set_xlim(0, T)
      axs[k].set_ylabel(ii)
      k=k+1

    if useEEG == True:
      axs[k].set_xlim(0, eegAttention.shape[0])
      axs[k].set_ylim(0, 100)
      axs[k].set_ylabel('EEG')
    else:
      axs[k].set_xlim(0, T)
      axs[k].set_ylim(0, 100)
      axs[k].set_ylabel('emgSUM')

    for line in lines:
      line.set_data([], [])
    return lines

  def amimate(i):
    emgrms = shared.get('emgrms') #N*T ndarry。 EMG对应的 RMS信号。一行是一个通道的数据
    eegdata = shared.get('eeg_attention')
    RMS = np.sum(emgrms[index, :], axis=0)
    if emgrms is None:
      for ii in range(axs.shape[0]):
        lines[ii].set_data(1, 2)
      print('emg_filter is None, waiting for data')
      return lines

    k=0
    for ii in index:
      lines[k].set_data(range(T), emgrms[ii])
      k+=1

    if useEEG == True:
      eegAttention = np.array(eegdata)[:, 1]
      lines[k].set_data(range(eegAttention.shape[0]),eegAttention)
    else:
      lines[k].set_data(range(T), RMS)

    return lines


  emgrms = shared.get('emgrms')
  useEEG = shared.get('useEEG')
  eegdata = shared.get('eeg_attention')
  if useEEG == True:
    eegAttention = np.array(eegdata)[:, 1]
  N, T = emgrms.shape[0],emgrms.shape[1]

  if index is None:
    index = range(N)

  plt.figure(2)
  fig, axs = plt.subplots(len(index)+1, 1)

  lines = []
  for ii in range(axs.shape[0]):
    lines.append(axs[ii].plot([], [])[0])

  ani = animation.FuncAnimation(fig, amimate, init_func=init, blit=True, interval=1, repeat=False)
  plt.show()

def plot_emg_rms_feat(index=None):
  '''eg: index=[1,2,3]'''
  def init():
    fig.suptitle('emg_feature')
    # axs[0].set_title('emg_feature')
    k=0
    for ii in index:
      axs[k].set_ylim(0, 100)
      axs[k].set_xlim(0, T)
      axs[k].set_ylabel(label[k])
      k=k+1

    if useEEG == True:
      axs[k].set_xlim(0, eegAttention.shape[0])
      axs[k].set_ylim(0, 100)
      axs[k].set_ylabel('EEG')
    else:
      axs[k].set_xlim(0, T)
      axs[k].set_ylim(0, 100)
      axs[k].set_ylabel('emgSUM')

    for line in lines:
      line.set_data([], [])
    return lines

  def amimate(i):
    emgrms = shared.get('emgrms') #N*T ndarry。 EMG对应的 RMS信号。一行是一个通道的数据
    eegdata = shared.get('eeg_attention')
    y_thr = shared.get('y_thr')  ##N*T ndarry(bool)。大小是True的位置即是潜在活动段位置。
    thr = shared.get('thr')  ##(N,) ndarry。 各通道对应的阈值
    emgThr = shared.get('emgThr')  ###list  长度是用于肌电的传感器个数，等于len(index)
    rmsThr = shared.get('rmsThr')  ##int整数
    RMS = np.sum(emgrms[index, :], axis=0)
    if emgrms is None:
      for ii in range(axs.shape[0]):
        lines[ii].set_data(1, 2)
      print('emg_filter is None, waiting for data')
      return lines

    k,num=0,0
    for ii in index:
      lines[k].set_data(range(T), emgrms[ii])
      k += 1
      lines[k].set_data(range(T), thr[ii] * y_thr[ii])
      k+=1
      lines[k].set_data(range(T), [emgThr[num]]*T)
      k += 1
      num+=1

    if useEEG == True:
      eegAttention = np.array(eegdata)[:, 1]
      lines[k].set_data(range(eegAttention.shape[0]),eegAttention)
      k+=1
      lines[k].set_data(range(eegAttention.shape[0]), [eegThr] * eegAttention.shape[0])
    else:
      lines[k].set_data(range(T), RMS)
      k+=1
      lines[k].set_data(range(T), [rmsThr] * emgrms.shape[1])


    return lines


  emgrms = shared.get('emgrms')
  useEEG = shared.get('useEEG')
  eegdata = shared.get('eeg_attention')
  eegThr = shared.get('eegThr')
  N, T = emgrms.shape[0],emgrms.shape[1]
  label = ['outer', 'fist', 'inner']
  if index is None:
    index = range(N)

  if useEEG == True:
    eegAttention = np.array(eegdata)[:, 1]
  fig, axs = plt.subplots(len(index)+1, 1)
  lines = []
  ####------每个子图增加3条曲线
  for ii in range(axs.shape[0]):
    lines.append(axs[ii].plot([], [])[0])
    lines.append(axs[ii].plot([], [])[0])
    lines.append(axs[ii].plot([], [])[0])

  ani = animation.FuncAnimation(fig, amimate, init_func=init, blit=True, interval=1, repeat=False)
  plt.show()

def plot_gmean(index=None):
  '''eg: index=[1,2,3]'''
  def init():
    fig.suptitle('g_mean data')
    axs[0][0].set_title('x')
    axs[0][1].set_title('y')
    axs[0][2].set_title('z')
    for ii in range(axs.shape[0]):
      axs[ii][0].set_ylabel('channel '+str(index[ii]))
      for jj in range(axs.shape[1]):
        axs[ii][jj].set_ylim(-90, 90)
        axs[ii][jj].set_xlim(0, T)
        ymajorLocater = MultipleLocator(20)
        axs[ii][jj].yaxis.set_major_locator(ymajorLocater)
        axs[ii][jj].set_yticklabels(["$-14$","$-12$","$-9$","$-6$","$-3$","$0$","$3$","$6$","$9$","$12$"])


    for line in lines:
      line.set_data([], [])
    return lines

  def amimate(i):
    g_mean = shared.get('g_mean')  ## 通道*T, 详细：[[xN;yN;zN], T] 先N行x的数据,再n行y,再N行z
    k=0
    for ii in index:
      lines[k].set_data(range(T), g_mean[ii])
      k+=1
      lines[k].set_data(range(T), g_mean[ii+N])
      k+=1
      lines[k].set_data(range(T), g_mean[ii+2*N])
      k+=1

    return lines

  g_mean = shared.get('g_mean')  ## 通道*T, 详细：[[xN;yN;zN], T] 先N行x的数据,再n行y,再N行z

  T = g_mean.shape[1]
  N = int(g_mean.shape[0] / 3)##传感器个数
  if index is None:
    index = range(0,N)

  fig, axs = plt.subplots(len(index), 3)

  lines = []
  for ii in range(axs.shape[0]):
    for jj in range(axs.shape[1]):
      lines.append(axs[ii][jj].plot([], [])[0])

  ani = animation.FuncAnimation(fig, amimate, init_func=init, blit=True, interval=1, repeat=False)
  plt.show()

def plot_g(index=None):
  '''eg: index=[1,2,3]'''
  def init():
    fig.suptitle('g_raw data')
    axs[0][0].set_title('x')
    axs[0][1].set_title('y')
    axs[0][2].set_title('z')
    for ii in range(axs.shape[0]):
      axs[ii][0].set_ylabel('channel '+str(index[ii]))
      for jj in range(axs.shape[1]):
        axs[ii][jj].set_ylim(-90, 90)
        axs[ii][jj].set_xlim(0, T)
        ymajorLocater = MultipleLocator(20)
        axs[ii][jj].yaxis.set_major_locator(ymajorLocater)
        axs[ii][jj].set_yticklabels(["$-14$","$-12$","$-9$","$-6$","$-3$","$0$","$3$","$6$","$9$","$12$"])


    for line in lines:
      line.set_data([], [])
    return lines

  def amimate(i):
    gx = shared.get('gx')  ## T*通道,
    gy = shared.get('gy')
    gz = shared.get('gz')
    k=0
    for ii in index:
      lines[k].set_data(range(T), gx[:,ii])
      k+=1
      lines[k].set_data(range(T), gy[:,ii])
      k+=1
      lines[k].set_data(range(T), gz[:,ii])
      k+=1

    return lines

  gx = shared.get('gx')  ## T*通道,
  gy = shared.get('gy')
  gz = shared.get('gz')
  T = gx.shape[0]
  N = gx.shape[1]##传感器个数
  if index is None:
    index = range(0,N)

  fig, axs = plt.subplots(len(index), 3)

  lines = []
  for ii in range(axs.shape[0]):
    for jj in range(axs.shape[1]):
      lines.append(axs[ii][jj].plot([], [])[0])

  ani = animation.FuncAnimation(fig, amimate, init_func=init, blit=True, interval=1, repeat=False)
  plt.show()

def plot_a(index=None):
  '''eg: index=[1,2,3]'''
  def init():
    fig.suptitle('a_raw data')
    axs[0][0].set_title('x')
    axs[0][1].set_title('y')
    axs[0][2].set_title('z')
    for ii in range(axs.shape[0]):
      axs[ii][0].set_ylabel('channel '+str(index[ii]))
      for jj in range(axs.shape[1]):
        axs[ii][jj].set_ylim(-130, 130)
        axs[ii][jj].set_xlim(0, T)


    for line in lines:
      line.set_data([], [])
    return lines

  def amimate(i):
    ax = shared.get('ax')## T*通道,
    ay = shared.get('ay')
    az = shared.get('az')
    k=0
    for ii in index:
      lines[k].set_data(range(T), ax[:,ii])
      k+=1
      lines[k].set_data(range(T), ay[:,ii])
      k+=1
      lines[k].set_data(range(T), az[:,ii])
      k+=1

    return lines

  gx = shared.get('ax')  ## T*通道,
  T = gx.shape[0]
  N = gx.shape[1]##传感器个数
  if index is None:
    index = range(0,N)

  fig, axs = plt.subplots(len(index), 3)

  lines = []
  for ii in range(axs.shape[0]):
    for jj in range(axs.shape[1]):
      lines.append(axs[ii][jj].plot([], [])[0])

  ani = animation.FuncAnimation(fig, amimate, init_func=init, blit=True, interval=1, repeat=False)
  plt.show()

# plot_a(index=None)
# plot_gmean(index=[0,3])
# plot_emg()
#
# plot_emg_rms_feat(index=[0,1,2])

if __name__=='__main__':
    print('data viewer is runing')
    p1=Process(target=plot_emg)
    p1.start()
    p2 = Process(target=plot_gmean,args=[[0,3],])
    p2.start()
    p3 = Process(target=plot_emg_rms_feat,args=[[0,1,2],])
    p3.start()
    # p4 = Process(target=plot_g,args=[[0,3],])
    # p4.start()
    # p5 = Process(target=plot_a)
    # p5.start()