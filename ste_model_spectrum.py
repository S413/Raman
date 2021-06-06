# -*- coding: utf-8 -*-
"""
Created on Wed May 13 16:52:29 2020

@author: Stefano rini
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import hilbert, find_peaks
import pylab as p
import scipy.signal as sci
import scipy.stats as stats
# import pymf3
from scipy.optimize import minimize
from scipy.optimize import curve_fit
import math
import scipy
from math import pi

#----------------------------------------------------------------------------
#       FUNCTION TO BE FITTED
#----------------------------------------------------------------------------

def smooth_data(data,win):
    return np.array([np.mean(data[int(np.max([j-win,0])):int(np.min([j+win,data.size]))]) for j in  range(data.size)])

# generalize gaussian with any amplitude
# for the bias, we will remove it from the fitting
def gauss_amp(x_data,beta):
    # beta: 
        # a
        # c
        # sgs    
        M=beta[0]
        c=beta[1]
        sgs=beta[2]
        return [M*math.exp(-(x_data[i]-c)**2/ (2*abs(sgs))) for i in range(x_data.size)]

def gen_lor_amp(x_data,beta):
    # beta: 
        # a
        # c
        # sgs    
        M=beta[0]
        c=beta[1]
        sgs=beta[2]
        d=beta[3]
        return [M/(1+(abs((x_data[i]-c)/sgs))**d) for i in range(x_data.size)]    


def lor_amp(x_data,beta):
    # beta: 
        # a
        # c
        # sgs    
        M=beta[0]
        c=beta[1]
        sgs=beta[2]
        d=2
        return [M/(1+(abs((x_data[i]-c)/sgs))**d) for i in range(x_data.size)]    


def cos_window(t,L,M,R,o,d,al,be):
    
    if t<o:
        out=L    
    elif o<=t & t<o+al:
        out=L+(M-L)/2*(1-np.cos(2*pi*(t-o)/(2*al)))
    elif o+al<=t & t<o+al+d: 
        out=M
    elif o+al+d<= t & t<o+al+d+be:
        out=R+(M-R)/2*(1-np.cos(2*pi*(be-(t-d-o-al))/(2*be)))
    elif t>=o+al+d+be:
        out=R
    else:
        out=0
    return  out


def cos_window2(t,L,M,R,o,al,be):
    
    if t<o:
        out=L    
    elif o<=t & t<o+al:
        out=L+(M-L)/2*(1-np.cos(2*pi*(t-o)/(2*al)))
    elif o+al<= t & t<o+al+be:
        out=R+(M-R)/2*(1-np.cos(2*pi*(be-(t-o-al))/(2*be)))
    elif t>=o+al+be:
        out=R
    else:
        out=0
    return  out

def cos_win(x_data,beta):    
    L=beta[0]
    M=beta[1]
    R=beta[2]
    o=beta[3]
    d=beta[4]
    al=beta[5]
    be=beta[6]
    
    yvec=[cos_window(t,L,M,R,o,d,al,be)  for t in range(x_data.size)]
    return yvec

def cos_win2(x_data,beta):    
    L=beta[0]
    M=beta[1]
    R=beta[2]
    o=beta[3]    
    al=beta[4]
    be=beta[5]
    
    yvec=[cos_window2(t,L,M,R,o,al,be)  for t in range(x_data.size)]
    return yvec

#-----------------------------------------------------------------------------

def positive_mse(y_pred,y_true):                
    loss=np.dot((10**8*(y_pred-y_true>0)+np.ones(y_true.size)).T,(y_pred-y_true)**2)
    return sum(loss)/y_true.size

def pos_mse_loss(beta, X, Y,function):                
    return positive_mse(function(X,beta), Y)


def positive_mse_loss(beta, X, Y):
    p=np.poly1d(beta)
    error = sum([positive_mse(p(X[i]), Y[i]) for i in range(X.size)])/X.size
    return(error)

def reg_positive_mse(y_pred,y_true):                
    loss_pos=(y_pred-y_true)**2
    loss_neg=np.dot((y_pred-y_true<0),(y_pred-y_true)**8)
    loss=loss_pos+loss_neg
    return np.sum(loss)/y_true.size

def reg_pos_loss(beta, X, Y,function):                
    return positive_mse(function(X,beta), Y)


def mse_loss(beta,X, Y,function):
    return sum((function(X,beta)-Y)**2)/Y.size

def find_peak_sym_supp(peak,l_pos,r_pos, win_len_mul, smooth_win, Y):
    # win_len_mul= how much do we extend the window length 
    # smooth_win= how much do we smooth the function
    res=Y.shape[0]
    Y_smooth=smooth_data(Y,smooth_win)

    
    if l_pos==r_pos:
        y_data=Y_smooth[l_pos]
        Y_max=y_data
        Y_max_idx=l_pos
        Y_min=Y_max
    else:
        y_data=Y_smooth[l_pos:r_pos]
        Y_max=np.max(y_data)
        Y_max_idx=l_pos+np.argmax(Y[l_pos:r_pos])        
        Y_min=np.mean(np.sort(y_data)[0:int(y_data.size/10)+1])
            
    l_pos_temp=Y_max_idx-1
    r_pos_temp=Y_max_idx+1
        
    while  Y_smooth[l_pos_temp-1]<=Y_smooth[l_pos_temp]  and l_pos_temp>0:
        l_pos_temp=l_pos_temp-1
    
    while  Y_smooth[r_pos_temp+1]<=Y_smooth[r_pos_temp] and r_pos_temp<res-1: 
        r_pos_temp=r_pos_temp+1
        
    return [l_pos_temp,r_pos_temp]

#-----------------------------------------------------------------------------
# Initialize parameters
#-----------------------------------------------------------------------------

def init_cos(x_data,y_data):
    # order of arguments: M,o,d,al,be
    
    # fix the smoothing window to 3
    y_smoth=smooth_data(y_data,3)
    power=np.dot(y_data,y_data.T)/dim_s
        
    floor_th=0.1*np.sqrt(power)
    # how to define the ceiling of the function
    ceil_th=0.9*np.sqrt(power)    
    
    #  while extending 0 l_win_low /  win_up / l_win_high-r_win_high / win_down / r_win_low-dim_s
    
    l_win_low  = np.argmax(floor_th<y_smoth) 
    r_win_low =x_data.size- np.argmax(floor_th<np.flip(y_smoth) )
    
    
    l_win_high =  np.argmax(ceil_th<y_smoth) 
    r_win_high =x_data.size- np.argmax(ceil_th<np.flip(y_smoth) )    
    
    # L_init=0
    # M_init =ceil_th
    # R_init=0
    # o_init = l_win_low  
    # d_init = r_win_high -l_win_high 
    # al_init= l_win_high-l_win_low  
    # be_init= r_win_low- r_win_high
    
    beta_cos_int=[0, ceil_th, 0, l_win_low, r_win_high -l_win_high, l_win_high-l_win_low, r_win_low- r_win_high]
    
    return beta_cos_int

def init_cos2(x_data,y_data):
    # order of arguments: L,M,R,o,al,be
    
    # fix the smoothing window to 3
    y_smoth=smooth_data(y_data,3)
    power=np.dot(y_data,y_data.T)/y_data.shape[0]
        
    floor_th=0.1*np.sqrt(power)
    
    l_win_low  = np.argmax(floor_th<y_smoth) 
    r_win_low =x_data.size- np.argmax(floor_th<np.flip(y_smoth) )
    
    
    M=np.max(y_data[l_win_low:r_win_low])
    peak_pos=l_win_low+np.argmax(y_data[l_win_low:r_win_low])
                     
    #l_win_high =  np.argmax(ceil_th<y_smoth) 
    #r_win_high =x_data.size- np.argmax(ceil_th<np.flip(y_smoth) )    
    
    # L_init=0
    # M_init =ceil_th
    # R_init=0
    # o_init = l_win_low  
    # al_init= peak_pos-l_win_low  
    # be_init= r_win_low- peak_pos
    
    beta_cos2_int=[0, M, 0, l_win_low, peak_pos-l_win_low, r_win_low- peak_pos]
    
    return beta_cos2_int   

def init_lor(x_data,y_data):
    
    beta_init_lor=np.zeros(4)
    
    # M=beta[0]
    # c=beta[1]
    # sgs=beta[2]
    # d=beta[3]
        
    beta_init_lor[0]=np.max(y_data)
    #center
    beta_init_lor[1]=x_data[np.argmax(y_data)]
    # gamma
    beta_init_lor[2]=(x_data[-1]-x_data[0])/16
    # 
    beta_init_lor[3]=2
    
    return beta_init_lor

#------------------------------------------------------------------------------

# PEAK FINDING

def peaks_cwt_1(data_mean):
    peaks = sci.find_peaks_cwt(data_mean, np.arange(0.001,10)) 
    [ prominences , l_ips, r_ips]=sci.peak_prominences(data_mean, peaks ,wlen=5)
    results_eighty = sci.peak_widths(data_mean, peaks, rel_height=0.8)
    peak_width=results_eighty[0]
    l_ips=(np.floor(results_eighty[2]))
    r_ips=(np.ceil(results_eighty[3]))
    l_ips.astype(int)
    r_ips.astype(int)
    return [peaks, prominences , l_ips, r_ips, peak_width]
    

def peaks_standard(data_mean):
# want to 
    peaks, properties = sci.find_peaks(smooth_data(data_mean,2),prominence=0.00001) 
    prominences=properties['prominences']    
    peak_width=properties['right_bases']-properties['left_bases']
    l_ips=(properties['left_bases'])    
    r_ips=(properties['right_bases'])
    #
    #l_ips=int(properties['left_bases'])    
    #r_ips=int(properties['right_bases'])
    #
    #l_ips.astype(int)
    #r_ips.astype(int)
    return [peaks, prominences , l_ips, r_ips, peak_width]

#----------------------------------------------------------------------
# Remove Estimated florescence
#----------------------------------------------------------------------

def recursive_merge(inter, start_index = 0):
    for i in range(start_index, len(inter) - 1):
        if inter[i][1] > inter[i+1][0]:
            new_start = inter[i][0]
            new_end = inter[i+1][1]
            inter[i] = [new_start, new_end]
            del inter[i+1]
            return recursive_merge(inter.copy(), start_index=i)
    return inter    

def poly4(x_data,beta):
        p=np.poly1d(beta)
        return p(x_data)
        
def positive_mse(y_pred,y_true):                
    loss=np.dot((10**8*(y_pred-y_true>0)+np.ones(y_true.size)).T,(y_pred-y_true)**2)
    return np.sum(loss)/y_true.size

def pos_mse_loss(beta, X, Y,function):                
    return positive_mse(function(X,beta), Y)

def reg_positive_mse(y_pred,y_true):                
    loss_pos=(y_pred-y_true)**2
    loss_neg=np.dot((y_pred-y_true>0),np.abs((y_pred-y_true)))
    loss=loss_pos+loss_neg
    return np.sum(loss)/y_true.size

def reg_pos_mse_loss(beta, X, Y,function):                
    return reg_positive_mse(function(X,beta), Y)

def remove_est_florescence(f_sup,data_sub):
    
    #min_data_amm=np.min(data_sub,axis=1)
    if data_sub.ndim>1:
        min_data_amm=np.mean(data_sub,axis=1)
    else:
        min_data_amm=data_sub
    
    poly_min=np.poly1d(np.polyfit(f_sup,min_data_amm,3))(f_sup)
    poly_min_pos=poly_min+min(min_data_amm-poly_min)
    
    beta_init=np.polyfit(f_sup,min_data_amm,4)
    beta_init[4]=beta_init[4]+min(min_data_amm-poly_min)
    
    #result = minimize(pos_mse_loss, beta_init, args=(f_sup,min_data_amm,poly4), method='Nelder-Mead', tol=1e-12)
    #result = minimize(mse_loss, beta_init, args=(f_sup,min_data_amm,poly4), method='Nelder-Mead', tol=1e-12)
    result = minimize(reg_pos_mse_loss, beta_init, args=(f_sup,min_data_amm,poly4), method='Nelder-Mead', tol=1e-12)
    
    beta_hat = result.x                 
        
    plt_back=1
        
    if plt_back:
            plt.figure('Pos MSE fit')
            #plt.plot(f_sup,np.mean(data_sub,axis=1),'--',label='original data')    
            plt.plot(f_sup,min_data_amm,label='original data')    
            #plt.plot(f_sup,np.mean(data_sub,axis=1),'-.',label='data minus bias')
            plt.plot(f_sup,poly4(f_sup,beta_init),'-.',label='poly 4 init')
            plt.plot(f_sup,poly4(f_sup,beta_hat),'-.',label='poly 4 hat')
            plt.legend()
            
        
    # subtract mean
    
    if data_sub.ndim>1:
        data_sub2=np.subtract(data_sub,poly4(f_sup,beta_hat).reshape([data_sub.shape[0],1]))
    else:
        data_sub2=data_sub-poly4(f_sup,beta_hat)
            
    plt_final=1
    
    if plt_final:
        plt.figure('Final recap')        
        plt.plot(f_sup,poly4(f_sup,beta_hat),'--',label='poly 4 hat')
        plt.plot(f_sup,min_data_amm,label='original data-back')    
        if data_sub.ndim>1:
            plt.plot(f_sup,np.mean(data_sub2,axis=1),label='original data-back-pos_MSE')    
        else:
            plt.plot(f_sup,data_sub2,label='original data-back-pos_MSE')    
        
        plt.legend()
        
    return data_sub2
    
#------------------------------------------------------------------------------
# main function here

def model_spectrum_ste(f_sup,data_mean_sparse,number_of_peaks):
        
    # we assume that the data is normalized, that is, the mean is equal to one
    res=data_mean_sparse.shape[0]
    method=1
    
    #------------------------------------------
    if method==0:
        [peaks, prominences , l_ips, r_ips, peak_width]=peaks_cwt_1(data_mean_sparse)
    elif method==1:
        [peaks, prominences , l_ips, r_ips, peak_width]=peaks_standard(data_mean_sparse)
    
    peak_high=data_mean_sparse[peaks]
    
    r_ips.astype(int)
    l_ips.astype(int)
    
    metric=1*peak_high+5*prominences
    
    idx_peaks=np.flip(np.argsort(metric))
    idx=peaks[idx_peaks]
    
    #############################33
    ##
    ##   TAKE ONLY THE STRONGEST ~number_of_peaks~ PEAKS
    ##
    #############################33
    rough_peak_positions = idx[0:number_of_peaks]
    
    #for  i in range(int(rough_peak_positions.size)):    
    if False:
        for  i in range(5):        
            p=idx_peaks[i]
            l_ips=int(properties['left_bases'][p])
            r_ips=int(properties['right_bases'][p])
            
            plt.plot(f_sup,data_mean_sparse)        
            plt.plot(f_sup[peaks[p]],data_mean_sparse[peaks][p],'*r')
            plt.plot(f_sup[l_ips:r_ips],data_mean_sparse[l_ips:r_ips]+0.00005,'--k')
        
        for  i in range(5):            
            p=idx_peaks[i]
            plt.plot(data_mean_sparse)
            plt.plot(peaks[p],data_mean_sparse[peaks[p]],'*')
            plt.plot(range(l_ips[p],r_ips[p]),data_mean_sparse[l_ips[p]:r_ips[p]],'--')            
            #plt.plot(range(l_win,r_win),data_mean_sparse[l_win:r_win],'--')      
    
    #----------------------------------------------------------
    # let's say that if the peak prominance is in the 75%  quantile, than we use the expand peak method only
    # if we are in the 25% quantile we worry about symmetry
    # also, the smoothing window depends on the 
    peak_prom_mean=np.mean(prominences)
    peak_width_mean=np.mean(peak_width)    
    
    # variables we store
    #------------------------------------------------------------------------------
    
    comp_range=np.zeros([rough_peak_positions.size,2])
    
    comp_beta_gauss=np.zeros([rough_peak_positions.size,4])
    comp_beta_lor=np.zeros([rough_peak_positions.size,3])
    comp_beta_gen_lor=np.zeros([rough_peak_positions.size,4])
    comp_beta_cos=np.zeros([rough_peak_positions.size,6])
    comp_MSE=np.zeros([rough_peak_positions.size,4])
    comp_bias=np.zeros([rough_peak_positions.size,1])
    
    #data_sparse_back=np.zeros([rough_peak_positions.size+1,data_sparse.shape[0],data_mean_sparse.shape[1]])
    #data_sparse_back[0,:,:]=data_sparse
        
    plot_f=0
    check_sup_fig=0
    #for  i in range(5):        
    #   for  i in range(int(rough_peak_positions.size)):
         
    for  i in range(int(rough_peak_positions.size)):
            print('Step: ',i,' - peak position: ',rough_peak_positions[i])
    
            p=idx_peaks[i]
            
            [l_win, r_win] = find_peak_sym_supp(peaks[p],int(l_ips[p]),int(r_ips[p]), 2, 3, data_mean_sparse)
            
            #[l_win, r_win],[l_ips,r_ips]
            
            if check_sup_fig:
                plt.figure('peak number '+str(int(i))+' frequency')
                plt.plot(data_mean_sparse)
                plt.plot(peaks[p],data_mean_sparse[peaks[p]],'*')
                plt.plot(range(l_ips[p],r_ips[p]),data_mean_sparse[l_ips[p]:r_ips[p]],'--')            
                plt.plot(range(l_win,r_win),data_mean_sparse[l_win:r_win],'--')            
                        
            #[l_win, r_win]=[l_ips,r_ips]
            x_data = f_sup[l_win:r_win]
            y_data = data_mean_sparse[l_win:r_win]
            #y_data = np.mean(data_sparse_back[i,l_win:r_win,:],axis=1)
            
            # this is my guess for a good strategy
            #bias_f = min(y_data)/2
            # random choice of bias
            bias_f = np.mean(np.sort(y_data)[0:int(y_data.size/5)])
            y_data = y_data -bias_f 
            
            # you can use the same intialization for gaus, lor, gen_lor        
            beta_init_lor=init_lor(x_data,y_data)
            
            
            # best gaussian fit
            result = minimize(mse_loss, beta_init_lor, args=(x_data,y_data,gauss_amp), method='Nelder-Mead', tol=1e-12)        
            beta_hat_gauss=result.x            
            MSE_gauss=result.fun
            
            # best generalized lorenzian         
            result = minimize(mse_loss, beta_init_lor, args=(x_data,y_data,gen_lor_amp), method='Nelder-Mead', tol=1e-12)        
            beta_hat_gen_lor=result.x    
            MSE_gen_lor=result.fun
            
            # best lorenzian 
            beta_init_lor2=beta_init_lor[:3]
            result = minimize(mse_loss, beta_init_lor2, args=(x_data,y_data,lor_amp), method='Nelder-Mead', tol=1e-12)        
            beta_hat_lor=result.x    
            MSE_lor=result.fun
            
            # best cosine window 
            
            beta_int_cos2=init_cos2(x_data,y_data)
            result = minimize(mse_loss, beta_int_cos2, args=(x_data,y_data,cos_win2), method='Powell', tol=1e-12)        
            beta_hat_cos2=result.x    
            MSE_cos2=result.fun
                    
            #plt.plot(x_data,y_data,label='original data') 
            #plt.plot(x_data,cos_win2(x_data,beta_int_cos2),'--',label='cos in')  
            #plt.plot(x_data,cos_win2(x_data,beta_hat_cos2),'--',label='cos')  
            
            if plot_f:
                plt.figure('peak number '+str(int(i))+' frequency')
                plt.plot(x_data,y_data,label='original data') 
                plt.plot(x_data[peaks[p]-l_win],y_data[peaks[p]-l_win],'*',label='peak')
                            
                plt.plot(x_data,gen_lor_amp(x_data,beta_hat_gen_lor),'-.',label='gen lor')
                plt.plot(x_data,lor_amp(x_data,beta_hat_lor),'-*',label='lor')
                plt.plot(x_data,cos_win2(x_data,beta_hat_cos2),'--',label='cos')  
                plt.plot(x_data,gauss_amp(x_data,beta_hat_gauss),'-|',label='gauss')  
                plt.legend()
                plt.show()
        
                    
            # store everything
            # function order is 
            # gaus
            # lor 
            # gen_lor
            # cos
            
            # store everything     
            comp_range[i]=[l_win,r_win]    
            comp_beta_gauss[i]=beta_hat_gauss
            comp_beta_lor[i]=beta_hat_lor
            comp_beta_gen_lor[i]=beta_hat_gen_lor
            comp_beta_cos[i]=beta_hat_cos2
            comp_MSE[i]=[MSE_gauss, MSE_lor, MSE_gen_lor, MSE_cos2]
            comp_bias[i]=[bias_f]
                        
        
    return [comp_range, comp_beta_gauss, comp_beta_lor, comp_beta_gen_lor, comp_beta_cos, comp_MSE, comp_bias]


def recap_spectrum(f_sup,data_mean_sparse,number_of_peaks,comp_range, comp_beta_gauss, comp_beta_lor, comp_beta_gen_lor, comp_beta_cos, comp_MSE, comp_bias):
    
    method=1
    
    #------------------------------------------
    if method==0:
        [peaks, prominences , l_ips, r_ips, peak_width]=peaks_cwt_1(data_mean_sparse)
    elif method==1:
        [peaks, prominences , l_ips, r_ips, peak_width]=peaks_standard(data_mean_sparse)
    
    peak_high=data_mean_sparse[peaks]
    
    r_ips.astype(int)
    l_ips.astype(int)
    
    metric=1*peak_high+5*prominences
    
    idx_peaks=np.flip(np.argsort(metric))
    idx=peaks[idx_peaks]
    
    #############################33
    ##
    ##   TAKE ONLY THE STRONGEST ~number_of_peaks~ PEAKS
    ##
    #############################33
    rough_peak_positions = idx[0:number_of_peaks]
    
    res=f_sup.shape[0]
    data_hat=np.zeros(res)
    
    count=np.zeros(4)
    
    for i in range(int(rough_peak_positions.size)):
        
        min_MSE_pos=int(np.argmin(comp_MSE[i,:]))
        l_win=int(comp_range[i,0])
        r_win=int(comp_range[i,1])
        x_data = f_sup[l_win:r_win]
        
        # gaus
        # lor 
        # gen_lor
        # cos
        count[min_MSE_pos]=count[min_MSE_pos]+1
        
        if    min_MSE_pos==0:     
            data_hat[l_win:r_win]=comp_bias[i]+gauss_amp(x_data,comp_beta_gauss[i])           
        elif  min_MSE_pos==1:
            data_hat[l_win:r_win]=comp_bias[i]+lor_amp(x_data,comp_beta_lor[i])           
        elif  min_MSE_pos==2:
            data_hat[l_win:r_win]=comp_bias[i]+gen_lor_amp(x_data,comp_beta_gen_lor[i])           
        else:
            data_hat[l_win:r_win]=comp_bias[i]+cos_win2(x_data,comp_beta_cos[i])           
                
    recap_peak_fit=1
    

    plt.figure('Reconstructed spectrum')
    plt.plot(f_sup,data_mean_sparse,label='original data') 
    plt.plot(f_sup[rough_peak_positions],data_mean_sparse[rough_peak_positions],'*',label='matched peaks')
    plt.plot(f_sup,data_hat,label='spectrum estimate') 
    
    for  i in range(int(rough_peak_positions.size)):    
        p=idx_peaks[i]    
        plt.annotate(str(i), (f_sup[peaks[p]],data_mean_sparse[peaks[p]]+10 ))
    
    #plt.annotate(str(i), (600,-10))
    
    plt.legend()
    plt.show()
    
    return data_hat


def data_pre_process(f_sup,data):
    # expect a 1600 times 10 times 10 file
    res=data.shape[0]
    dim_s=data.shape[1]
    data_sub=data.reshape(res,dim_s)
    
    
    min_data_amm=np.min(data_sub,axis=1)
    
    poly_min=np.poly1d(np.polyfit(f_sup,min_data_amm,3))(f_sup)
    poly_min_pos=poly_min+min(min_data_amm-poly_min)
    
    beta_init=np.polyfit(f_sup,min_data_amm,4)
    beta_init[4]=beta_init[4]+min(min_data_amm-poly_min)
    
    result = minimize(pos_mse_loss, beta_init, args=(f_sup,min_data_amm,poly4), method='Powell', tol=1e-18)
    beta_hat = result.x                 

    data_sub2=np.subtract(data_sub,poly4(f_sup,beta_hat).reshape([1,res,1])).reshape(res,10,10)
    
    fig_on=0

    if  fig_on:
        plt.figure('Check subtracting florescence')
        #plt.plot(f_sup,np.mean(data,axis=(1,2)),label)
        plt.plot(f_sup,min_data_amm,label='original data')    
        plt.plot(f_sup,poly4(f_sup,beta_hat),'--',label='Estimated florescence')
        plt.plot(f_sup,np.mean(data_sub2,axis=(1,2)),label='Sparsified data')
        plt.legend()
        
    return data_sub2


def identify_fitting_win_up(f_sup,data_mean,slide_win,fun, init_fit_fun):
    # slide the window, identify the block with small high  amplitude, fit 
    
    # loop over all windows of the data of size win 
    
    # order the data, form intervals of background and peaks
    # in the backgrount interpolate a poly 
    # int the rest interpoloted the fun, fitting optimized started by init_fit_fun    

    # data_mean=np.mean(data[2],axis=1)
    data_temp=data_mean.copy()
    # make even
    slide_win=int(2*int(slide_win/2))
    win_small=int(slide_win/25)

   
    win_poly = np.empty(2*int(data_temp.size/slide_win), dtype=np.object)
    fit_gen_lor = np.empty(2*int(data_temp.size/slide_win), dtype=np.object)
    for i in range(data_mean.shape[0]):
        win_poly [i] = []
        win_poly [i].append(i)
    
        fit_gen_lor [i] = []
        fit_gen_lor [i].append(i)
        
    count=-1
    for i in range(0,data_temp.shape[0]-slide_win,int(slide_win/2)):
        # slide of half of the window at each time
        count=count+1
        y_data=data_temp[i:i+int(slide_win)-1].copy()
        x_data=f_sup[i:i+int(slide_win)-1].copy()

        mean_level=np.mean(y_data)*np.ones(y_data.shape[0])
                
        # threshold for amplitude         
        # DIP DOWN ONLY VERSION: WE PUT NO ABSOLUTE VAUE
        th_10=np.linspace(np.sort(y_data-mean_level)[int(win_small)],0,10)
    
        # total MSE of interpolation plus fitting        
        mse10=100*np.ones(th_10.shape[0])
        
        # plt.plot(x_data,y_data)
        j_min_temp=0
        mse_min_tem=101
        
        
        for j in range(1,th_10.shape[0]):
            
            # both high and low
            # DIP DOWN ONLY VERSION: WE PUT NO ABSOLUTE VAUE
            pos=np.array(np.where((y_data-mean_level)<th_10[j])[0])
            
            if pos.size==0:
                # what to do here? restart with the mean value 
                mean_level=np.mean(y_data)
                pos=np.array(np.where((y_data-mean_level)<th_10[j])[0])
                
                
            #--------------------------------------------------------------------
            #   merge the points
            #--------------------------------------------------------------------
            
            diff_pos=pos[1:]-pos[:-1]-1            
            jumps=np.where(diff_pos>0)[0]
                
            #if the final element is res, the add a jump an the end
            if pos[-1]==f_sup.shape[0]-1:
                jumps=np.append(jumps,pos.shape[0]-1)
            
            final_lb=[]
            final_rb=[]
            
            if jumps.size==0:            
                    final_lb.append(pos[0])
                    final_rb.append(pos[-1])
            else:                    
                                
                    final_lb.append(pos[0])
                    final_rb.append(pos[jumps[0]])
                    
                    k=0
                    while k<jumps.shape[0]-1:
                        # 
                        final_lb.append(pos[jumps[k]+1])
                        # go to the next gap                
                        k=k+1
                        final_rb.append(pos[jumps[k]])
                    
            
            # add the first and the last intervals     
            idx_lr=np.zeros([2,len(final_rb)])
            idx_lr[0]=np.array(final_lb)
            idx_lr[1]=np.array(final_rb)
            idx_lr.astype(int)
            idx_lr=idx_lr.T
            
            # merge intervals 
            # remove the one intervals
            idx_lr=idx_lr[np.where(idx_lr[:,1]-idx_lr[:,0]>2)[0],:]        
            
            
            # minimum length of the intervals here
            # random choice
            
            merged = recursive_merge(idx_lr.tolist())
            idx_lr = np.array(merged).astype(int)
            
            #-------------------------------------------------------------------
            # Update the fitting
            #-------------------------------------------------------------------
                
            if idx_lr.size==0:
                # weird case when the whole interval is to be fittened
                # mean_level=np.zeros(x_data.shape)
                # don't do anything
                mean_level=mean_level
            else:                
                ind_poly=[]        
                for k in range(idx_lr.shape[0]):
                    left=int(idx_lr[k,0])
                    right=int(idx_lr[k,1])  
                    ind_poly=ind_poly+list(range(left,right-1))    
            
                ind_poly=np.array(ind_poly)
                
                mean_level=np.poly1d(np.polyfit(x_data[ind_poly],y_data[ind_poly],3))(x_data)
                        
                if False:
                    plt.plot(x_data,y_data) 
                    plt.plot(x_data,mean_level) 
                    plt.plot(x_data[ind_poly],y_data[ind_poly],'-*')
                    
                
            #----------------------------------
            # fit the function we have in input
            #----------------------------------
                        
            # find the complement of the position
            
            #----------------------------------
            # consider the problem of having to fit multiple peaks!
            #---------------------------------- just not now!            
            
            if idx_lr.size==0:
                # idx_lr_comp=np.array(range(i,i+int(slide_win)-1))
                idx_lr_comp=np.array([0,slide_win-1])
                idx_lr_comp=idx_lr_comp.reshape([1,2])
            else:
                idx_lr_comp=[] 
                
                # include the first interval?
                if  idx_lr[0,0]>0:
                    idx_lr_comp.append([0,idx_lr[0,0]])
            
                for k in range(1,idx_lr.shape[0]-1):
                    idx_lr_comp.append([idx_lr[k-1,1],idx_lr[k,0]])
                
                # include the last interval
                if  idx_lr[-1,1]<int(slide_win)-2:
                    idx_lr_comp.append([idx_lr[-1,1],int(slide_win)-2])
                        
            idx_lr_comp=np.array(idx_lr_comp)        
            beta_hat_gen_lor=np.zeros([idx_lr_comp.shape[0],4])
            MSE_gen_lor=np.zeros(idx_lr_comp.shape[0])
            
            
            
            #----------------------------------
            # PUT ANY FUNCTION HERE
            #----------------------------------
                        
            for k in range(idx_lr_comp.shape[0]):    
                ind_poly_comp=np.array(range(idx_lr_comp[k,0].astype(int),idx_lr_comp[k,1].astype(int)))
                beta_init_lor=init_lor(x_data[ind_poly_comp],data_mean[ind_poly_comp])
                result = minimize(mse_loss, beta_init_lor, args=(x_data[ind_poly_comp],data_mean[ind_poly_comp],gen_lor_amp), method='Nelder-Mead', tol=1e-12)        
                beta_hat_gen_lor[k]=result.x    
                MSE_gen_lor[k]=result.fun
                            
            #----------------------------------
            # look at the overall MSE
            #----------------------------------
            
            mse10[j]=np.var(data_mean[ind_poly]-mean_level[ind_poly])/np.size(ind_poly)+np.sum(MSE_gen_lor)
            
                
            if mse_min_tem>mse10[j]:
               mse_min_tem=mse10[j] 
               win_poly[count] = idx_lr_comp
               fit_gen_lor[count] = beta_hat_gen_lor
               # store the everything 
               
                        
    return    [win_poly,fit_gen_lor]
        
            
def data_pre_process_v1(f_sup,data_temp):
    
    res=data_temp.shape[0]

    f_sup_temp=f_sup.copy()
    idx_temp=range(f_sup.shape[0])
    #data_temp=data[2]
    data_mean=np.mean(data_temp,axis=1)
    data_temp_mean=np.mean(data_temp,axis=1)
    
    # what's the interva we want to cover?
    fit_th=0.8
    
    #while len_temp<fit_th*f_sup.shape[0]:
    th_hist=np.zeros(10)
    
    for i0 in range(10):
       
        poly_min=np.poly1d(np.polyfit(f_sup_temp,data_temp_mean,3))(f_sup_temp)
        poly_min_pos=poly_min+min(data_temp_mean-poly_min)
        
        beta_init=np.polyfit(f_sup_temp,data_temp_mean,4)
        beta_init[4]=beta_init[4]+min(data_temp_mean-poly_min)
            
        #result = minimize(mse_loss, beta_init, args=(f_sup_temp,data_temp_mean,poly4), method='Nelder-Mead', tol=1e-12)
        result = minimize(reg_pos_mse_loss, beta_init, args=(f_sup_temp,data_temp_mean,poly4), method='Nelder-Mead', tol=1e-12)
        # look at the variance between the estimated florescence and the data, pick the interval in which this 
        # variance is below somethig
        
        
        beta_hat = result.x                 
            
        #est_clean=np.subtract(data_temp[idx_temp],est_flor.reshape([est_flor.shape[0],1]))
        
        est_flor=poly4(f_sup,beta_hat)
        
        est_clean=np.subtract(data_temp,est_flor.reshape([est_flor.shape[0],1]))
        
        # normalize variance
        est_var=np.var(est_clean,axis=1)/np.var(est_clean)
        
        # find the portion of the data (original) in whi
        th=min(est_var)
        len_temp=0
        
        while len_temp<fit_th*f_sup.shape[0]:
                    
            pos=[]
            
            while len(pos)==0:
                pos=np.array(np.where(est_var<th)[0])        
                th=th*1.1
                    
            diff_pos=pos[1:]-pos[:-1]-1    
            jumps=np.where(diff_pos>0)[0]
            
            #if the final element is res, the add a jomp an the end
            if pos[-1]==res-1:
                jumps=np.append(jumps,pos.shape[0]-1)
            
            final_lb=[]
            final_rb=[]        
                        
            final_lb.append(pos[0])
            final_rb.append(pos[jumps[0]])
            
            i=0
            while i<jumps.shape[0]-1:
                # 
                final_lb.append(pos[jumps[i]+1])
                # go to the next gap                
                i=i+1
                final_rb.append(pos[jumps[i]])
            
            # add the first and the last intervals 
            win_tail=int(fit_th*f_sup.shape[0]/10)
            final_lb.insert(0,0)
            final_rb.insert(0,win_tail)
            
            final_lb.append(res-win_tail-1)
            final_rb.append(res-1)
                            
            idx_lr=np.zeros([2,len(final_rb)])
            idx_lr[0]=np.array(final_lb)
            idx_lr[1]=np.array(final_rb)
            idx_lr.astype(int)
            idx_lr=idx_lr.T
            
            # merge intervals 
            # remove the one intervals
            idx_lr=idx_lr[np.where(idx_lr[:,1]-idx_lr[:,0]>2)[0],:]        
    
            merged = recursive_merge(idx_lr.tolist())
            idx_lr = np.array(merged).astype(int)
                                
            # min length of the intervals here
            win=win_tail/2
            idx_lr=idx_lr[np.where(idx_lr[:,1]-idx_lr[:,0]>win)[0],:]
                
            len_temp=np.sum(idx_lr[:,1]-idx_lr[:,0])
            th=th*1.1   
            
        # update  the fitting support
                
        # leh's see the final fitting
    
            ind_wb=[]
            
            # check the positions
                
            for i in range(idx_lr.shape[0]):
                left=int(idx_lr[i,0])
                right=int(idx_lr[i,1])+1    
                ind_wb=ind_wb+list(range(left,right))    
                
            ind_wb=ind_wb+list(range(left,right))    
            ind_wb=np.array(ind_wb)    
        
            f_sup_temp =  f_sup[ind_wb]
            data_temp_mean =  data_mean[ind_wb]
    
    
    
        th_hist[i0]=th
        # reduce the fitting threshould
        fit_th=fit_th*0.95
            
    #######
    ##
    ## add the beginnig and the end to the interval, so we don't go all the way off!!!
     
    if False:
    #if True:
        plt.plot(est_flor,label='est. flor. ')
        plt.plot(data_mean, label='mean values')
        plt.plot(np.mean(est_clean,axis=1),label='est mean values')
        #plt.plot(est_var,label='variance estiamte')
        plt.plot(ind_wb,data_mean[ind_wb],'*',label='good variance')
        plt.plot(ind_wb,  data_temp_mean,'*',label='my interval')
        plt.legend()
        plt.show
    
    
    # find the best scaling of the florescence to remove from each spectrum
    
    # var_additive=np.dot(est_flor,data_temp.reshape(res,dim_s))
    sub=np.outer(est_flor,np.dot(est_flor,data_temp)/var_additive)
    
    data_curr=data_temp-sub
            
    
    # plt.plot(np.mean(data_curr,axis=1),label='new flor')
    
    # data11=data_pre_process(f_sup,data[2])
    # data11=data11.reshape([res,dim_s])
    
    # plt.plot(np.mean(data11-data_curr,axis=1))
    
    # plt.plot(np.mean(data11,axis=1),label='old flor')
    # plt.legend()
    # plt.plot()

    return data_curr



def reconstruct_spectrum(f_sup, comp_range, comp_beta_gauss, comp_beta_lor, comp_beta_gen_lor, comp_beta_cos, comp_MSE, comp_bias):
    
    res=f_sup.shape[0]
    data_hat=np.zeros(res)
    
    count=np.zeros(4)
    
    for i in range(int(comp_range.shape[0])):
        
        min_MSE_pos=int(np.argmin(comp_MSE[i,:]))
        l_win=int(comp_range[i,0])
        r_win=int(comp_range[i,1])
        x_data = f_sup[l_win:r_win]
        
        # gaus
        # lor 
        # gen_lor
        # cos
        count[min_MSE_pos]=count[min_MSE_pos]+1
        
        if    min_MSE_pos==0:     
            data_hat[l_win:r_win]=comp_bias[i]+gauss_amp(x_data,comp_beta_gauss[i])           
        elif  min_MSE_pos==1:
            data_hat[l_win:r_win]=comp_bias[i]+lor_amp(x_data,comp_beta_lor[i])           
        elif  min_MSE_pos==2:
            data_hat[l_win:r_win]=comp_bias[i]+gen_lor_amp(x_data,comp_beta_gen_lor[i])           
        else:
            data_hat[l_win:r_win]=comp_bias[i]+cos_win2(x_data,comp_beta_cos[i])       
            
    return data_hat