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
        ax1.xaxis.set_minor_locator(mdates.MinuteLocator())
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
        ax1.xaxis.set_minor_locator(mdates.MinuteLocator())
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
