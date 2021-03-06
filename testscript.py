import numpy as np
import matplotlib.pyplot as plt
import pyXdPhys as thomas
import os
from scipy.signal import periodogram

plt.close('all')


# load data into acceptable numpy format, using pyXdPhys library
relative_path = os.path.dirname(os.path.realpath(__file__))
A_filepath    = relative_path + '/AAND_Data/A/872.08.9.bf'
stim_obj      = thomas.Stimulation(A_filepath)
traces        = stim_obj.traces
stim_freqs     = stim_obj.depvar
stim          = stim_obj.stim
times         = stim_obj.times # I think the times are in the unit miliseconds.


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

# select the stimulation frequency that you want plots for
### SELECT frequency here
user_spec_freq = 4750
freq_indices = np.where(stim_freqs == user_spec_freq)[0]


# Plot averaged voltage trace (average over all trials)
fig, (ax1,ax2) = plt.subplots(2,1)
plt.tight_layout()
ax1.plot(complete_times, np.average(complete_stim[freq_indices,:], axis=0))
ax1.set_xlabel("Time [ms]")
ax1.set_ylabel("stimulus intensity")
ax1.set_title(str("stimulus and voltage trace averaged for frequency " +str(user_spec_freq) + " Hz"))
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
mask = (psd_freqs > user_spec_freq - 1000) & (psd_freqs < user_spec_freq + 1000)
zoomed_freq = psd_freqs[mask]
psd = psd[mask]
plt.figure()
plt.plot(zoomed_freq, psd)
plt.xlabel("Frequency [Hz]")
plt.ylabel("PSD")
plt.yscale('log')
plt.title("Power Spectral density for stimulation with " + str(user_spec_freq) \
          + " Hz")
          





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
    for row_idx, freq_idx in enumerate(freq_indices):
        psd_freqs,  psd = periodogram(traces[freq_idx,:], fs=48077)
        psd_list.append(psd)
    psd = np.average(psd_list,axis=0)
    
    # get indices of region around current_freq
    mask = (psd_freqs > current_freq - margin) & (psd_freqs < current_freq + margin)
    psd_per_freq[idx] = np.average(psd[mask])


plt.figure()
plt.plot(all_freqs,psd_per_freq)
plt.xlabel("Stimulation frequency [Hz]")
plt.ylabel("PSD peak value at corresponding trace")
plt.title("Stimulation frequency vs. peak PSD at corresponding trace")