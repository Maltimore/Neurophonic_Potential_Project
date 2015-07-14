# This file contains all functions used in the Neurophonic Potential Project
# (AAND summer semester 2015)
# Malte Esders, Hüseyin Camalan, Hanna Röhling

import numpy as np
import matplotlib.pyplot as plt
import pyXdPhys as thomas
import os
from scipy.signal import periodogram
from scipy.stats import mode, linregress


def plot_PSD_mult_freq(filepath, frequency):
    """
    Function plots subsequent PSDs of the traces stimulated by the 
    frequencies given by the input parameter frequency
    
    INPUT:
    filepath:  Filepath to one of the bf files from dataset A
    frequency: list of exactly three different stimulation frequencies 
               (must be valid)
    ---------------------------------------------------------------------------
    OUTPUT: no explicit output, but plots are being generated within the 
            function
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
        
        
    
    plt.figure(figsize = (12,8))
    cols = ['Salmon','MediumBlue','Black']
    plt.plot(psd_freqs[mask],psd_plotting[0],color = cols[0])#zoomed_freq, 
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("PSD")
    plt.yscale('log')
    plt.legend(['Stimulation frequency: '+str(frequency[0])+' Hz'])  ### hard coded!
    plt.plot(np.ones(100)*frequency[0],np.linspace(1,10**4,100),'--r')
    
    plt.figure(figsize = (12,8))
    for i in range(2):
        cols = ['Salmon','MediumBlue']
        plt.plot(psd_freqs[mask],psd_plotting[i],color = cols[i])#zoomed_freq, 
        plt.xlabel("Frequency [Hz]")
        plt.ylabel("PSD")
        plt.yscale('log')
        plt.legend(['Stimulation frequency: '+str(frequency[0])+' Hz',\
                'Stimulation frequency: '+str(frequency[1])+' Hz'])  ### hard coded!
    plt.plot(np.ones(100)*frequency[0],np.linspace(1,10**4,100),'--r')
    plt.plot(np.ones(100)*frequency[1],np.linspace(1,10**4,100),'--r')

    
    plt.figure(figsize = (12,8))
    for i in range(len(frequency)):
        cols = ['Salmon','MediumBlue','Black']
        plt.plot(psd_freqs[mask],psd_plotting[i],color = cols[i])#zoomed_freq, 
        plt.xlabel("Frequency [Hz]")
        plt.ylabel("PSD")
        plt.yscale('log')
        plt.legend(['Stimulation frequency: '+str(frequency[0])+' Hz',\
                'Stimulation frequency: '+str(frequency[1])+' Hz',\
                'Stimulation frequency: '+str(frequency[2])+' Hz'])  ### hard coded!
    plt.plot(np.ones(100)*frequency[0],np.linspace(1,10**4,100),'--r')
    plt.plot(np.ones(100)*frequency[1],np.linspace(1,10**4,100),'--r')
    plt.plot(np.ones(100)*frequency[2],np.linspace(1,10**4,100),'--r')



def plot_PSD_single_freq(filepath, frequency):
    """
    Function plots PSD of the traces stimulated with the frequency given in the 
    parameter frequency
    
    INPUT:
    filepath: Filepath to one of the bf files from dataset A
    frequency: single (valid) stimulation frequency
    ---------------------------------------------------------------------------
    OUTPUT:
    stim_obj: The stimulation object used for the computations
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
    """
    Function computes and plots the frequency tuning plot of the respective .bf
    file
    
    INPUT:
    filepath: Filepath to one of the bf files from dataset A
    ---------------------------------------------------------------------------
    OUTPUT:
    stim_obj: The stimulation object used for the computations
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
    """
    generates an ITD tuning plot
    
    INPUT:
    filepath: filepath to an ITD file of the A folder
    ---------------------------------------------------------------------------
    OUTPUT:
    stim_obj: The stimulation object used for the computations
    psd_per_itd: The power spectral density at the respective ITD value
    """
    
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
    plt.xlabel("ITD [$\mu$s]")
    plt.ylabel("PSD value around stimulation frequency "+str(stimulation_freq[0])+' Hz')
    plt.title("ITD vs. peak PSD")
        
    return stim_obj, psd_per_itd

def plot_PSD_itd(stim_obj, stimulated=True):
    """
    generates plots of 
    
    INPUT:
    stim_obj: Stimulation object created out of one of the ITD files of the B 
              folder
    stimulated: Using a stimulated portion of the signal (True) or an 
                unstimulated one (False)
    ---------------------------------------------------------------------------
    OUTPUT:
    stim_obj: The stimulation object used for the computations
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
    """
    conducts a linear regression on the phases extracted with get_phases()
    
    INPUT: 
    phases: Phase differences computed by function get_phases
    ---------------------------------------------------------------------------
    OUTPUT:
    slope: Slope of the regression line
    intercept: Intercept of the regression line
    residuals: Respective residuals between phases and the regression line   
    """
    num_traces = len(phases)
    x = np.arange(num_traces)

    slope, intercept, r_value, p_value, std_err = linregress(x,phases)
    residuals = phases - (intercept + slope*x)
    
    return slope, intercept, residuals

def get_phases_single(stim_obj, n_slices, ind_itd = 0):
    """
    computes phases for a single trial in order to be able to analyze 
    intra-trial stability
    
    INPUT: 
    stim_obj: stimulation object created out of one of the ITD files of the B 
              folder
    n_slices: number of 'slices' the single trial is supposed to be divided 
              into
    ind_itd: determines the ITD value used (apart from -6666 there are only two
             so ind_itd should either be 0 or 1)
    ---------------------------------------------------------------------------
    OUTPUT:
    phases: phase differences for the individual slices
    single_itd: the actual ITD that is used
    variance: variance between the phases
    """
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
    

def get_phases(stim_obj, index_itd = 0):
    """
    computes phases across trials in order to be able to analyze 
    inter-trial stability
    
    INPUT: 
    stim_obj: stimulation object created out of one of the ITD files of the B 
              folder
    index_itd: determines the ITD value used (apart from -6666 there are only two
             so ind_itd should either be 0 or 1)
    ---------------------------------------------------------------------------
    OUTPUT:
    phases: phase differences for each individual trial
    single_itd: the actual ITD that is used
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