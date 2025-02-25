from itertools import islice

import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import hilbert, find_peaks
import pylab as p
import scipy.signal as sci
import scipy.stats as stats
from scipy.optimize import minimize
from scipy.optimize import curve_fit
import math
from math import pi

#import ste_model_spectrum.py

from ste_model_spectrum_v3 import *

res=964
dim_s=100

#------------------------------------------------------------------------------
import shelve

filename='shelve_save_data_analyte.out'

my_shelf = shelve.open(filename)
for key in my_shelf:
    globals()[key]=my_shelf[key]
my_shelf.close()

space_mean=np.mean(data[2],axis=1)            
f_sup=f_sup[:-1]


fit_fun = gen_lor_amp
init_fit_fun = init_lor

slide_win=100
num_th=100

# proceduce: 

# star with poly interpolation
# choose the points where the linear interpolation crosses the  spectrum
# one parameter: number of threshord
# choose peaks below threshould 
# fit and store
x_data=f_sup
y_data=space_mean

poly_interp=np.poly1d(np.polyfit(x_data,y_data,4))(x_data)
idx_pos_min=np.argsort((y_data-poly_interp)**2)[:num_th]

y_interp = np.interp(idx_pos_min, f_sup, space_mean)



if False:
    plt.plot(x_data,y_data)
    plt.plot(x_data,poly_interp)
    plt.plot(x_data,y_interp)
    plt.plot(x_data[idx_pos_min],y_data[idx_pos_min],'*')
    


 
th_10=np.linspace(-np.sort(-(y_data_win-mean_level_win))[int(win_small)],0,11)


mse_poly= np.var(y_data_win[ind_poly]-mean_level_win[ind_poly])









#------------------------------------------------------------------------------


# find the  points in which the 


plt.plot(f_sup,space_mean)














fitting_data=identify_fitting_win_up(f_sup,space_mean,num_th,num_th,gen_lor_amp,init_lor)




# # merge the windows, swip through the i's and identify the windows

if False
    range_lr=[0 , 0]
    for i in range(2*int(space_mean.shape[0]/slide_win)):
            for j in range(1,num_th):
                
                range_lr=np.squeeze(np.array(fitting_data[i,j]['range_peak']))
                        
                if range_lr.size==1:
                    print('Window',i,'Th',j,'No peak')
                else:
                    print('Window',i,'Th',j,'Range',range_lr[0],'--',range_lr[1])



# stitch together the variaous windows and check visually

all_win=[]

for i in range(2*int(space_mean.shape[0]/slide_win)):        
    for j in range(1,num_th):
        peak_l_r_win=np.zeros((1,2))
        # pile all intervals in the smallest threshold and check that everything is fine there
        tmp=np.squeeze(np.array(fitting_data[i,j]['range_peak']))
        if tmp.size>1:
            tmp=tmp.reshape(int(tmp.size/2),2)
            range_lr=np.array(i*int(slide_win/2)+tmp)
            # range_lr=np.array(tmp)
            # peak_l_r_win.extend(range_lr.tolist())
            peak_l_r_win=np.concatenate((peak_l_r_win,range_lr),axis=0)
                           
            peak_l_r_win=peak_l_r_win[1:]
            
            sorted_on_start = sorted(peak_l_r_win.tolist())
            
            merged_lr = recursive_merge(sorted_on_start.copy())
             
            merged_lr = np.array(merged_lr ).astype(int)
            
            idx_peaks=[]        
            for j in range(merged_lr.shape[0]):    
                idx_peaks=idx_peaks+list(range(merged_lr[j,0],merged_lr[j,1]))    
            
            
            idx_peaks=np.array(idx_peaks)
            plt.plot(f_sup[idx_peaks],j+space_mean[idx_peaks],'--')
                    


# plot windows 

            
# let's check some peaks
if False:
    plt.plot(f_sup,space_mean)
    for j in range(peak_l_r_win.shape[0]):
        idx_peaks=range(int(peak_l_r_win[j,0]),int(peak_l_r_win[j,1]))
        plt.plot(f_sup[idx_peaks],j+space_mean[idx_peaks],'--')




#---------------------------------------------------------------------
# merge windows on the boudaries across thresholds 
# merging occurs at the same th. level









#---------------------------------------------------------------------
# rank peaks on MSE, hight, area, 



# merge the windows, swip through the i's and identify the windows
range_lr=[0 , 0]
for i in range(2*int(space_mean.shape[0]/slide_win)):
        for j in range(1,num_th):
            
            range_lr=np.squeeze(np.array(fitting_data[i,j]['range_peak']))
            
            if range_lr.size==1:
                print('Window',i,'Th',j,'No peak')
            else:
                print('Window',i,'Th',j,'Range',range_lr[0],'--',range_lr[1])


# ----------------------------------------------------------------------------


peak_l_r_win=np.zeros((1,2))

for i in range(2*int(space_mean.shape[0]/slide_win)):        
        j=9
        # pile all intervals in the smallest threshold and check that everything is fine there
        tmp=np.squeeze(np.array(fitting_data[i,j]['range_peak']))
        if tmp.size>1:
            # rank_mse = 
            # rank_area = 
            # rank_hight =
            
            tmp=tmp.reshape(int(tmp.size/2),2)
            range_lr=np.array(i*int(slide_win/2)+tmp)
            # range_lr=np.array(tmp)
            # peak_l_r_win.extend(range_lr.tolist())
            peak_l_r_win=np.concatenate((peak_l_r_win,range_lr),axis=0)
            
        
                    
            

# at this point we have to merge intervals that superpose A LOT: what do we mean by that?





#----------------------------------------------------------------------------
# choose the number of peaks you want and keep the N largest peaks.
# then merge up the intervals so that you preserve those peaks

peak_l_r_win=np.zeros((1,2))
beta_win=np.zeros((1,4))
rank_win= np.zeros((1,1))
y_data=space_mean

for i in range(2*int(space_mean.shape[0]/slide_win)):
        for j in range(1,10):            
                                    
            beta_tmp = np.array(fitting_data[i,j]['beta_peak'])
            
            for k in  range(beta_tmp.shape[0]):
                # beta_win = np.concatenate((beta_win,beta_tmp[k].reshape((1,4)),axis=0)                            
                beta_tmp2=beta_tmp[k][0].reshape(1,4)
                
                beta_win = np.concatenate((beta_win,beta_tmp2))
                
                rank_tmp = appr_area_gen_lor(beta_tmp2.T)
                                
                rank_win = np.concatenate((rank_win,rank_tmp),axis=0)
                
            range_tmp=np.squeeze(np.array(fitting_data[i,j]['range_peak']))
            range_tmp.reshape(int(range_tmp.size/2),2)
            
            peak_l_r_win=np.concatenate((peak_l_r_win,range_lr),axis=0)
            

peak_l_r_win=peak_l_r_win[1:]
            





# merge intervals on the boundaries


# remove peaks in which the peaks are too close
for  i in range(2*int(y_data.shape[0]/slide_win)):
    np.where 
    int(i*(slide_win/2))



#-------------------------------------------------------------------------------
# order the peaks by area (for now just do amplitude) and display the top TEN

TOP=10




#----------------------------------------------------------------------------
#----------------------------------------------------------------------------
#----------------------------------------------------------------------------

# go down the thershold
# -> split 
# -> merge , or 
# -> add
# do this across neighbouring intervals
# 












#----------------------------------------------------------------------------
#----------------------------------------------------------------------------
#----------------------------------------------------------------------------

for i in range(2*int(space_mean.shape[0]/slide_win)):        
        j=9
        # pile all intervals in the smallest threshold and check that everything is fine there
        tmp=np.squeeze(np.array(fitting_data[i,j]['range_peak']))


peak_l_r_win=peak_l_r_win[1:]

sorted_on_start = sorted(peak_l_r_win.tolist())

merged = recursive_merge(sorted_on_start.copy())

merged_up =np.array(merged).astype(int)

idx_peaks=[]        
for k in range(merged_up.shape[0]):    
    idx_peaks=idx_peaks+list(range(merged_up[k,0],merged_up[k,1]))    
    
idx_peaks=np.array(idx_peaks)
# check the peak position

if False:
    plt.plot(f_sup,space_mean)
    plt.plot(f_sup[idx_peaks],space_mean[idx_peaks],'--')

peak_l_r_win.append(range_lr.tolist()) 
peak_l_r_win = np.array(recursive_merge(peak_l_r_win.tolist())).astype(int)    





for i in range(2*int(space_mean.shape[0]/slide_win)):        
        
        # pile all intervals in the smallest threshold and check that everything is fine there
        tmp=np.squeeze(np.array(fitting_data[i,j]['range_peak']))



for i in range(2*int(space_mean.shape[0]/slide_win)):
        for j in range(1,10):
            
            range_lr=np.squeeze(np.array(fitting_data[i,j]['range_peak']))
            
            if range_lr.size==1:
                print('Window',i,'Th',j,'No peak')
            else:
                print('Window',i,'Th',j,'Range',range_lr[0],'--',range_lr[1])
    
    



# #
# #-------------------------------------------------------------------------------
    
    
#             peak_l_r_win=np.zeros([peaks.size,2])
    
#     for i in range(peaks.size):     
#         [l_win, r_win]=find_win_supp(peaks[i],l_ips[i],r_ips[i], y_up_sub,1)
#         peak_l_r_win[i]=[l_win, r_win]

#         # merge intervals                       
    
    
    
    
#         peak_l_r_win.append(range_lr.tolist()) 
        
    
        
#         # this is too tricky to implement atm         
#         for i in range(peaks.size):     
#             [l_win, r_win]=find_win_supp(peaks[i],l_ips[i],r_ips[i], y_up_sub)
#             peak_l_r_win[i]=[l_win, r_win]
    
#         # for i in range(peaks.size):                 
#         #     peak_l_r_win[i]=[l_ips[i], r_ips[i]]
    
#         # merge intervals                       
#         peak_l_r_win = np.array(recursive_merge(peak_l_r_win.tolist())).astype(int)
        
    
    
    
        
    
    
#         # do they interset? the
#         range_lr=np.squeeze(np.array(fitting_data[i,j]['range_peak']))
        
#         if range_lr.size==1:
#             print('Window',i,'Th',j,'No peak')
#         else:
#             print('Window',i,'Th',j,'Range',range_lr[0],'--',range_lr[1])




        

# plot  the MSE in terms of the different threshold windows


#------------------------------------------------------------------------------
# import the clean ACE spectrum

i_file= open('data/Acephate_Exported.dat', "r")
temp = i_file.readlines()
temp=[i.strip('\n') for i in temp]
dataACE=np.array([(row.split('\t')) for row in temp], dtype=np.float32)
f_ACE=dataACE[:,0]
dataACE=dataACE[:,1]

#------------------------------------------------------------------------------
f_sup=f_sup[:-1]
data_mean=np.mean(data,axis=2)
#------------------------------------------------------------------------------
# aligt the data

#  what's the shift?
align_init=np.argmin((f_ACE-f_sup[0])**2)
align_end=np.argmin((f_ACE-f_sup[-1])**2)

len_temp=f_sup.shape[0]
data_ace_temp =np.zeros(len_temp)
n_feq=align_init

i=0
s1=f_sup.copy()

while i<len_temp-1:        
    pos=np.where((f_ACE>=f_sup[i]) & (f_ACE<=f_sup[i+1]))
    
    # 
    data_ace_temp[i] =np.mean(dataACE[pos])
    
    # update counter
    i=i+1
    
# last point just guess
data_ace_temp[i]=dataACE[align_end]


while False:
    plt.plot(f_ACE, dataACE,label='orig')
    plt.plot(f_sup, data_ace_temp,label='temp')
    plt.plot(f_sup, data_mean[0],label='data')
    
    plt.legend()
    plt.show()

#------------------------------------------------------------------------------

# update the data mean
data_mean[0]=data_ace_temp

#------------------------------------------------------------------------------

plt.figure('raw data')
labels = ['ACE', 'MG', 'mix1_1','mix1_2','mix2_1','mix2_2']


for data_mean, label in zip(data_mean, labels):
    plt.plot(f_sup, data_mean, label=label)

plt.legend()
plt.show()

num_peaks=10

data_mean=np.mean(data,axis=2)
data_mean[0]=data_ace_temp

#------------------------------------------------------------------------------
# Normalize data
#------------------------------------------------------------------------------

for i in range(6):
    data[i]=data[i]/np.mean(data[i])
    
# model MG
data_MG_sparse=remove_est_florescence(f_sup,data[1])
data_MG_mean=np.mean(data_MG_sparse,axis=1)
data_MG_mean_smooth = sci.savgol_filter(data_MG_mean, window_length = 11, polyorder = 5)

[comp_rangeM, comp_beta_gaussM, comp_beta_lorM, comp_beta_gen_lorM, comp_beta_cosM, comp_MSEM, comp_biasM]=model_spectrum_ste(f_sup,data_MG_mean_smooth ,num_peaks)

vecM=[comp_rangeM, comp_beta_gaussM, comp_beta_lorM, comp_beta_gen_lorM, comp_beta_cosM, comp_MSEM, comp_biasM]

recap_spectrum(f_sup,data_MG_mean_smooth,num_peaks,*vecM)

plt.plot(f_sup,data_MG_mean_smooth)

#------------------------------------------------------------------------------

# # model ACE 
data_ACE_sparse=remove_est_florescence(f_sup,data_mean[0])

data_ACE_mean_smooth=sci.savgol_filter(data_ACE_sparse, window_length = 11, polyorder = 5)
#data_ACE_mean=data

[comp_rangeA, comp_beta_gaussA, comp_beta_lorA, comp_beta_gen_lorA, comp_beta_cosA, comp_MSEA, comp_biasA]=model_spectrum_ste(f_sup,data_ACE_mean_smooth,num_peaks)

vecA=[comp_rangeA, comp_beta_gaussA, comp_beta_lorA, comp_beta_gen_lorA, comp_beta_cosA, comp_MSEA, comp_biasA]

recap_spectrum(f_sup,data_ACE_mean_smooth,num_peaks, comp_rangeA, comp_beta_gaussA, comp_beta_lorA, comp_beta_gen_lorA, comp_beta_cosA, comp_MSEA, comp_biasA)

# show the smoothing
while False:
    plt.figure("Smoothing")
    plt.plot(f_sup,data_MG_sparse)
    plt.plot(f_sup,data_MG_mean_smooth)


while False:
    plt.figure("Smoothing")
    plt.plot(data_ACE_sparse)
    plt.plot(data_ACE_mean_smooth)
    

    
# ####--------------------------------------------------------------------------
# # align the spectrums, refarding of the power

# plt.plot(data[2,:,10])
# plt.plot(data[2,:,20])


# find the area of minimum variability
# space_var=np.var(data[2],axis=1)

# # find the contiguous intervals in which the variance is below a certain thershold, so that 

# plt.plot(space_mean)
# plt.plot(data[2,:,10])
# plt.plot(data[2,:,20])
# plt.plot(space_var)

# # minimized polyfit variance

# # plt.plot(np.var(data_curr,axis=1),label='new flor')
# # plt.plot(np.var(data11,axis=1),label='old flor')
# # plt.legend()
# # plt.plot()


####-----------------------------------------------------------------------
####


#------------------------
# init_fit_fun = init_lor
# fit_fun = gen_lor_amp            

space_mean=np.mean(data[2],axis=1)            
[window , beta]=identify_fitting_win_up(f_sup,space_mean,100,gen_lor_amp,init_lor)

####
####-----------------------------------------------------------------------


# compare with the previous processing

plt.plot(f_sup,np.mean(data[2],axis=1))

identify_fitting_win_up

data11v1=data_pre_process_v1(f_sup,data[2])



data11v1=data_pre_process_v1(f_sup,data[2])
data12v1=data_pre_process_v1(f_sup,data[3])
data21v1=data_pre_process_v1(f_sup,data[4])
data22v1=data_pre_process_v1(f_sup,data[5])
    
data11=data_pre_process(f_sup,data[2])
data12=data_pre_process(f_sup,data[3])
data21=data_pre_process(f_sup,data[4])
data22=data_pre_process(f_sup,data[5])

        
data_11_smooth=sci.savgol_filter(np.mean(data11v1,axis=1), window_length = 11, polyorder = 5)
vec_11=model_spectrum_ste(f_sup,data_11_smooth,2*num_peaks)

data_12_smooth=sci.savgol_filter(np.mean(data12v1,axis=1), window_length = 11, polyorder = 5)
vec_12=model_spectrum_ste(f_sup,data_12_smooth,2*num_peaks)

data_21_smooth=sci.savgol_filter(np.mean(data21v1,axis=1), window_length = 11, polyorder = 5)
vec_21=model_spectrum_ste(f_sup,data_21_smooth,2*num_peaks)

data_22_smooth=sci.savgol_filter(np.mean(data22v1,axis=1), window_length = 11, polyorder = 5)
vec_22=model_spectrum_ste(f_sup,data_22_smooth,2*num_peaks)


rec11=recap_spectrum(f_sup,data_11_smooth,2*num_peaks,*vec_11)
rec12=recap_spectrum(f_sup,data_12_smooth,2*num_peaks,*vec_11)
rec21=recap_spectrum(f_sup,data_21_smooth,2*num_peaks,*vec_21)
rec22=recap_spectrum(f_sup,data_22_smooth,2*num_peaks,*vec_21)

recMG=recap_spectrum(f_sup,data_MG_mean_smooth,num_peaks,*vecM)
recACE=recap_spectrum(f_sup,data_ACE_mean_smooth,num_peaks,*vecA)

plt.plot(rec11,label='11')
plt.plot(np.mean(data[2],axis=1)-np.mean(data[2]))
plt.plot(recMG,label='MG')
plt.plot(recACE,label='ACE')
plt.legend()
plt.show()



plt.plot(rec21,label='21 rec')
plt.plot(data_21_smooth,'--',label='21')
plt.plot(np.mean(data[4],axis=1)-np.mean(data[4]))
plt.plot(recMG,label='MG')
plt.plot(recACE,label='ACE')
plt.legend()
plt.show()



plt.plot(rec22,label='22 rec')
plt.plot(data_22_smooth,'--',label='22')
plt.plot(np.mean(data22v1,axis=1),'-.',label='22 orig.')
plt.plot(np.mean(data[5],axis=1)-np.mean(data[5]))
plt.plot(np.mean(data22,axis=1)-np.mean(data22))
plt.plot(data22,'--',label='22')
plt.plot(recMG,label='MG')
plt.plot(recACE,label='ACE')
plt.legend()
plt.show()
    
####--------------------------------------------------------------------------
####--------------------------------------------------------------------------
####--------------------------------------------------------------------------
####--------------------------------------------------------------------------


correlation_approach=False

if correlation_approach:
    # check special  correlation with the 2 measuraments set in the two time instants
    
    #------------------------------------------------------------------------------
    # store per peak correlation
    
    mean_m11=np.zeros(int(num_peaks))
    mean_m12=np.zeros(int(num_peaks))
    mean_m21=np.zeros(int(num_peaks))
    mean_m22=np.zeros(int(num_peaks))
    
    # start with data 15
    
    plt.plot(np.mean(data11,axis=1)-np.mean(data11),label='v0')
    plt.plot(np.mean(data11v1,axis=1)-np.mean(data11v1),label='v1')
    plt.plot(dataMG_hat,label='MG hat')
    plt.legend()
    plt.show
    
    dataMG_hat=reconstruct_spectrum(f_sup,*vecM)
    dataA_hat=reconstruct_spectrum(f_sup,*vecA)

  
    # total correlation plot MG
    corr_11MG= np.dot(dataMG_hat,data11.reshape(res,dim_s)).reshape(10,10)
    corr_12MG= np.dot(dataMG_hat,data12.reshape(res,dim_s)).reshape(10,10)
    corr_21MG= np.dot(dataMG_hat,data21.reshape(res,dim_s)).reshape(10,10)
    corr_22MG= np.dot(dataMG_hat,data22.reshape(res,dim_s)).reshape(10,10)

    corr_11MGv1= np.dot(dataMG_hat,data11v1.reshape(res,dim_s)).reshape(10,10)
    corr_12MGv1= np.dot(dataMG_hat,data12v1.reshape(res,dim_s)).reshape(10,10)
    corr_21MGv1= np.dot(dataMG_hat,data21v1.reshape(res,dim_s)).reshape(10,10)
    corr_22MGv1= np.dot(dataMG_hat,data22v1.reshape(res,dim_s)).reshape(10,10)
    
    # total correlation plot ACE
    corr_11A= np.dot(dataA_hat,data11.reshape(res,dim_s)).reshape(10,10)
    corr_12A= np.dot(dataA_hat,data12.reshape(res,dim_s)).reshape(10,10)
    corr_21A= np.dot(dataA_hat,data21.reshape(res,dim_s)).reshape(10,10)
    corr_22A= np.dot(dataA_hat,data22.reshape(res,dim_s)).reshape(10,10)
    
    corr_11Av1= np.dot(dataA_hat,data11v1.reshape(res,dim_s)).reshape(10,10)
    corr_12Av1= np.dot(dataA_hat,data12v1.reshape(res,dim_s)).reshape(10,10)
    corr_21Av1= np.dot(dataA_hat,data21v1.reshape(res,dim_s)).reshape(10,10)
    corr_22Av1= np.dot(dataA_hat,data22v1.reshape(res,dim_s)).reshape(10,10)
        
    plot_cor_space=1
    
    if plot_cor_space:
        plt.figure('Total correlation in space for MG')
        plt.plot(corr_11MG.reshape(dim_s)-np.mean(corr_11MG.reshape(dim_s)),'*-',label='11-MG')
        plt.plot(corr_11MGv1.reshape(dim_s)-np.mean(corr_11MGv1.reshape(dim_s)),'*-',label='11-MG-v1')
        plt.legend()
        # plt.plot(corr_12MG.reshape(dim_s),'.-',label='12-MG')
        
        # plt.plot(corr_21MG.reshape(dim_s),'|-',label='21-MG')
        # plt.plot(corr_22MG.reshape(dim_s),'+-',label='22-MG')
        
        
    
        plt.legend()
        plt.show()
    
        plt.figure('Total correlation in space for A')
        
        plt.plot(corr_11A.reshape(dim_s),'*-',label='11-A')
        plt.plot(corr_12A.reshape(dim_s),'.-',label='12-A')
        
        plt.plot(corr_21A.reshape(dim_s),'|-',label='21-A')
        plt.plot(corr_22A.reshape(dim_s),'+-',label='22-A')
    
        plt.legend()
        plt.show()
    
    
    # average correlation in time
    time_corr_MG=np.zeros(2)
    time_corr_MG[0]=np.mean([np.mean(corr_11MG),np.mean(corr_12MG)])
    time_corr_MG[1]=np.mean([np.mean(corr_21MG),np.mean(corr_22MG)])
    
    time_corr_A=np.zeros(2)
    time_corr_A[0]=np.mean([np.mean(corr_11A),np.mean(corr_12A)])
    time_corr_A[1]=np.mean([np.mean(corr_21A),np.mean(corr_22A)])
    
    
    plot_time_corr=1
    
    if plot_time_corr:
        plt.plot(time_corr_MG,'o-',label='MG')
        plt.plot(time_corr_A,'+-',label='A')
        
        plt.legend()
        plt.show()
        
    
    # average correlation PER PEAK
    mean_corr11M=np.zeros(num_peaks)
    mean_corr12M=np.zeros(num_peaks)
    mean_corr21M=np.zeros(num_peaks)
    mean_corr22M=np.zeros(num_peaks)
    
    
    mean_corr11A=np.zeros(num_peaks)
    mean_corr12A=np.zeros(num_peaks)
    mean_corr21A=np.zeros(num_peaks)
    mean_corr22A=np.zeros(num_peaks)
    
    
    for i in range(num_peaks):
                   
        l_win=int(comp_rangeM[i,0])
        r_win=int(comp_rangeM[i,1])
        x_data = f_sup[l_win:r_win]
        
        #np.dot(data_hat,data1p5p.reshape(res,dim_s)).reshape(10,10)
         
        mean_corr11M[i]=np.mean(np.dot(dataMG_hat[l_win:r_win],data11[l_win:r_win].reshape([r_win-l_win,dim_s])))
        mean_corr12M[i]=np.mean(np.dot(dataMG_hat[l_win:r_win],data12[l_win:r_win].reshape([r_win-l_win,dim_s])))
        mean_corr21M[i]=np.mean(np.dot(dataMG_hat[l_win:r_win],data21[l_win:r_win].reshape([r_win-l_win,dim_s])))
        mean_corr22M[i]=np.mean(np.dot(dataMG_hat[l_win:r_win],data22[l_win:r_win].reshape([r_win-l_win,dim_s])))
        
        # gaus
        # lor 
        # gen_lor
        # cos
        
    
    for i in range(num_peaks):
                   
        l_win=int(comp_rangeA[i,0])
        r_win=int(comp_rangeA[i,1])
        x_data = f_sup[l_win:r_win]
        
        #np.dot(data_hat,data1p5p.reshape(res,dim_s)).reshape(10,10)
         
        mean_corr11A[i]=np.mean(np.dot(dataA_hat[l_win:r_win],data11[l_win:r_win].reshape([r_win-l_win,dim_s])))
        mean_corr12A[i]=np.mean(np.dot(dataA_hat[l_win:r_win],data12[l_win:r_win].reshape([r_win-l_win,dim_s])))
        mean_corr21A[i]=np.mean(np.dot(dataA_hat[l_win:r_win],data21[l_win:r_win].reshape([r_win-l_win,dim_s])))
        mean_corr22A[i]=np.mean(np.dot(dataA_hat[l_win:r_win],data22[l_win:r_win].reshape([r_win-l_win,dim_s])))
        
    corr_peak=1
    plt.figure('Correlation recap')
    
    if corr_peak:
        
        plt.plot(mean_corr11M,'*-',label='M-11')
        plt.plot(mean_corr12M,'.-',label='M-12')
        plt.plot(mean_corr21M,'|-',label='M-21')
        plt.plot(mean_corr22M,'+-',label='M-22')
        
        plt.plot(mean_corr11A,'*-',label='A-11')
        plt.plot(mean_corr12A,'.-',label='A-12')
        plt.plot(mean_corr21A,'|-',label='A-21')
        plt.plot(mean_corr22A,'+-',label='A-22')
            
            
        plt.legend()
        plt.show()
        
    
    
    # CHECH THE CORRELATION POINT AT 
    plt.figure('Check position (1,8) ')
    
    plt.plot(data21[:,1,8],label='2,1 pos(1,8)') 
    plt.plot(data22[:,1,8],label='2,2 pos(1,8)') 
    plt.plot(np.mean(data21,axis=(1,2)), label='2,1 mean' )
    plt.plot(np.mean(data22,axis=(1,2)), label='2,2 mean' )
    
    plt.legend()
    plt.show()
    
    
    # MODEL AVERAGE SPECTRUM
    
    plt.plot(np.max(data21,axis=(1,2)), label='2,1 max' )
    plt.plot(np.max(data22,axis=(1,2)), label='2,2 max' )
    plt.plot(np.mean(data21,axis=(1,2)), label='2,1 mean' )
    plt.plot(np.mean(data22,axis=(1,2)), label='2,2 mean' )
    plt.legend()
    plt.show()
    

# """
# Created on Wed May  6 11:40:53 2020

# @author: rinis
# """

# str_ACE='data/SERS with mix analyte/Acephate 10-2M 5715minutes/Acephate-SERS_1500ms_Exported.dat'
# str_MG='data/SERS with mix analyte/MG 10-5M 930minutes\MG-SERS_1500ms 1avg 2box_Exported.dat'
# str_mix1_1='data/SERS with mix analyte/mix/1115min/Mix-SERS-A-(1)-1115min_532nm_Newton_105um _ND1-51_20x-NA0.75_1500ms 1avg 2box (S-S-H-C)_Exported.dat'
# str_mix1_2='data/SERS with mix analyte/mix/1115min/Mix-SERS-A-(2)-1115min_532nm_Newton_105um _ND1-51_20x-NA0.75_1500ms 1avg 2box (S-S-H-C)_Exported.dat'
# str_mix2_1='data/SERS with mix analyte/mix/4027min\Mix-SERS-A-(1)-4027min_532nm_Newton_105um _ND1-51_20x-NA0.75_1500ms 1avg 2box (S-S-H-C)_Exported.dat'
# str_mix2_2='data/SERS with mix analyte/mix/4027min\Mix-SERS-A-(2)-4027min_532nm_Newton_105um _ND1-51_20x-NA0.75_1500ms 1avg 2box (S-S-H-C)_Exported.dat'

# loader_on=1
# #all spectrums
# if loader_on:
    
#     #-----------------ACE-----------------
#     i_file= open(str_ACE, "r")
#     temp = i_file.readlines()
#     temp=[i.strip('\n') for i in temp]
#     data_ace=np.array([(row.split('\t')) for row in temp], dtype=np.float32)
    
#     f_sup=data_ace[:,0]
#     data_ace=data_ace[:,1:101]
    
#     #-----------------MG-----------------
#     i_file= open(str_MG, "r")
#     temp = i_file.readlines()
#     temp=[i.strip('\n') for i in temp]
#     data_mg=np.array([(row.split('\t')) for row in temp], dtype=np.float32)
    
#     f_sup_mg=data_mg[:,0]    
#     data_mg=data_mg[:,1:101]
    
#     #-----------------mix 1-----------------
#     i_file= open(str_mix1_1, "r")
#     temp = i_file.readlines()
#     temp=[i.strip('\n') for i in temp]
    
#     data_mix1_1=np.array([(row.split('\t')) for row in temp], dtype=np.float32)        
#     f_sup_m1=data_mix1_1[:,0]    
#     data_mix1_1=data_mix1_1[:,1:101]
    
#     i_file= open(str_mix1_2, "r")
#     temp = i_file.readlines()
#     temp=[i.strip('\n') for i in temp]
        
#     data_mix1_2=np.array([(row.split('\t')) for row in temp], dtype=np.float32)        
#     data_mix1_2=data_mix1_2[:,1:101]
    
#     #-----------------mix 2-----------------
    
#     i_file= open(str_mix2_1, "r")
#     temp = i_file.readlines()
#     temp=[i.strip('\n') for i in temp]
    
#     data_mix2_1=np.array([(row.split('\t')) for row in temp], dtype=np.float32)        
#     f_sup_m2=data_mix2_1[:,0]    
#     data_mix2_1=data_mix2_1[:,1:101]
    
#     i_file= open(str_mix2_2, "r")
#     temp = i_file.readlines()
#     temp=[i.strip('\n') for i in temp]
        
#     data_mix2_2=np.array([(row.split('\t')) for row in temp], dtype=np.float32)        
#     f_sup_m22=data_mix2_2[:,0]
#     data_mix2_2=data_mix1_2[:,1:101]
        
    
    
#     init_plot=0
    
#     if init_plot:
#         plt.figure('Data available recap')                
#         plt.plot(f_sup,np.mean(data_ace,axis=1),label='ACE')
#         plt.plot(f_sup_mg,np.mean(data_mg,axis=1),label='MG')
#         plt.plot(f_sup_mg,np.mean(data_mix1_1,axis=1),'--',label='MIX1_1')
#         plt.plot(f_sup_mg,np.mean(data_mix1_2,axis=1),'-.',label='MIX1_2')
#         plt.plot(f_sup,np.mean(data_mix2_1,axis=1),'-*',label='MIX2_1')
#         plt.plot(f_sup,np.mean(data_mix2_2,axis=1),'-|',label='MIX2_2')
#         plt.legend()

# #-----------------------------------------------------------
    
# # downsample everything down to the same frequencies between ~142 to ~~1742

# # min f 151.281
# # max f 1728.141


# data_ace_temp=data_ace[120:alg2,:]
# data_mix2_1_temp=data_mix2_1[120:alg2,:]
# data_mix2_2_temp=data_mix2_1[120:alg2,:]

# len_temp=alg2-120

# # the rest of the data is avareged 
# data_mg_temp     =np.zeros([len_temp,dim])
# data_mix1_1_temp =np.zeros([len_temp,dim])
# data_mix1_2_temp =np.zeros([len_temp,dim])



# # f_sup[120]
# # max(f_sup_mg)

# # do frequencies line up? NO
    
# # find the 
# alg1=np.argmin((f_sup_mg-f_sup[120])**2)
# alg2=np.argmin((f_sup-max(f_sup_mg))**2)


# s1=f_sup[120:alg2]
# s2=f_sup_mg[alg1:-1]

# # s1 is short, s2 is long
# plt.plot(s1-s2[:s1.size])
# plt.plot(s1,'*',label='s1')
# plt.plot(s2,'.',label='s2')
# plt.legend()
# # s1 is always larger than s2

# diff_vec=s1-s2[:s1.size]



# #----------------------------------------------------------------------
# # Subsample
# #----------------------------------------------------------------------




# while i<len_temp-1:    
#     delta_f_int=s1[i+1]-s1[i]
#     pos=np.where((s2>=n_feq) & (s2<=n_feq+delta_f_int))
    
#     # 
#     data_mg_temp[i]     =np.mean(data_mg[alg1+pos,:],axis=1)
#     data_mix1_1_temp[i] =np.mean(data_mix1_1[alg1+pos,:],axis=1)
#     data_mix1_2_temp[i] =np.mean(data_mix1_2[alg1+pos,:],axis=1)
#     #data_mix2_2_temp[i] =np.mean(data_mix2_2[alg1+pos,:],axis=1)
    
#     # update counter
#     i=i+1
#     n_feq=n_feq+delta_f_int

# sub_plot=1


# if sub_plot:
#     plt.figure('Data subsampling recap')                
#     plt.plot(s1,np.mean(data_ace_temp,axis=1),label='ACE')    
#     plt.plot(s1,np.mean(data_mg_temp,axis=1),label='MG')
#     plt.plot(s1,np.mean(data_mix1_1_temp,axis=1),'--',label='MIX1_1')
#     plt.plot(s1,np.mean(data_mix1_2_temp,axis=1),'-.',label='MIX1_2')
#     plt.plot(s1,np.mean(data_mix2_1_temp,axis=1),'.-',label='MIX2_1')
#     plt.plot(s1,np.mean(data_mix2_2_temp,axis=1),'--',label='MIX2_2')
#     plt.legend()
    

# #----------------------------------------------------------------------
# # Save everything
# #----------------------------------------------------------------------



# # # what do we keep? 
# # # the data that are already sparse we just cut down

# # data_ace_temp=data_ace[120:alg2,:]
# # data_mix2_1_temp=data_mix2_1[120:alg2,:]



# # n_feq=min(s1[0],s2[0])
# # # s1 has fewer elements, so you have to merge s2 into s1
# # n_feq_last=min(s1[-1],s2[-1])
# # cont=0
    
# # while n_feq<=n_feq_last:    
# #     delta_f_int=s1[cont+1]-s1[cont]
# #     pos=np.where((s2>=n_feq) & (s2<=n_feq+delta_f_int))
    
    
# #     data[i,:]=np.amax(data[pos[0],:],0)
# #     data_st[i]=np.amax(data_st[pos[0]],0)    
# #     # update counter
# #     i=i+1
# #     n_feq=n_feq+delta_f_int
        
    


# # f_sup_int=np.array(f_sup).astype(int)

# # # the lowest resolution is 2 wavenumbers 
# # delta_f_int=max(np.diff(f_sup_int))

# # #starting frequency-1
# # n_feq=min(f_sup_int)
# # n_feq_last=max(f_sup_int)

# # data_sub=np.zeros(((int((n_feq_last-n_feq)/delta_f_int)+1,dim)))
# # #
# # f_sup_sub=np.array(range(min(f_sup_int),max(f_sup_int)+1,delta_f_int))
# # i=0;

# # while n_feq<=n_feq_last:    
# #     # pos=np.where(f_sup_int==n_feq | f_sup_int==n_feq)    
# #     pos=np.where((f_sup_int>=n_feq) & (f_sup_int<=n_feq+delta_f_int))
# #     data[i,:]=np.amax(data[pos[0],:],0)
# #     data_st[i]=np.amax(data_st[pos[0]],0)    
# #     # update counter
# #     i=i+1
# #     n_feq=n_feq+delta_f_int

# # data=data[1:i+1,:]
# # data_st=data_st[1:i+1]

# # dim_sub=i

# # np.where(f_sup_mg==f_sup[120])

# # f_sup_temp=

# # np.find()
# # plt.plot(f_sup,'--')
# # plt.plot(f_sup_mg,'-.')
# # plt.plot(f_sup_m1,'-.')
# # plt.plot(f_sup_m2,'-.')
        

#     # #normalize the area to one
#     # #
#     # i_file= open('data/MG set 1/1500ppb_all_spectrum.dat', "r")
#     # temp = i_file.readlines()
#     # temp=[i.strip('\n') for i in temp]
#     # data1500=np.array([(row.split('\t')) for row in temp], dtype=np.float32)
#     # f_1500=data1500[:,0]
#     # data1500=data1500[:,1:101]
#     # I=[np.trapz(data1500[:,i],f_1500) for i in range(100)]
#     # data1500=data1500/I
#     # data1500=data1500.reshape([1600,10,10])
    
    
#     # i_file= open('data/MG set 1/15ppb_all_spectrum.dat', "r")
#     # temp = i_file.readlines()
#     # temp=[i.strip('\n') for i in temp]
#     # data15=np.array([(row.split('\t')) for row in temp], dtype=np.float32)
#     # f_15=data15[:,0]
#     # data15=data15[:,1:101]
#     # I=[np.trapz(data15[:,i],f_15) for i in range(100)]
#     # data15=data15/I
#     # data15=data15.reshape([1600,10,10])