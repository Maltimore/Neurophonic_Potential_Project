import numpy as np
import matplotlib.pyplot as plt
import pyXdPhys as thomas
import os
from scipy.signal import periodogram

plt.close('all')


# load data into acceptable numpy format, using pyXdPhys library
relative_path = os.path.dirname(os.path.realpath(__file__))
A_filepath = relative_path + '/AAND_Data/A/872.08.4.itd'
stim_obj = thomas.Stimulation(A_filepath)
traces = stim_obj.traces
depvar = stim_obj.depvar
stim   = stim_obj.stim
times  = stim_obj.times # I think the times are in the unit miliseconds.


# the get the indices where the stimulus was played
relevant_indices = (times > 20) & (times < 100)
traces = traces[:,relevant_indices]
times = times[relevant_indices]
stim   = stim[:,relevant_indices]

# Plot averaged voltage trace (average over all trials)
plt.figure()
plt.plot(times, np.average(traces, axis=0))
plt.xlabel("Time [ms]")
plt.ylabel("Voltage [mV]")
plt.title("Voltage trace averaged over all trials")

# compute psd of the three traces that were stimulated with "-300"
freqs,  psd1 = periodogram(traces[3,:], fs=48077)
freqs,  psd2 = periodogram(traces[4,:], fs=48077)
freqs,  psd3 = periodogram(traces[5,:], fs=48077)
psd = np.average(np.vstack((psd1,psd2,psd3)),axis=0)

# plot PSD
plt.figure()
plt.plot(freqs, psd)
plt.xlabel("Frequency [Hz]")
plt.ylabel("PSD")
plt.yscale('log')
plt.title("Power Spectral density for stimulation with xxx Hz")