## Project -> put everything into functions

import numpy as np
import matplotlib.pyplot as plt
import pyXdPhys as thomas 
import os
from scipy.signal import periodogram
from scipy.stats import mode, linregress

def plot_PSD_itd(stim_obj, stimulated=True):
    """
    Function apparently should only be used for the files in folder A!!!
    """
    
    # load data into acceptable numpy format, using pyXdPhys library
    traces       = stim_obj.traces
    itds         = stim_obj.depvar # these are the ITDs in .itd files
    stim         = stim_obj.stim
    times        = stim_obj.times 
    freqs        = stim_obj.freqs
    
    # make copies of the complete times, traces, stim before we shorten them to the
    # relevant (stimulated) length
    complete_times  = times.copy()
    complete_traces = traces.copy()
    complete_stim   = stim.copy()
    
    # get the indices where the stimulus was played
    if stimulated:
        lowerbound = 20
        upperbound = 100
    else:
        lowerbound = 120
        upperbound = 200
        
    time_indices = (times > lowerbound) & (times < upperbound)
    traces = traces[:,time_indices]
    times = times[time_indices]
    stim   = stim[:,time_indices]
    
    single_itds = list(set(itds))
    single_itds.remove(-6666) # remove the unstimulated trials
    psds = []
    for itd in single_itds:
        # find the indices of the frequency parameter that was passed to this
        # function
        itd_indices = np.where(itds == itd)[0]
        
        print(single_itds)
        print("Averaging over " +str(len(itd_indices))+ " trials for " \
              + "itd " +str(itd))
        
        # Plot averaged voltage trace (average over all trials)
        fig, (ax1,ax2) = plt.subplots(2,1)
        plt.tight_layout()
        ax1.plot(complete_times, np.average(complete_stim[itd_indices,:], axis=0))
        ax1.set_xlabel("Time [ms]")
        ax1.set_ylabel("stimulus intensity")
        ax1.set_title(str("stimulus and voltage trace averaged for itd " +str(itd) + " Hz"))
        ax2.plot(complete_times, np.average(complete_traces[itd_indices,:], axis=0))
        ax2.set_xlabel("Time [ms]")
        ax2.set_ylabel("Voltage [mV]")
        plt.show()
        
        frequency = mode(freqs)[0]
        
        # compute psd of the traces that were stimulated with user_spec_freq
        psd_list = []
        for row_idx, freq_idx in enumerate(itd_indices):
            psd_freqs,  psd = periodogram(traces[freq_idx,:], fs=48077)
            psd_list.append(psd)
        psd = np.average(psd_list,axis=0)
        psds.append(psd)
        # plot PSD
        # zoom in to relevat frequency portion
    #    mask = (psd_freqs > frequency - 1000) & (psd_freqs < frequency + 1000)
    #    zoomed_freq = psd_freqs[mask]
    #    psd = psd[mask]
        plt.figure()
        plt.plot(psd_freqs[:800], psd[:800])
        plt.xlabel("Frequency [Hz]")
        plt.ylabel("PSD")
        plt.yscale('log')
        plt.ylim(10**-1,10**6)
        if stimulated == True:
            plt.title("Power Spectral density for stimulation with " + str(frequency[0]) \
                  + " Hz,"+" ITD = "+str(itd))
        else:
            plt.title("Power Spectral density for no stimulation")            
        
    plt.figure(figsize = (12,8))
    plt.plot(psd_freqs[:800], psds[0][:800], color = 'Salmon')
    plt.plot(psd_freqs[:800],psds[1][:800], color = 'b')
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("PSD")
    plt.yscale('log')
    plt.ylim(10**-1,10**6)            
    plt.title("Power Spectral density for stimulation with " + str(frequency[0]) \
                  + " Hz")
    plt.legend(['ITD = '+str(single_itds[0])+' $\mu$s','ITD = '+str(single_itds[1])+' $\mu$s'])
    
    
    return stim_obj

def regression_residuals(phases):
    
    num_traces = len(phases)
    x = np.arange(num_traces)

    slope, intercept, r_value, p_value, std_err = linregress(x,phases)
    residuals = phases - (intercept + slope*x)
    
    return slope, intercept, residuals
          
#def frequency_tuning_plot(filepath):
#    # load data into acceptable numpy format, using pyXdPhys library
#    stim_obj     = thomas.Stimulation(filepath)
#    traces       = stim_obj.traces
#    stim_freqs   = stim_obj.depvar
#    stim         = stim_obj.stim
#    times        = stim_obj.times    
#    
#    # make copies of the complete times, traces, stim before we shorten them to the
#    # relevant (stimulated) length
#    complete_times  = times.copy()
#    complete_traces = traces.copy()
#    complete_stim   = stim.copy()
#    
#    # get the indices where the stimulus was played
#    time_indices = (times > 20) & (times < 100)
#    traces = traces[:,time_indices]
#    times = times[time_indices]
#    stim   = stim[:,time_indices]    
#    
#    # get all frequencies
#    all_freqs = [stim_freqs[0]]
#    for freq in stim_freqs:
#        if not(freq in all_freqs):
#            all_freqs.append(freq)
#    all_freqs = np.array(all_freqs) # just making it a numpy array
#    all_freqs = all_freqs[1:] # deleting first element (corresponding to no stimulation)
#
#    margin = 8 # the margin around a frequency that we take to average psd
#    psd_per_freq = np.zeros(len(all_freqs))
#    
#    ## loop over all frequencies
#    for idx, current_freq in enumerate(all_freqs):
#    
#        freq_indices = np.where(stim_freqs == current_freq)[0]
#        psd_list = []
#        for freq_idx in freq_indices:
#            psd_freqs,  psd = periodogram(traces[freq_idx,:], fs=48077)
#            psd_list.append(psd)
#        psd = np.average(psd_list,axis=0)
#    
#        # get indices of region around current_freq
#        mask = (psd_freqs > current_freq - margin) & (psd_freqs < current_freq + margin)
#        psd_per_freq[idx] = np.average(psd[mask])
#
#
#    plt.figure()
#    plt.plot(all_freqs, psd_per_freq)
#    plt.xlabel("Stimulation frequency [Hz]")
#    plt.ylabel("PSD peak value at corresponding trace")
#    plt.title("Stimulation frequency vs. peak PSD at corresponding trace")
#    
#    return stim_obj
#    
#def itd_freq_tuning(filepath):
#    
#    # load data into acceptable numpy format, using pyXdPhys library
#    stim_obj     = thomas.Stimulation(filepath)
#    traces       = stim_obj.traces
#    stim_freqs   = stim_obj.freqs
#    itds         = stim_obj.depvar
#    #stim         = stim_obj.stim
#    #times        = stim_obj.times 
#    
#    # There's only one frequency that is used for Stimulation
#    stimulation_freq = mode(stim_freqs)[0]
#
#    # get all ITDs
#    all_itds = np.sort(list(set(itds)))
#    all_itds = all_itds[1:] # deleting first element (corresponding to no stimulation (-6666))
#    
#    # the margin around a frequency that we take to average PSD
#    margin = 10 
#    psd_per_itd = np.zeros(len(all_itds))
#    
#    ## loop over all ITDs
#    for idx, current_itd in enumerate(all_itds):
#    
#        itd_indices = np.where(itds == current_itd)[0]
#        psd_list = []
#        for itd_idx in itd_indices:
#            psd_itds,  psd = periodogram(traces[itd_idx,:], fs=48077)
#            psd_list.append(psd)
#        psd = np.average(psd_list,axis=0)
#    
#        # get indices of region around the stimulation frequency
#        mask = (psd_itds > stimulation_freq - margin) & (psd_itds < stimulation_freq + margin)
#        psd_per_itd[idx] = np.average(psd[mask])
#
#    
#    plt.figure()
#    plt.plot(all_itds, psd_per_itd)
#    plt.xlabel("Itd [mi]")
#    plt.ylabel("PSD peak value at corresponding trace")
#    plt.title("ITD vs. peak PSD at corresponding trace")
#        
#    return stim_obj, psd_per_itd


#relative_path = os.getcwd()
#B1_filepath    = relative_path + '/AAND_Data/B/016.13.10.itd'
#B2_filepath    = relative_path + '/AAND_Data/B/016.14.11.itd'



#stim_obj     = thomas.Stimulation(B1_filepath)
#stim_obj = plot_PSD_itd(stim_obj, stimulated=True)
