from django_filters import FilterSet
from django_filters import filters
from dsrt.models import ImageData
from scipy.interpolate import interp1d
import random
import matplotlib.dates as mdates
from astropy.io import fits
from threading import Thread
from pylab import *
import datetime
import matplotlib.ticker as ticker
import base64
import os
import cv2

def getQuickLookImage(project_filename,spec_filename, start_time, end_time):
    
    # 读取文件并生成quicklook图片
     
    path1 = r'/home/gytide/dsrtprod/data/2023/03/project_image/PRO20230301.fits'#投影文件的路径
    path2 = r'/home/gytide/dsrtprod/data/2023/03/speview/SPE20220301.fits' #频谱概图的路径

    hdu1 = fits.open(path1)
    hdu2 = fits.open(path2)
    fig = gen1Dimg(hdu1, hdu2, start_time, end_time, time_resolved=time_resolved)

def gen1Dimg(data, start_times=None, end_times=None):
    '''
     参数: ewdata : EW方向投影的文件
          sndata : SN方向投影的文件
          start_time : 起始时间  "09:50:00"
          start_time : 结束时间  "10:50:00"
          time_resolved : 时间分辨率 默认时设置为 1 秒 (步长为1)
     返回: <matplotlib.figure.Figure>  fig 可以直接 savefig() 为图片
    '''

    # 设置零点
    dtime0 = datetime.datetime.strptime("00:00:00", "%H:%M:%S")
    start_time = None
    end_time = None

    # 时间转换，由字符串转换为毫秒数
    if (start_times != None):
        start_time = datetime.datetime.strptime(start_times, "%H:%M:%S")
        start_time = int(format((start_time - dtime0).seconds)) * 1000

    if (end_times != None):
        end_time = datetime.datetime.strptime(end_times, "%H:%M:%S")
        end_time = int(format((end_time - dtime0).seconds)) * 1000

    hdu = data

    # 未赋值或超出范围的设为边界值
    # 为不合法数据设置默认值
    if (start_time == None or start_time > hdu[1].data['time'][-1] or start_time < hdu[1].data['time'][0]):
        start_time = hdu[1].data['time'][0]
    if (end_time == None or end_time > hdu[1].data['time'][-1] or end_time < hdu[1].data['time'][0]):
        end_time = hdu[1].data['time'][-1]

    # 读出概图的成像数据
    # 1
    dataRL1 = hdu[0].data
    timeData1 = hdu[1].data['time']


    # 裁减坐标

    index1 = np.where(timeData1 >= start_time)[0][0]
    index2 = np.where(timeData1 >= end_time)[0][0]

    # 根据时间分辨率生成切割步长（成像概图数据 1秒 1格）

    time_interval = 20


    # 裁切投影图
    dataRL1 = dataRL1[:, index1:index2 + 1:time_interval]

    # 数据取反 测试
    #

    dataRL1 = -dataRL1

    timeData1 = timeData1[index1:index2 + 1:time_interval]


    # 读入日期,设置时间起点
    datess = hdu[0].header['DATE-OBS']
    dtime0 = datetime.datetime.strptime("00:00:00", "%H:%M:%S")

    fig, axs = plt.subplots(2, 1, figsize=(10.0, 8.0), dpi=102.4)

    # ####################################################
    ax1 = axs[0]
    # 设置坐标
    # 设置时间轴范围
    trang1 = dtime0 + datetime.timedelta(seconds=timeData1[0] / 1000)
    trang2 = dtime0 + datetime.timedelta(seconds=timeData1[-1] / 1000)
    ax1.set_ylabel('Pixel')
    ax1.set_title("DSRT Radio 1D project EW" + ' ' + datess)
    ax1.set_xlim([trang1, trang2])
    ax1.set_ylim([0, dataRL1.shape[0]])
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    ax1.xaxis.set_minor_locator(mdates.MinuteLocator())
    ax1.yaxis.set_minor_locator(MultipleLocator(10))
    # ax1.yaxis.set_minor_locator(MultipleLocator(10))

    ax1in1 = ax1.inset_axes([0.0, 0.0, 1, 1])
    # 使用minmax归一化
    psm1 = ax1in1.pcolormesh(dataRL1, vmin=np.min(dataRL1) * 0.5, cmap='hot', vmax=np.max(dataRL1) * 0.5,
                             rasterized=True)
    ax1in1.axis('off')
    # color bar

    minv = 4.0
    maxv = 8.0
    bar1 = fig.colorbar(psm1, ax=ax1)
    bar1.ax.text(1, maxv + (maxv - minv) / 100, 'dB')
    return fig
