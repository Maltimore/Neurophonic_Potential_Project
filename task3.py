import numpy as np
import matplotlib.pyplot as plt
import pyXdPhys as thomas
import os
from scipy.signal import periodogram
from scipy.stats import mode



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
        stimuli = stimuli[valid_inds*2,:]
    else:
        stimuli = stimuli[valid_inds*2+1,:]        
    
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
        correlation = np.correlate(stimuli[i,:],traces[i,:],'full')
        ft = np.fft.fft(correlation)
        freqs_ft = np.fft.fftfreq(len(correlation), dt)
        mask = np.where((freqs_ft > stim_freq - 3.) & (freqs_ft < stim_freq + 3.))[0]
        angles = np.angle(ft[mask])
        phases[i] = np.mean(angles)
    
    
    return phases

B1_clean = '/Users/hanna/Desktop/Neurophonic_Potential_Project/AAND_Data/B/016.13.10_clean.itd'
B2_clean = '/Users/hanna/Desktop/Neurophonic_Potential_Project/AAND_Data/B/016.14.11_clean.itd'
stim_obj_b2clean = thomas.Stimulation(B2_clean, depvar_sort = False)  
