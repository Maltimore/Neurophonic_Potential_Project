# -*- coding: utf-8 -*-
# This script executes the functions from npp.py and generates plots for the
# presentation on the Neurophonic Potential in Barn Owls (AAND summer semester 
# 2015)
# Malte Esders, Hüseyin Camalan, Hanna Röhling

from npp import *

# To execute the following you need to be in the directory were the Ddataset is
# at (in a folder called AAND_Data)

# plotting subsequent PSDs for dataset A, bf files
A1_filepath     = os.getcwd()+'/AAND_Data/A/872.08.7.bf'
A1_filepath_itd = os.getcwd()+'/AAND_Data/A/872.08.4.itd'
plot_PSD_mult_freq(A1_filepath, [4500,5000,5500])

# plotting the frequency tuning 
stim_objA = frequency_tuning_plot(A1_filepath)

# plotting the ITD tuning
stim_objA, psdperitd = itd_freq_tuning(A1_filepath_itd)

# from here on we're going to use the dataset B
B1_clean = os.getcwd()+'/AAND_Data/B/016.13.10_clean.itd'
stim_obj_b1clean = thomas.Stimulation(B1_clean, depvar_sort = False)

# plotting PSDs for file from dataset B and choose the parameter stimulated
# according to whether you want to see the PSD for an un- or a stimulated
# portion of the traces
stim_obj = plot_PSD_itd(stim_obj_b1clean, stimulated=False)
stim_obj = plot_PSD_itd(stim_obj_b1clean, stimulated=True)

# now we want to analyze the phase stability for different ITDs

# first we're looking at the single trial variability
phases0, singleitd0, variance0 = get_phases_single(stim_obj_b1clean, 4, 0)
n_traces, n_slices = np.shape(phases0)

phases_centered0 = np.mean(phases0, axis = 0) - np.mean(phases0[:,0])
error_sd0 = np.std(phases0, axis = 0)

phases1, singleitd1, variance1 = get_phases_single(stim_obj_b1clean, 4, 1)
n_traces1, n_slices1 = np.shape(phases1)

phases_centered1 = np.mean(phases1, axis = 0) - np.mean(phases1[:,0])
error_sd1 = np.std(phases1, axis = 0)

plt.figure()
plt.errorbar(np.arange(n_slices)+1,phases_centered0, error_sd0, color ='Salmon')
plt.errorbar(np.arange(n_slices1)+1,phases_centered1, error_sd1, color ='b')
plt.xlim(0,5)
plt.legend(['ITD = '+str(singleitd1)+' $\mu$s','ITD = '+str(singleitd0)+' $\mu$s'])
plt.xlabel('slices')
plt.ylabel('corrected mean phase and standard deviation')

# now we're going to take a look at the inter trial variability
phase_test0, singleitd_test0 = get_phases(stim_obj_b1clean, index_itd = 0)
phase_test1, singleitd_test1 = get_phases(stim_obj_b1clean, index_itd = 1)

# Do regression and fit the phase information to the regression line
slope0, intercept0, residuals0 = regression_residuals(phase_test0)
slope1, intercept1, residuals1 = regression_residuals(phase_test1)

stim_freq = np.unique(stim_obj_b1clean.freqs)[np.where(np.unique(stim_obj_b1clean.freqs) != -6666)[0]][0]

ticks_lista = list(np.array([-np.pi,0.,np.pi]))
ticks_listb = list(np.round((ticks_lista/stim_freq)*10**3,2))

plt.figure()
plt.plot(phase_test0, 'Salmon')
plt.plot(phase_test1, 'Gold')
plt.plot(np.arange(len(phase_test0))*slope0+intercept0,'b')
plt.plot(np.arange(len(phase_test1))*slope1+intercept1,'b')
plt.legend(['ITD = '+str(singleitd_test0)+' $\mu$s','ITD = '+str(singleitd_test1)+' $\mu$s'])
plt.yticks(ticks_lista, ticks_listb)
plt.ylabel('phase [ms]')

ticks_listc = list(np.array([-np.pi/7.,-np.pi/14.,0.,np.pi/14.,np.pi/7.]))
ticks_listd = list(np.round((ticks_listc/stim_freq)*10**3,2))

plt.figure()
plt.plot(residuals0,'Salmon')
plt.plot(residuals1, 'Gold')
plt.xlabel('trials')
plt.ylabel('phase [ms]')
plt.legend(['ITD = '+str(singleitd_test0)+' $\mu$s','ITD = '+str(singleitd_test1)+' $\mu$s'])
plt.yticks(ticks_listc, ticks_listd)

# calculate and plot "standard deviation bars" 
std_single_0 = np.mean(np.std(phases0, axis = 1))
std_single_1 = np.mean(np.std(phases1, axis = 1))
std_across_0 = np.std(residuals0) 
std_across_1 = np.std(residuals1) 

std0 = np.array([std_single_0, std_across_0])
std1 = np.array([std_single_1, std_across_1])


ind = np.arange(2)
width = 0.35
fig, ax = plt.subplots()
rects1 = ax.bar(ind, std0, width, color='Salmon')
rects2 = ax.bar(ind+width, std1, width, color='b')

ticks_liste = list(np.array([0.,0.05,0.1,0.15, 0.2,0.25]))
ticks_listf = list(np.round((ticks_liste/stim_freq)*10**6,2))

ax.set_ylabel('standard deviation [$\mu$s]')
ax.set_xticks(ind+width)
ax.set_xticklabels( ('intra-trial', 'inter-trial') )
ax.legend( (rects1[0], rects2[0]), ('ITD = '+str(singleitd_test0)+' $\mu$s','ITD = '+str(singleitd_test1)+' $\mu$s') )
plt.title('Standard deviation of phase during single trials and across trials')
plt.yticks(ticks_liste, ticks_listf)

#as an alternative to the "mean across single trials" barplot, we can also look at the mean "maximum-minimum phase" in the different slices
maxmin_0 = np.mean(np.max(phases0, axis = 1) - np.min(phases0, axis = 1))
maxmin_1 = np.mean(np.max(phases1, axis = 1) - np.min(phases1, axis = 1))

ticks_listg = list(np.array([0.,0.2,0.4,0.6, 0.8]))
ticks_listh = list(np.round((ticks_liste/stim_freq)*10**6,2))

plt.figure(figsize = (3,4))
plt.bar([0.35,0.7], [maxmin_0, maxmin_1], width = 0.35, color = ['Salmon', 'b'])
plt.bar([0.7],[maxmin_1], width = 0.35, color = 'b')
plt.xlim(0.35,1.4)
plt.ylim(0,0.8)
plt.legend(['ITD = '+str(singleitd_test0)+' $\mu$s','ITD = '+str(singleitd_test1)+' $\mu$s'], loc = 'best')
plt.ylabel('mean max.phase - min.phase [$\mu$s]')
plt.xticks([0.7],['intra-trial'])
plt.yticks(ticks_listg, ticks_listh)