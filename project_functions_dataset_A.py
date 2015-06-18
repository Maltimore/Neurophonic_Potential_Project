## Project -> put everything into functions

import numpy as np
import matplotlib.pyplot as plt
import pyXdPhys as thomas
import os
from scipy.signal import periodogram
from scipy.stats import mode

def plot_PSD_mult_freq(filepath, frequency):
    """
    Function apparently should only be used for the files in folder A!!!
    """
    
    # load data into acceptable numpy format, using pyXdPhys library
    stim_obj     = thomas.Stimulation(filepath)
    traces       = stim_obj.traces
    stim_freqs   = stim_obj.depvar
    stim         = stim_obj.stim
    times        = stim_obj.times    
    
    
    # get the indices where the stimulus was played
    time_indices = (times > 20) & (times < 100)
    traces = traces[:,time_indices]
    times = times[time_indices]
    stim   = stim[:,time_indices]
    
    # find the indices of the frequency parameter that was passed to this
    # function
    psd_plotting = []   
    counterplot  = 0
    for curr_freq in frequency:
        freq_indices = np.where(stim_freqs == curr_freq)[0]
       
        # compute psd of the traces that were stimulated with user_spec_freq
        psd_list = []
        for row_idx, freq_idx in enumerate(freq_indices):
            psd_freqs,  psd = periodogram(traces[freq_idx,:], fs=48077)
            psd_list.append(psd)
        psd = np.average(psd_list,axis=0)
        
        # plot PSD
        # zoom in to relevat frequency portion
        mask = (psd_freqs > np.min(frequency) - 500) & (psd_freqs < np.max(frequency) + 500)
        #zoomed_freq = psd_freqs[mask]
        psd_plotting.append(psd[mask])
        counterplot += 1        
        
        
    plt.figure(figsize =(12,8))
    for i in range(len(frequency)):
        cols = ['LightSkyBlue','MediumBlue','Black']
        plt.plot(psd_freqs[mask],psd_plotting[i],color = cols[i])#zoomed_freq, 
        plt.xlabel("Frequency [Hz]")
        plt.ylabel("PSD")
        plt.yscale('log')
    plt.legend(['Stimulation frequency: '+str(frequency[0])+' Hz',\
                'Stimulation frequency: '+str(frequency[1])+' Hz',\
                'Stimulation frequency: '+str(frequency[2])+' Hz'])  ### hard coded!

def plot_PSD_single_freq(filepath, frequency):
    """
    Function apparently should only be used for the files in folder A!!!
    """
    
    # load data into acceptable numpy format, using pyXdPhys library
    stim_obj     = thomas.Stimulation(filepath)
    traces       = stim_obj.traces
    stim_freqs   = stim_obj.depvar
    stim         = stim_obj.stim
    times        = stim_obj.times    
    
    # make copies of the complete times, traces, stim before we shorten them to the
    # relevant (stimulated) length
    complete_times  = times.copy()
    complete_traces = traces.copy()
    complete_stim   = stim.copy()
    
    # get the indices where the stimulus was played
    time_indices = (times > 20) & (times < 100)
    traces = traces[:,time_indices]
    times = times[time_indices]
    stim   = stim[:,time_indices]
    
    # find the indices of the frequency parameter that was passed to this
    # function
    freq_indices = np.where(stim_freqs == frequency)[0]
    
    # Plot averaged voltage trace (average over all trials)
    fig, (ax1,ax2) = plt.subplots(2,1)
    plt.tight_layout()
    ax1.plot(complete_times, np.average(complete_stim[freq_indices,:], axis=0))
    ax1.set_xlabel("Time [ms]")
    ax1.set_ylabel("stimulus intensity")
    ax1.set_title(str("stimulus and voltage trace averaged for frequency " +str(frequency) + " Hz"))
    ax2.plot(complete_times, np.average(complete_traces[freq_indices,:], axis=0))
    ax2.set_xlabel("Time [ms]")
    ax2.set_ylabel("Voltage [mV]")
    
    # compute psd of the traces that were stimulated with user_spec_freq
    psd_list = []
    for row_idx, freq_idx in enumerate(freq_indices):
        psd_freqs,  psd = periodogram(traces[freq_idx,:], fs=48077)
        psd_list.append(psd)
    psd = np.average(psd_list,axis=0)
    
    # plot PSD
    # zoom in to relevat frequency portion
    mask = (psd_freqs > frequency - 1000) & (psd_freqs < frequency + 1000)
    zoomed_freq = psd_freqs[mask]
    psd = psd[mask]
    plt.figure()
    plt.plot(zoomed_freq, psd)
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("PSD")
    plt.yscale('log')
    plt.title("Power Spectral density for stimulation with " + str(frequency) \
              + " Hz")

    return stim_obj
    
def frequency_tuning_plot(filepath):
    # load data into acceptable numpy format, using pyXdPhys library
    stim_obj     = thomas.Stimulation(filepath)
    traces       = stim_obj.traces
    stim_freqs   = stim_obj.depvar
    stim         = stim_obj.stim
    times        = stim_obj.times    
    
    # make copies of the complete times, traces, stim before we shorten them to the
    # relevant (stimulated) length
    complete_times  = times.copy()
    complete_traces = traces.copy()
    complete_stim   = stim.copy()
    
    # get the indices where the stimulus was played
    time_indices = (times > 20) & (times < 100)
    traces = traces[:,time_indices]
    times = times[time_indices]
    stim   = stim[:,time_indices]    
    
    # get all frequencies
    all_freqs = [stim_freqs[0]]
    for freq in stim_freqs:
        if not(freq in all_freqs):
            all_freqs.append(freq)
    all_freqs = np.array(all_freqs) # just making it a numpy array
    all_freqs = all_freqs[1:] # deleting first element (corresponding to no stimulation)

    margin = 8 # the margin around a frequency that we take to average psd
    psd_per_freq = np.zeros(len(all_freqs))
    
    ## loop over all frequencies
    for idx, current_freq in enumerate(all_freqs):
    
        freq_indices = np.where(stim_freqs == current_freq)[0]
        psd_list = []
        for freq_idx in freq_indices:
            psd_freqs,  psd = periodogram(traces[freq_idx,:], fs=48077)
            psd_list.append(psd)
        psd = np.average(psd_list,axis=0)
    
        # get indices of region around current_freq
        mask = (psd_freqs > current_freq - margin) & (psd_freqs < current_freq + margin)
        psd_per_freq[idx] = np.average(psd[mask])


    plt.figure()
    plt.plot(all_freqs, psd_per_freq)
    plt.xlabel("Stimulation frequency [Hz]")
    plt.ylabel("PSD peak value at corresponding trace")
    plt.title("Stimulation frequency vs. peak PSD at corresponding trace")
    
    return stim_obj
    
def itd_freq_tuning(filepath):
    
    # load data into acceptable numpy format, using pyXdPhys library
    stim_obj     = thomas.Stimulation(filepath)
    traces       = stim_obj.traces
    stim_freqs   = stim_obj.freqs
    itds         = stim_obj.depvar
    #stim         = stim_obj.stim
    #times        = stim_obj.times 
    
    # There's only one frequency that is used for Stimulation
    stimulation_freq = mode(stim_freqs)[0]

    # get all ITDs
    all_itds = np.sort(list(set(itds)))
    all_itds = all_itds[1:] # deleting first element (corresponding to no stimulation (-6666))
    
    # the margin around a frequency that we take to average PSD
    margin = 10 
    psd_per_itd = np.zeros(len(all_itds))
    
    ## loop over all ITDs
    for idx, current_itd in enumerate(all_itds):
    
        itd_indices = np.where(itds == current_itd)[0]
        psd_list = []
        for itd_idx in itd_indices:
            psd_itds,  psd = periodogram(traces[itd_idx,:], fs=48077)
            psd_list.append(psd)
        psd = np.average(psd_list,axis=0)
    
        # get indices of region around the stimulation frequency
        mask = (psd_itds > stimulation_freq - margin) & (psd_itds < stimulation_freq + margin)
        psd_per_itd[idx] = np.average(psd[mask])

    
    plt.figure()
    plt.plot(all_itds, psd_per_itd)
    plt.xlabel("Itd [mi]")
    plt.ylabel("PSD peak value at corresponding trace")
    plt.title("ITD vs. peak PSD at corresponding trace")
        
    return stim_obj, psd_per_itd


relative_path = os.path.dirname(os.path.realpath(__file__))
A1_filepath    = relative_path + '/AAND_Data/A/872.08.7.bf'
A2_filepath    = relative_path + '/AAND_Data/A/872.08.9.bf'

stim_obj = plot_PSD_single_freq(A1_filepath, 4750)
stim_obj = frequency_tuning_plot(A1_filepath)