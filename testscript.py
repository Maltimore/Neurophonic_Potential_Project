import numpy as np
import matplotlib.pyplot as plt
import pyXdPhys as thomas
import os
from scipy.signal import periodogram

# load data into acceptable numpy format, using pyXdPhys library
relative_path = os.path.dirname(os.path.realpath(__file__))
A_filepath = relative_path + '/AAND_Data/A/872.08.4.itd'
stim_obj = thomas.Stimulation(A_filepath)
traces = stim_obj.traces
depvar = stim_obj.depvar
stim   = stim_obj.stim
times  = stim_obj.times # I think the times are in the unit miliseconds.


# the get the indices where the stimulus was played
relevant_indices = stim != 0


plt.figure()
plt.plot(np.average(traces, axis=0))
first_three = np.average(traces[3:6,:],axis=0)
freqs,  psd1 = periodogram(traces[3,relevant_indices[3,:]], fs=48000)
freqs,  psd2 = periodogram(traces[4,relevant_indices[4,:]], fs=48000)
freqs,  psd3 = periodogram(traces[5,relevant_indices[5,:]], fs=48000)

psd = np.average(np.vstack((psd1,psd2,psd3)),axis=0)
#freqsfft = np.fft.fftfreq(len(first_three),d=1/5800)


plt.plot(freqs, psd)
#plt.xlim([0,400])
plt.xlabel("Frequency [Hz]")
plt.ylabel("PSD")
plt.title("Power Spectral density for stimulation with xxx Hz")

plt.figure()
plt.plot(times, stim[3,:])
plt.xlabel("Time [ms]")
plt.ylabel("Stimulus intensity")
plt.title("Entire stimulus trace")

plt.figure()
plt.plot(times, stim[3,:])
plt.xlim([7,15])
plt.xlabel("Time [ms]")
plt.ylabel("Stimulus intensity")
plt.title("An excerpt of a stimulus trace where we see the stimulus beginning")