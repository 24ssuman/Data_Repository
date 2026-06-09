import numpy as np
import matplotlib.pyplot as plt

data1 = np.loadtxt('lcurve.out')

change_indices = np.where(np.diff(data1[:,5]) != 0)[0] + 1

plot_indices = np.concatenate(([0], change_indices))

filtered_x = data1[plot_indices, 0]
filtered_y = data1[plot_indices, 5]

plt.figure(figsize=(5, 4))

#plt.plot(data1[:,0], data1[:,4], ls='-', label='RMSE Forces Training', color='green')
#plt.plot(data1[:,0], data1[:,3], ls='-', label='RMSE Forces Validation', color='lightgreen')
plt.plot(filtered_x/100000, filtered_y*10000, linestyle='-', label='Total Loss', color='deepskyblue')
#plt.plot(data1[:,0], data1[:,5], linestyle='-', label='loss true', color='red')

#plt.ticklabel_format(style='sci', axis='both', scilimits=(0,0))
plt.xlabel(r'Number of Steps ($\times 10^5$)', fontsize=12)
plt.ylabel(r'Learning Rate ($\times 10^{-4}$)', fontsize=12)
#plt.legend(loc='best')
#plt.xscale('log')
#plt.xscale('symlog')
#plt.yscale('log')
#plt.grid()
plt.tight_layout()
plt.savefig('FigureS4.pdf', dpi=300)
#plt.show()
