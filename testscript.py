import numpy as np
import matplotlib.pyplot as plt
import pyXdPhys as thomas
import os
from scipy.signal import periodogram

plt.close('all')


# load data into acceptable numpy format, using pyXdPhys library
relative_path = os.path.dirname(os.path.realpath(__file__))
A_filepath = relative_path + '/AAND_Data/A/872.08.9.bf'
stim_obj = thomas.Stimulation(A_filepath)
traces = stim_obj.traces
depvar = stim_obj.depvar
stim   = stim_obj.stim
times  = stim_obj.times # I think the times are in the unit miliseconds.


# make copies of the complete times, traces, stim before we shorten them to the
# relevant (stimulated) length
complete_times  = times.copy()
complete_traces = traces.copy()
complete_stim   = stim.copy()

# the get the indices where the stimulus was played
relevant_indices = (times > 20) & (times < 100)
traces = traces[:,relevant_indices]
times = times[relevant_indices]
stim   = stim[:,relevant_indices]


# Plot averaged voltage trace (average over all trials)
fig, (ax1,ax2) = plt.subplots(2,1)
plt.tight_layout()
ax1.plot(complete_times, np.average(complete_stim[3:6,:], axis=0))
ax1.set_xlabel("Time [ms]")
ax1.set_ylabel("stimulus intensity")
ax1.set_title("Voltage trace averaged over all trials")
ax2.plot(complete_times, np.average(complete_traces[3:6,:], axis=0))
ax2.set_xlabel("Time [ms]")
ax2.set_ylabel("Voltage [mV]")
ax2.set_title("Voltage trace averaged over all trials")

# compute psd of the three traces that were stimulated with "-300"
stimulation_frequency = 5000
idxes = np.where(depvar == stimulation_frequency)[0]
freqs,  psd1 = periodogram(traces[idxes[0],:], fs=48077)
freqs,  psd2 = periodogram(traces[idxes[1],:], fs=48077)
freqs,  psd3 = periodogram(traces[idxes[2],:], fs=48077)
psd = np.average(np.vstack((psd1,psd2,psd3)),axis=0)

# plot PSD
plt.figure()
plt.plot(freqs, psd)
plt.xlabel("Frequency [Hz]")
plt.ylabel("PSD")
plt.yscale('log')
plt.title("Power Spectral density for stimulation with 2000 Hz")