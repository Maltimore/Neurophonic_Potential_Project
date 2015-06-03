import numpy as np
import matplotlib.pyplot as plt
import pyXdPhys as thomas
import os
from scipy.signal import periodogram

plt.close('all')

relative_path = os.path.dirname(os.path.realpath(__file__))
A_filepath = relative_path + '/AAND_Data/A/872.08.4.itd'
stim_obj = thomas.Stimulation(A_filepath)
traces = stim_obj.traces[:,int(15*48.077):int(95*48.077)]
depvar = stim_obj.depvar
stim   = stim_obj.stim
times  = stim_obj.times # I think the times are in the unit miliseconds.
#plt.figure()
#plt.plot(np.average(traces, axis=0))
#first_three = np.average(traces[3:6,:],axis=0)
freqs,  psd1 = periodogram(traces[3,:], fs=48077)
freqs,  psd2 = periodogram(traces[4,:], fs=48077)
freqs,  psd3 = periodogram(traces[5,:], fs=48077)

psd = np.average(np.vstack((psd1,psd2,psd3)),axis=0)
#freqsfft = np.fft.fftfreq(len(first_three),d=1/5800)

plt.plot(freqs, psd)
#plt.xlim([0,400])
plt.xlabel("Frequency [Hz]")
plt.ylabel("PSD")
#plt.yscale('log')
plt.title("Power Spectral density for stimulation with xxx Hz")

plt.figure()
plt.plot(times, stim[3,:])
plt.xlabel("Time [ms]")
plt.ylabel("Stimulus intensity")
plt.title("Entire stimulus trace")

plt.figure()
plt.plot(times, stim[3,:])
plt.xlim([5,15])
plt.xlabel("Time [ms]")
plt.ylabel("Stimulus intensity")
plt.title("An excerpt of a stimulus trace where we see the stimulus beginning")