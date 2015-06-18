

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import correlate



# The code below ONLY works for .itd files
# load data into acceptable numpy format, using pyXdPhys library
traces       = stim_obj.traces
itds         = stim_obj.depvar # for itd files depvar corresponds to itds
stimulus     = stim_obj.stim
times        = stim_obj.times
stim_freq    = stim_obj.freqs

# make copies of the complete times, traces, stim before we shorten them to the
# relevant (stimulated) length
complete_times    = times.copy()
complete_traces   = traces.copy()
complete_stimulus = stimulus.copy()

# get the indices where the stimulus was played
time_indices = (times > 20) & (times < 100)
traces = traces[:,time_indices]
times = times[time_indices]
stimulus   = stimulus[:,time_indices]

plt.plot(complete_times, complete_traces[1])
plt.plot(complete_times, complete_stimulus[2])
plt.show()

correlation = correlate(traces[1,:],stimulus[1,:])

plt.plot(correlation)
plt.show()