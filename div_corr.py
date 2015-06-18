import numpy as np
import matplotlib.pyplot as plt

def div_corr(stim, trace, n_slices=2):
    #stim = stim[450:]    
    #trace = trace[450:]
    slices = []
    stims = []
    taus = []
    
    slice_len = int(len(trace)/n_slices)
    for i in range(0, n_slices):
        slices.append(trace[i*slice_len:(i+1)*slice_len])
        stims.append(stim[i*slice_len:(i+1)*slice_len])
        corr = np.correlate(stims[i], slices[i], mode = "same")
        #print(len(corr))        
        tau = np.argmax(corr) - (len(corr)/2)
        taus.append(tau)        
        plt.plot(corr)
        #plt.xlim(0,100)
        plt.figure()
    return corr, np.array(taus)

corr, c = div_corr(stim[0,:], traces[0,:], 10)
ft = np.fft.fft(corr)
psd = np.abs(ft)**2
angle = np.angle(ft) #in radians, don't forget to convert
#look for the bin that is the frequency
#plt.plot(stim[0,:])
