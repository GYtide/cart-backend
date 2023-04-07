from django_filters import FilterSet
from django_filters import filters
from dsrt.models import ImageData
from scipy.interpolate import interp1d
import random
import matplotlib.dates as mdates
from astropy.io import fits
from threading import Thread
from pylab import *
from datetime import datetime
import matplotlib.ticker as ticker
import base64
import os
from datetime import timedelta
import matplotlib.cm as mplcm
from matplotlib.ticker import MultipleLocator
import cv2
import redis
import json
import numpy as np
from proto import frame_pb2

# redis连接池
redis_connection_pool = redis.ConnectionPool(
    host='localhost',
    port=6379,
    db=0,
    decode_responses=False
)


def compress_matrix(timearr,spearr,matrix, max_elements):
    """
    对给定的矩阵进行间隔采样，使其元素数量不超过指定的最大值。
    
    参数：
    matrix -- 要进行采样的矩阵
    max_elements -- 最大的元素数量
    
    返回值：
    采样后的矩阵
    """
    # 获取矩阵的形状和元素数量
    lay,rows, cols = matrix.shape
    num_elements = rows * cols
    
    # 计算采样间隔
    interval = int(np.ceil(np.sqrt(num_elements / max_elements)))
    
    # 采样矩阵
    compressed_matrix = matrix[:,::interval, ::interval]
    timearr = timearr[::interval]
    spearr = spearr[::interval]
    
    return [timearr,spearr,compressed_matrix]

def spe_merge(fitslist):

    timeArray = np.array([])
    speArray = np.array([])
    dataArray = np.zeros((0,0,0))

    for fitsfile in fitslist:
        with fits.open(fitsfile) as hdulist:
            data = hdulist[0].data  # 读取 SPE 文件中的 data 数组
            time = hdulist[1].data['TIME'][0]  # 读取 SPE 文件中的 time
            frequency = hdulist[1].data['frequency'][0]  # 读取 SPE 文件中的 frequency

            timeArray = np.concatenate((timeArray, time))
        
            if speArray.size == 0:  
                speArray = np.concatenate((speArray, frequency))
            if dataArray.size == 0:
                dataArray = data
            else:
                dataArray = np.concatenate((dataArray,data),axis=2)
                

    return compress_matrix(timeArray,frequency,dataArray,400000)


# 在 tx 中找出 t1 t2的索引


def findindex(tx, t1, t2):
    '''


    Parameters
    ----------
    tx : TYPE
        DESCRIPTION.
    t1 : TYPE
        DESCRIPTION.
    t2 : TYPE
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.
    types : 数据状态
        000 = 0  时间范围内无数据；
        010 = 2  观测时间范围内有数据，在观测时间段中；
        101 = 5  查询时间段内 包含观测数据；
        001 = 1  查询时间内，刚开始时间，无数据，结束时间有数据；
        100 = 4  查询时间段内，开始段，有数据，结束段，无数据；

    '''
    index1 = []
    index2 = []
    types = 0
    if t1 >= t2:
        print('t1 >= t2 is wrong!')
        return [], [], types
    else:
        if t1 >= tx[-1]:
            print('t1 {:f} > tx[-1] {:f}'.format(t1, tx[-1]))
            return [], [], types
        if t2 <= tx[0]:
            print('t2 {:f} < tx[0] {:f}'.format(t2, tx[0]))
            return [], [], types
        else:
            index = np.where(tx <= t1)
            if len(index[0]) > 0:
                types = 4
                index1 = [index[0][-1]]
            else:
                print('t1 < tx !!')
                types = 1
                index1 = [0]

            index = np.where(tx >= t2)
            if len(index[0]) > 0:
                index2 = [index[0][0]]
                if types == 4:
                    types = 2
            else:
                print('t2 > tx !!')
                index2 = [len(tx)-1]
                if types == 1:
                    types = 5
            return index1, index2, types

#### end findindex ##################


class Rimg1Dsyn():
    def __init__(self, fn):
        self.file = fn

    def readdata(self):
        hdu = fits.open(self.file)
        self.dirs = hdu[0].header['dirs']
        if self.dirs[0:2] == 'EW':
            self.yy = np.ravel(hdu[1].data[0]['sunx'])
        elif self.dirs[0:2] == 'NS':
            self.yy = np.ravel(hdu[1].data[0]['suny'])
        self.tt = np.ravel(hdu[1].data['time'])
        self.freq = hdu[0].header['freq']
        self.img = hdu[0].data
        self.polss = hdu[0].header['POLARIZA']
        self.dateobs = hdu[0].header['DATE_OBS'][0:10]
        self.datet0 = datetime.fromisoformat(self.dateobs + 'T00:00:00')
        hdu.close()

    def getdatat(self, t1, t2):
        index1, index2, types = findindex(self.tt, t1, t2)
        missvalue = 256
        if types > 0:
            xdatax = self.img[:, index1[0]: index2[0] + 1]
            xtt = self.tt[index1[0]: index2[0] + 1]
            if types == 1:
                # 前面无数据，后面有数据
                t1a = np.ones((len(self.yy), 1)) * missvalue
                xdatax = np.hstack((t1a, xdatax))
                xtt = np.hstack((t1, xtt))
            elif types == 4:
                # 前面有数据，后面无数据
                t2b = np.ones((len(self.yy), 1)) * missvalue
                xdatax = np.hstack((xdatax, t2b))
                xtt = np.hstack((xtt, t2))
            elif types == 5:
                t1a = np.ones((len(self.yy), 1)) * missvalue
                t2b = np.ones((len(self.yy), 1)) * missvalue
                xdatax = np.hstack((t1a, xdatax, t2b))
                xtt = np.hstack((t1, xtt, t2))
            tg, yg = np.meshgrid(xtt, self.yy)

        else:
            tg, yg = np.meshgrid(np.array([t1, t2]), self.yy)
            xdatax = tg * 0.0 + missvalue
        self.ttg = tg
        self.yyg = yg
        self.xdata = xdatax
        # return tg, yg, xdata

    def plot_img1D(self, minv=0, maxv=255, newcmp='gray', figsize=(10, 4)):
        shading = 'flat'
        jcmap = mplcm.get_cmap(newcmp).copy()
        jcmap.set_over(color='w')
        trange1 = self.datet0 + \
            timedelta(milliseconds=int(self.ttg[0, 0] * 1000))
        trange2 = self.datet0 + \
            timedelta(milliseconds=int(self.ttg[0, -1] * 1000))

        self.fig, self.axs = plt.subplots(1, 1, figsize=figsize)
        ax1 = self.axs
        ax1.set_xlabel('Time (UT)')
        ax1.set_ylabel(self.dirs[0:2] + ' (arcsec)')

        ax1.set_title("CART Radio 1D Image " +
                      '{:3.0f}MHz '.format(self.freq) + self.polss + ' ' + self.dateobs)
        ax1.set_xlim([trange1, trange2])
        ax1.set_ylim([self.yyg[0, 0], self.yyg[-1, 0]])
        # ax.xticks(rotation=70)
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        # ax1.xaxis.set_minor_locator(mdates.MinuteLocator())
        # ax1.yaxis.set_major_locator(MultipleLocator(5))
        ax1.yaxis.set_minor_locator(MultipleLocator(10))
        ax1in1 = ax1.inset_axes([0.0, 0.0, 1, 1], zorder=1)
        if shading == 'flat':
            self.xdata[:, -2] = self.xdata[:, -1]
            self.xdata = self.xdata[:-1:, :-1:]
        psm1 = ax1in1.pcolormesh(self.ttg, self.yyg, self.xdata,
                                 vmin=minv, vmax=maxv, cmap=jcmap, shading=shading, rasterized=True)
        ax1in1.axis('off')
        return self.fig


class RspecSyn():
    def __init__(self, fn):
        self.file = fn

    def readdata(self):
        # 依赖于数据格式；
        hdu = fits.open(self.file)

        self.tt = np.ravel(hdu[1].data['time'])
        self.freq = np.ravel(hdu[1].data['frequency'])
        self.img = hdu[0].data
        self.polss = hdu[0].header['POLARIZA']
        self.dateobs = hdu[0].header['DATE_OBS'][0:10]
        self.datet0 = datetime.fromisoformat(self.dateobs + 'T00:00:00')
        hdu.close()

    def getdatat(self, t1, t2):
        '''


        Parameters
        ----------
        t1 : TYPE
            DESCRIPTION.
        t2 : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        '''
        index1, index2, types = findindex(self.tt, t1, t2)
        missvalue = 256
        if types > 0:
            xdatax = self.img[:, index1[0]: index2[0] + 1]
            xtt = self.tt[index1[0]: index2[0] + 1]
            if types == 1:
                # 前面无数据，后面有数据
                t1a = np.ones((len(self.freq), 1)) * missvalue
                xdatax = np.hstack((t1a, xdatax))
                xtt = np.hstack((t1, xtt))
            elif types == 4:
                # 前面有数据，后面无数据
                t2b = np.ones((len(self.freq), 1)) * missvalue
                xdatax = np.hstack((xdatax, t2b))
                xtt = np.hstack((xtt, t2))
            elif types == 5:
                t1a = np.ones((len(self.freq), 1)) * missvalue
                t2b = np.ones((len(self.freq), 1)) * missvalue
                xdatax = np.hstack((t1a, xdatax, t2b))
                xtt = np.hstack((t1, xtt, t2))
            tg, yg = np.meshgrid(xtt, self.freq)

        else:
            tg, yg = np.meshgrid(np.array([t1, t2]), self.freq)
            xdatax = tg * 0.0 + missvalue
        self.ttg = tg
        self.yyg = yg
        self.xdata = xdatax
        # return tg, yg, xdata

    def plot_specd(self, minv=0, maxv=255, newcmp='jet', figsize=(10, 4)):
        shading = 'flat'
        jcmap = mplcm.get_cmap(newcmp).copy()
        jcmap.set_over(color='w')

        trange1 = self.datet0 + \
            timedelta(milliseconds=int(self.ttg[0, 0] * 1000))
        trange2 = self.datet0 + \
            timedelta(milliseconds=int(self.ttg[0, -1] * 1000))

        self.fig, self.axs = plt.subplots(1, 1, figsize=figsize)
        ax1 = self.axs
        ax1.set_xlabel('Time (UT)')
        ax1.set_ylabel('Frequency (MHz)')

        ax1.set_title("CART Radio Dynamic Spectrum " +
                      self.polss + ' ' + self.dateobs)
        ax1.set_xlim([trange1, trange2])
        ax1.set_ylim([self.yyg[0, 0], self.yyg[-1, 0]])
        # ax.xticks(rotation=70)
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        # ax1.xaxis.set_minor_locator(mdates.MinuteLocator())
        ax1.yaxis.set_minor_locator(MultipleLocator(10))
        ax1in1 = ax1.inset_axes([0.0, 0.0, 1, 1], zorder=1)
        if shading == 'flat':
            self.xdata[:, -2] = self.xdata[:, -1]
            self.xdata = self.xdata[:-1:, :-1:]

        psm1 = ax1in1.pcolormesh(self.ttg, self.yyg, self.xdata,
                                 vmin=minv, vmax=maxv, cmap=jcmap, shading=shading, rasterized=True)
        ax1in1.axis('off')
        return self.fig


# 生成检索快视图
def genQuicklook(fnspec, file1, *fnimg, start_times='2022-01-01T00:00:00', end_times='2022-01-01T00:05:00', time_resolved=None):
    '''


    Parameters
    ----------
    file1 : string
        一维投影 文件名 
    file2 : string
        一维投影 文件名 
    start_times : time string optional
        ''00:00:00''. The default  
    end_times : string optional
       ''00:05:00''. The default  
    time_resolved : TYPE, optional
        DESCRIPTION. The default is None.

    Returns
    -------
    None.

    '''
    # time transpose

    tdate1 = datetime.fromisoformat(start_times)
    tdate2 = datetime.fromisoformat(end_times)
    t0 = datetime.fromisoformat(tdate1.strftime('%Y-%m-%d') + 'T00:00:00')
    t1 = (tdate1 - t0).seconds
    t2 = (tdate2 - t0).seconds

    ###############################
    # 这里需要 考虑输出3个图

    ###########################
    # 频谱检索
    rspec = RspecSyn(fnspec)
    rspec.readdata()
    rspec.getdatat(t1, t2)
    figspec = rspec.plot_specd(figsize=(10, 2))

    ###################################
    rimg = Rimg1Dsyn(file1)
    rimg.readdata()
    rimg.getdatat(t1, t2)
    fig1 = rimg.plot_img1D(figsize=(10, 2))
    figimg = [fig1]
    if len(fnimg) > 0:
        for ii in range(len(fnimg)):
            filei = fnimg[ii][0]
            rimg2 = Rimg1Dsyn(filei)
            rimg2.readdata()
            rimg2.getdatat(t1, t2)
            figimg.append(rimg2.plot_img1D(figsize=(10, 2)))
    return figspec, figimg


def FlowCal(fileList, area):
    redis_con = redis.Redis(connection_pool=redis_connection_pool)

    try:
        for file in fileList:
            hdu = redis_con.hgetall(file)
            if not hdu:
                # 没有缓存，打开文件加入缓存
                # 暂时默认一个文件
                path = r'/home/gytide/dsrtprod/data/2023/03/dsrtimg/ODACH_CART02_SRIM_L2_233MHz_20220417032600_V01.10.fits'
                nhdu = fits.open(path)
                num = 1
                pipe = redis_con.pipeline()
                header = [{}, {}]
                for card in nhdu[0].header.cards:
                    header[0][str(card[0])] = str(card[1])

                for card in nhdu[1].header.cards:
                    header[1][str(card[0])] = str(card[1])

                header_str = json.dumps(header)

                redis_con.hset(
                    'ODACH_CART02_SRIM_L2_233MHz_20220417032600_V01.10.fits', 'header', header_str)
                for data in nhdu[1].data:
                    data_str = str([item.tolist() if isinstance(
                        item, np.ndarray) else item for item in data])
                    redis_con.hset(
                        'ODACH_CART02_SRIM_L2_233MHz_20220417032600_V01.10.fits', num, data_str)
                    num = num + 1
                redis_con.expire(
                    'ODACH_CART02_SRIM_L2_233MHz_20220417032600_V01.10.fits', 180)
                pipe.execute()
                nhdu.close()
                hdu = redis_con.hgetall(file)
            hdu_data = sorted(hdu.items())

            message = frame_pb2.FlowCalAck()
            for btablestr in hdu_data[0:-1]:
                btable = json.loads(btablestr[1])
                time = btable[0]
                stokesi = np.array(btable[2])
                stokesv = np.array(btable[3])
                sunx = np.array(btable[4])
                suny = np.array(btable[5])
                sunxindex = np.where(
                    (sunx >= area[0][0]) & (sunx <= area[0][1]))[0]
                sunyindex = np.where(
                    (suny >= area[1][0]) & (suny <= area[1][1]))[0]
                sun_stokesi = stokesi[np.ix_(sunyindex, sunxindex)]
                sun_stokesv = stokesv[np.ix_(sunyindex, sunxindex)]
                stokesi_sum = np.sum(sun_stokesi)
                stokesv_sum = np.sum(sun_stokesv)
                message.stokesi[time] = stokesi_sum
                message.stokesv[time] = stokesv_sum
            return message
    except Exception as e:
        print(e)
