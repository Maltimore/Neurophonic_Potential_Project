import numpy as np
import matplotlib.pyplot as plt
import pyXdPhys as thomas
import os
from scipy.signal import periodogram
from scipy.stats import mode

def get_phases_single(stim_obj, n_slices, ind_itd = 0):
    stimuli = stim_obj.stim
    traces  = stim_obj.traces
    freqs   = stim_obj.freqs
    depvar  = stim_obj.depvar
    true_times = stim_obj.times
    times   = stim_obj.times   
    
    time_indices = (times > 20.) & (times <  100.)
    traces       = traces[:,time_indices]
    times        = times[time_indices]
    stimuli      = stimuli[:,time_indices]
    
    valid_inds = np.where(freqs != -6666)[0]
    stimuli = stimuli[valid_inds*2,:]
    traces  = traces[valid_inds,:]
    freqs   = freqs[valid_inds]
    depvar  = depvar[valid_inds]
    
    single_itd = list(set(list(depvar)))[ind_itd] 
    
    itd_inds = np.where(depvar == single_itd)[0]
    
    stimuli = stimuli[itd_inds,:]
    traces  = traces[itd_inds,:]
    freqs   = freqs[itd_inds]
    depvar  = depvar[itd_inds]   
    
    
    dt = true_times[1]*10**(-3)
    n_traces, n_timepoints = np.shape(traces)   
    phases = np.zeros([n_traces, n_slices]) 
    slice_size = int(n_timepoints/n_slices) 
    
    for i in range(n_traces):
        for j in range(n_slices):
            stim_freq = freqs[i]
            correlation = np.correlate(stimuli[i,j*slice_size:(j+1)*slice_size],traces[i,j*slice_size:(j+1)*slice_size],'same')
            ft = np.fft.fft(correlation)
            freqs_ft = np.fft.fftfreq(len(correlation), dt)
            mask = np.where((freqs_ft > stim_freq - 3.) & (freqs_ft < stim_freq + 3.))[0]
            angles = np.angle(ft[mask])
            phases[i,j] = np.mean(angles)
            
    variance = np.zeros(n_traces)
    variance = np.var(phases, axis = 1)
    
    return phases, single_itd, variance
        
    
#phases, single_itd, variance = get_phases_single(stim_obj_b2clean, 4, ind_itd = 0)    
    

def get_phases(stim_obj, index_itd = 0):
    """
    INPUT:
    needs to be "clean", i.e. the number of stimulus traces needs to be twice
    the number of voltage traces
    """    
    stimuli = stim_obj.stim
    traces  = stim_obj.traces
    freqs   = stim_obj.freqs
    depvar  = stim_obj.depvar
    true_times = stim_obj.times
    times   = stim_obj.times    
    
    # get the indices where the stimulus was (definetely) played
    time_indices = (times > 20.) & (times <  100.)
    traces       = traces[:,time_indices]
    times        = times[time_indices]
    stimuli      = stimuli[:,time_indices]
    
    # get rid of non stimulated stimulus traces, voltage traces, freqs and depvar
    valid_inds = np.where(freqs != -6666)[0]
    
    single_itd = list(set(list(depvar)))[index_itd]
    
    if single_itd < 0:
        stimuli = stimuli[valid_inds*2+1,:]
    else:
        stimuli = stimuli[valid_inds*2,:]        
    
    traces  = traces[valid_inds,:]
    freqs   = freqs[valid_inds]
    depvar  = depvar[valid_inds]
    
    itd_inds = np.where(depvar == single_itd)[0]
    
    stimuli = stimuli[itd_inds,:]
    traces  = traces[itd_inds,:]
    freqs   = freqs[itd_inds]
    depvar  = depvar[itd_inds]    
    
    
    dt = true_times[1]*10**(-3)
    
    n_traces, n_timepoints = np.shape(traces)   
    phases = np.zeros(n_traces)    
    
    for i in range(n_traces):
        stim_freq = freqs[i]
        correlation = np.correlate(stimuli[i,:],traces[i,:],'same')
        ft = np.fft.fft(correlation)
        freqs_ft = np.fft.fftfreq(len(correlation), dt)
        mask = np.where((freqs_ft > stim_freq - 3.) & (freqs_ft < stim_freq + 3.))[0]
        angles = np.angle(ft[mask])
        phases[i] = np.mean(angles)
    
    
    return phases, single_itd

#B1_clean = '/Users/hanna/Desktop/Neurophonic_Potential_Project/AAND_Data/B/016.13.10_clean.itd'
#B2_clean = '/Users/hanna/Desktop/Neurophonic_Potential_Project/AAND_Data/B/016.14.11_clean.itd'
#stim_obj_b2clean = thomas.Stimulation(B2_clean, depvar_sort = False)  
#stim_obj_b1clean = thomas.Stimulation(B1_clean, depvar_sort = False)
#
#phase_b1_0, sitd_b1_0, variance0 = get_phases_single(stim_obj_b1clean, 4,0)
#phase_b1_1, sitd_b1_1, variance1 = get_phases_single(stim_obj_b1clean, 4,1)
#
#plt.figure()
#plt.plot(phase_b1_0)
#plt.plot(phase_b1_1)
#plt.xlabel('trials')
#plt.ylabel('phase [radians]')
#plt.title('data B, 1st file')
#plt.legend(['ITD ='+str(sitd_b1_0)+' $\mu$s', 'ITD ='+str(sitd_b1_1)+' $\mu$s'])
#
#
#phase_b2_0, sitd_b2_0 = get_phases(stim_obj_b2clean, index_itd = 0)
#phase_b2_1, sitd_b2_1 = get_phases(stim_obj_b2clean, index_itd = 1)
#
#
##np.mean(phases_b1_0,axis = 0)
##np.std(phases_b1_0,axis = 0)
#
#
#
#plt.figure()
#plt.plot(phase_b2_0)
#plt.plot(phase_b2_1)
#plt.xlabel('trials')
#plt.ylabel('phase [radians]')
#plt.legend(['ITD ='+str(sitd_b2_0)+' $\mu$s', 'ITD ='+str(sitd_b2_1)+' $\mu$s'])
#plt.title('data B, 2nd file')
#
#plt.figure()
#for i in range(10):
#    plt.plot(phases[i,:], 'b')
#    #plt.plot(phases1[i,:], 'r')
#    plt.xticks(np.linspace(0,4,5), ["1", "2", "3", "4", "5"])
#    plt.xlim(0,3)
#    plt.xlabel('number of slice')
#    plt.ylabel('phase [radians]')
#plt.legend(['ITD = '+str(singleitd0),'ITD = '+str(singleitd1)])
#
#plt.figure()
#plt.plot(variance0)
#plt.plot(variance1)
#plt.xlabel('number of trial')
#plt.ylabel('variance of phases in single trial')
#plt.legend(['ITD = '+str(singleitd0),'ITD = '+str(singleitd1)])
#plt.title('number of slices per trial: 4')
#
#
#err0 = np.std(phase_b1_0, axis = 0)
#err1 = np.std(phase_b1_1, axis = 0)
#plt.errorbar(np.arange(1,5),np.mean(phase_b1_0, axis = 0), err0)
#plt.errorbar(np.arange(1,5),np.mean(phase_b1_1, axis = 0), err1)
#plt.xlim(0,5)
#
#
## compare average of best ITD for the first 250 and the last 250 traces
#stimuli = stim_obj_b1clean.stim
#traces  = stim_obj_b1clean.traces
#freqs   = stim_obj_b1clean.freqs
#depvar  = stim_obj_b1clean.depvar
#true_times = stim_obj_b1clean.times
#times   = stim_obj_b1clean.times 
#
## extract the indices for the "good" itd
#rel_itd = np.where(depvar == 8)[0]
#rel_traces = traces[rel_itd,:]
#rel_traces1 = rel_traces[:50,:]
#rel_traces2 = rel_traces[125:250,:]
#rel_traces3 = rel_traces[250:375,:]
#rel_traces4 = rel_traces[450:500,:]
#av_traces1 = np.mean(rel_traces1, axis = 0)
#av_traces2 = np.mean(rel_traces2, axis = 0)
#av_traces3 = np.mean(rel_traces3, axis = 0)
#av_traces4 = np.mean(rel_traces4, axis = 0)
#
#plt.figure()
#plt.plot(av_traces1)
##plt.plot(av_traces2)
##plt.plot(av_traces3)
#plt.plot(av_traces4)
##plt.plot(stimuli[10,:])
#plt.xlabel('time')
#plt.ylabel('signal')
#plt.xlim(900,1000)
#plt.legend(['average over traces 1-125','average over traces 376-500'])
##plt.xlim(900,1000)
#
#plt.figure()
#plt.plot(av_traces1)
#plt.plot(av_traces2)
##plt.plot(stimuli[10,:])
#plt.xlabel('time')
#plt.ylabel('signal')
#plt.legend(['average over traces 1-250','average over traces 251-500'])
#plt.xlim(900,1000)
