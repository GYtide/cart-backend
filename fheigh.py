# -*- coding: utf-8 -*-
"""
Created on Thu Jul  7 11:09:38 2022

@author: micro
"""
import numpy as np
import matplotlib.pyplot as plt
from astropy import constants as const
# import matplotlib.colors as mcolors
import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
# from matplotlib.widgets import LassoSelector#, Cursor
import datetime
from scipy import optimize



def typeIIradioSource(t,f, dates, Nharmset = 2, Nfoldset = 1 ,dens_model = 'Newkirk' ) :
    
    '''
    t 时间偏移量  # seconds
    f 频率选取点  # MHz
    dates 日期 # 如 dates = '2022-08-29'
    Nharmset =1 ，2 ，3 ；； 基频选1 ，谐频选2
    Nfoldset = 1  密度模型的倍数
    
    dens_model = 'Newkirk'  ， 'Saito'  密度模型
    
    
    '''
    
    ## frequency  MHz
    freqx = np.array(f)
    tt = np.array(t)
    
    
    dtime0 = datetime.datetime.fromisoformat( dates + 'T00:00:00' )
    freqs = ' '
    if Nharmset == 1 : freqs = 'Fundamental'
    if Nharmset == 2 : freqs = 'Harmonic'
    if Nharmset == 3 : freqs = 'Third Times'
    
    
    def Newkirkmodel(freqx, Nharm =1, Nfold = 1 ) :
        '''
        Gordon Newkirk JR 1961, ApJ 133, 983
        THE SOLAR CORONA IN ACTIVE REGIONS AND THE THERMAL ORIGIN 
        OF THE SLOWLY VARYING COMPONENT OF SOLAR RADIO RADIATION 
        pp 984 equation(1)
        '''
        ###====
        lgN0 = np.log10(4.2) + 4.0
        
        freqp = freqx / Nharm 
        kk =  ( const.e.value * const.e.value) / ( 4.0 * np.pi * np.pi * const.eps0.value * const.m_e.value)
        
        e_density = freqp * freqp / kk
        
        RR = 4.32 / ( np.log10(e_density ) + 6.0 - np.log10( Nfold) - lgN0 )
        return RR
    
    
    def Saitomodel(freqx,  Nharm =1,  Nfold = 1 ) :
        '''
        Kuniji Saito, et.al., Solar Physics 55(1977) 121-134
        A study of the background corona near solar minimum
        pp 127 equation (4) 
        
        '''
        ###====     
        freqp = freqx / Nharm 
        kk =  ( const.e.value * const.e.value) / ( 4.0 * np.pi * np.pi * const.eps0.value * const.m_e.value)
        
        e_density = freqp * freqp / kk
        c1n = ( 1.36e6, 5.27e6, 3.15e6 ) ## background hole ,polar regions hole
        c2n = (1.68e8, 3.54e6, 1.6e6 )
        d1n = (2.14, 3.3, 4.71 )
        d2n = ( 6.13, 5.8, 3.01)
        ix = 0
        Ne =  e_density  * 1.0e6 / Nfold
        # Ne = c1n[ix] * rx**(-d1n[ix]) + c2n[ix] * rx**(-d2n[ix])
        def Ne2culR( Ne ):
            rx = 3.50
            rx1 = 1.0
            rx2 = 6.0
            ni = 0
            while ni < 100 :
                Nei = c1n[ix] * rx**(-d1n[ix]) + c2n[ix] * rx**(-d2n[ix])
                if abs( Nei - Ne) < Ne/100.0 :
                    break
                if Nei - Ne < 0 :
                    rxi1 = rx1 
                    rx2 = rx
                    
                if Nei - Ne > 0 :
                    rxi1 = rx2  
                    rx1 =rx
    
                rx = (rx + rxi1)/2 
                ni +=1
            return rx
        ##############################
        RR = Ne2culR( Ne )
        return RR
 ##############################################################################3   

    if dens_model == 'Newkirk' :
       RR = Newkirkmodel(freqx, Nharm =Nharmset, Nfold = Nfoldset )
    if dens_model == 'Saito' :
       RR = np.array( [Saitomodel(freqx[ii], Nharm =Nharmset, Nfold = Nfoldset ) for ii in range(len(freqx))])   
    ###   拟合  速度
    Rsunkm = const.R_sun.value / 1000.0  # km
    
    ttx = tt.copy()
    
    def fx_1(x,A,B):
        return A*x + B
    
    def fx_2(x,A,B,C):
        return A * x**2 + B*x + C
    
    A1, B1 = optimize.curve_fit(fx_1, ttx, RR)[0]
    yy1 =  ttx * A1 + B1
    
    A2, B2, C2 = optimize.curve_fit(fx_2, ttx, RR)[0]
    yy2 = A2 * ttx **2 + B2 * ttx + C2
    ### linear velosity fit v1
    v1 = A1 * Rsunkm  ## km /s
    
    v2 = B2 * Rsunkm  ## km /s 
    a2 = A2 * Rsunkm  ## km /s
    
    ##############################################################################
    dt = tt[1] - tt[0]
    #
    trang1 = dtime0 + datetime.timedelta(seconds = np.double( tt[0] - dt ) )
    trang2 = dtime0 + datetime.timedelta(seconds = np.double( tt[-1] + dt) )
    
    ttlist =np.array( [dtime0 + datetime.timedelta(seconds = np.double( tt[ii] ) ) for ii in range(len(tt)) ])
    
    
    fig, ax = plt.subplots(1,1,figsize=(10,8))
    dR = RR[1] - RR[0]
    
    #ax.plot(tt, RR, 'r*')
    
    
    ax.set_title('Shock Height vs time ')
    ax.set_xlabel('Time ('+ dates + ')' )
    
    ax.set_xlim([trang1, trang2])
    ax.xaxis.set_major_formatter( mdates.DateFormatter('%H:%M:%S'))
    ax.xaxis.set_minor_locator(mdates.MinuteLocator())
    
    ax.plot( ttlist,  yy1, 'b')
    ax.plot( ttlist,  yy2, 'g')
    ax.plot( ttlist,  RR, 'r*')
    
    
    ax.set_ylabel('R (Rsun)')
    ax.set_ylim([RR[0] - dR, RR[-1] + dR ])
    
    ss = dens_model+ ' model:  ' +  freqs + ' {:2d} fold model, shock speed {:6.1f} km/s'.format(Nfoldset, v1 )
    ax.text(0.3, 0.9, ss , horizontalalignment='center',
         verticalalignment='center', transform=ax.transAxes)
    
    return fig






## test ## use 
#############################################################################
if __name__ == '__main__':
    t= [0,100,200,300,400]
    f= [300,250,200,180,150]
    
    Nharmset = 2
    Nfoldset = 1
    dates = '2022-02-12'
    
    typeIIradioSource(t,f, dates, Nharmset = 2, Nfoldset = 1 ,dens_model = 'Newkirk')
    # typeIIradioSource(t,f, dates, Nharmset = 2, Nfoldset =2 ,dens_model = 'Saito')
    plt.savefig('plt.png')