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
user_spec_freq = 5000
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