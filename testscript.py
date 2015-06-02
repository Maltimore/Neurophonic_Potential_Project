import numpy as np
import matplotlib.pyplot as plt
import pyXdPhys as thomas
import os

relative_path = os.path.dirname(os.path.realpath(__file__))
A_filepath = relative_path + '/AAND_Data/A/872.08.4.itd'
stim_obj = xd.Stimulation(A_filepath)
traces = stim_obj.traces

plt.figure()
plt.plot(np.average(traces, axis=0))
