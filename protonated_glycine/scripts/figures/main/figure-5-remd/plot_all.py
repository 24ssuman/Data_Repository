import os,sys
import glob
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from matplotlib import rcParams
import matplotlib as mpl



input_files = sorted(glob.glob("*.dat"))
nplot = len(input_files)
dat = [np.loadtxt(input_files[i]) for i in range(nplot)]


# Markers
markers = ['o','s','v','^','<','>','P','x','X','D','d','p','*','+','1','2','3','4']
colors = ['r', 'b', 'g', 'c', 'm', 'tab:olive']
names = ['A', 'B', 'C', 'D', 'E', 'F']

rcParams['font.family'] = 'Helvetica'

# Now the plot itself
fig, axes = plt.subplots(2, int(nplot / 2), figsize=(12,6), sharex=True, sharey=True)


for i, ax in enumerate(axes.flatten()):	

	legends = []
	data = dat[i]
	if i != 5:
		data = data[:25,]
	ax.plot(data[:,0], 1 - np.sum(data[:,1:len(data[0])], axis=1),  marker=markers[len(data[0]) - 1], color='darkgrey', linestyle='--', linewidth=1.5, markersize=0, label='Others')
	#legends.append('Other Isomers')		
	for j in range(len(data[0]) - 1):
		ax.plot(data[:,0], data[:,j + 1], marker=markers[j], color=colors[j], linestyle='-', linewidth=1.5, markersize=3, label=str(i + 1) + names[j])
		#legends.append('Isomer {}'.format(names[j]))

	handles, labels = ax.get_legend_handles_labels()
	# sort both labels and handles by labels
	labels, handles = zip(*sorted(zip(labels, handles), key=lambda t: t[0]))
	ax.legend(handles, labels, loc='upper right')	

	ax.set_xlim(0, 215)
	ax.set_ylim([-0.05,1.05])
#	ax.set_title('REMD For PGL + ' + str(i + 1) + ' Waters')
#	ax.legend(legends, loc='upper right')
	ax.grid(True, linestyle="--", c='lightgray', alpha=0.7)
	ax.text(0.07, 0.93, fr'GlyH$^{{+}}$(H$_2$O)$_{{{i + 1}}}$', transform=ax.transAxes, verticalalignment='top', horizontalalignment='left')
	if i // (nplot // 2) == 1:
	   ax.set_xlabel('Temperature (K)', fontsize=12)

#fig.supxlabel('Temperature (K)')
fig.supylabel('Fraction of Population', fontsize=12)

#handles, labels = axes.flatten()[-1].get_legend_handles_labels()
#fig.legend(handles, labels,
#           loc='upper center',
#           ncol=6,
#           bbox_to_anchor=(0.5, 0.995),
#           frameon=True)

#Tight layout
plt.tight_layout()

#Save images
#plt.savefig('Figure5.png', dpi=1000)
plt.savefig('Figure5.pdf', dpi=1000)
plt.show()
