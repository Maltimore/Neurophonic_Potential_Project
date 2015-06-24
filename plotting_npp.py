# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 16:03:59 2015

@author: hanna
"""

# plotting errorbar
from task3 import *
from project_functions_dataset_B import *

B1_clean = '/Users/hanna/Desktop/Neurophonic_Potential_Project/AAND_Data/B/016.13.10_clean.itd'
B2_clean = '/Users/hanna/Desktop/Neurophonic_Potential_Project/AAND_Data/B/016.14.11_clean.itd' 
stim_obj_b1clean = thomas.Stimulation(B1_clean, depvar_sort = False)

# plotting subsequent PSDs for dataset A, bf files
A1_filepath = os.getcwd()+'/AAND_Data/A/872.08.7.bf'
plot_PSD_mult_freq(A1_filepath, [4500,5000,5500])


# plotting PSDs for dataset B
stim_obj = plot_PSD_itd(stim_obj_b1clean, stimulated=True)



phases0, singleitd0, variance0 = get_phases_single(stim_obj_b1clean, 4, 0)
n_traces, n_slices = np.shape(phases0)

phases_centered0 = np.mean(phases0, axis = 0) - np.mean(phases0[:,0])
error_sd0 = np.std(phases0, axis = 0)

phases1, singleitd1, variance1 = get_phases_single(stim_obj_b1clean, 4, 1)
n_traces1, n_slices1 = np.shape(phases1)

phases_centered1 = np.mean(phases1, axis = 0) - np.mean(phases1[:,0])
error_sd1 = np.std(phases1, axis = 0)

plt.figure()
plt.errorbar(np.arange(n_slices)+1,phases_centered0, error_sd0)
plt.errorbar(np.arange(n_slices1)+1,phases_centered1, error_sd1)
plt.xlim(0,5)
plt.legend(['ITD = '+str(singleitd0),'ITD = '+str(singleitd1)])
plt.xlabel('slices')

phase_test0, singleitd_test0 = get_phases(stim_obj_b1clean, index_itd = 0)
phase_test1, singleitd_test1 = get_phases(stim_obj_b1clean, index_itd = 1)
phase_test_centered0 = phase_test0 - phases0[:,0] # -phase_test0[0]
phase_test_centered1 = phase_test1 - phases1[:,0] # -phase_test1[1]

plt.figure()
plt.plot(phase_test_centered1, 'g')
plt.plot(phase_test_centered0, 'b')
plt.ylim(-1.2,0.4)
plt.legend(['ITD = '+str(singleitd_test1)+' $\mu$s','ITD = '+str(singleitd_test0)+' $\mu$s'])


# Do regression and fit the phase information to the regression line
slope0, intercept0, residuals0 = regression_residuals(phase_test0)
slope1, intercept1, residuals1 = regression_residuals(phase_test1)

plt.figure()
plt.plot(phase_test0)
plt.plot(np.arange(len(phase_test0))*slope0+intercept0)
plt.plot(phase_test1)
plt.plot(np.arange(len(phase_test1))*slope1+intercept1)
plt.legend(['ITD = '+str(singleitd_test0)+' $\mu$s','ITD = '+str(singleitd_test1)+' $\mu$s'])

plt.figure()
plt.plot(residuals0)
plt.plot(residuals1)
plt.legend(['ITD = '+str(singleitd_test0)+' $\mu$s','ITD = '+str(singleitd_test1)+' $\mu$s'])

# calculate and plot "variance bars" 
var_single_0 = np.mean(np.var(phases0, axis = 1))
var_single_1 = np.mean(np.var(phases1, axis = 1))
var_across_0 = np.var(residuals0) # centered or uncenetered?
var_across_1 = np.var(residuals1) # centered or uncenetered?

variances0 = np.array([var_single_0, var_across_0])
variances1 = np.array([var_single_1, var_across_1])


ind = np.arange(2)
width = 0.35
fig, ax = plt.subplots()
rects1 = ax.bar(ind, variances0, width, color='b')
rects2 = ax.bar(ind+width, variances1, width, color='g')

ax.set_ylabel('variance')
ax.set_xticks(ind+width)
ax.set_xticklabels( ('mean across single trials', 'across trials') )
ax.legend( (rects1[0], rects2[0]), ('ITD = '+str(singleitd_test0)+' $\mu$s','ITD = '+str(singleitd_test1)+' $\mu$s') )
plt.title('Variability of phase during single trials and across trials')

#as an alternative to the "mean across single trials" barplot, we can also look at the mean "maximum-minimum phase" in the different slices
maxmin_0 = np.mean(np.max(phases0, axis = 1) - np.min(phases0, axis = 1))
maxmin_1 = np.mean(np.max(phases1, axis = 1) - np.min(phases1, axis = 1))

plt.figure(figsize = (3,4))
plt.bar([0.35,0.7], [maxmin_0, maxmin_1], width = 0.35, color = ['Salmon', 'b'])
plt.bar([0.7],[maxmin_1], width = 0.35, color = 'b')
plt.xlim(0.35,1.4)
plt.ylim(0,0.8)
plt.legend(['ITD = '+str(singleitd_test0)+' $\mu$s','ITD = '+str(singleitd_test1)+' $\mu$s'], loc = 'best')
plt.ylabel('mean max.phase - min.phase')
plt.xticks([0.7],['mean across single trials'])
