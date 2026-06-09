import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import glob
import os
from scipy.interpolate import make_interp_spline
from matplotlib.lines import Line2D
import matplotlib.image as mpimg
import re



input_files = sorted(glob.glob("*.dat"))
nplot = len(input_files)
dat = [np.loadtxt(input_files[i]) for i in range(nplot)]
image_path = './pics/'
img_files = sorted(glob.glob(image_path + '*stretch.png'))
lab = ['C8-O9', 'N4-H1', 'O10-H11', 'O9-H3', 'H1-O$_W$', 'H11-O$_W$']
pos = [[0.15, 0.74, 0.2, 0.2], [0.65, 0.71, 0.2, 0.2], [0.13, 0.43, 0.19, 0.19], [0.65, 0.4, 0.2, 0.2], [0.15, 0.05, 0.22, 0.22], [0.65, 0.01, 0.25, 0.25]]
lab2 = ['a', 'b', 'c', 'd', 'e', 'f']
span = np.loadtxt('min_max')
masks = [(0.9, 1.7), (0.6, 1.5), (0.7, 1.6)]


# d ref mb-nrg

fig, axes = plt.subplots(int(nplot / 2), 2, sharex=False, figsize=(10, 11), dpi=300)



# ---- PLOT ALL IN FOR LOOP ---- #

for i, ax in enumerate(axes.flatten()):	

	data = dat[i]

	img = mpimg.imread(img_files[i])
	newax = fig.add_axes(pos[i], anchor='NE')
	newax.imshow(img)
	newax.axis('off')
	
	if (i < 3):
		mask = masks[i]
		temp = (data[:,0] >= mask[0]) & (data[:,0] <= mask[1])
		data = data[temp,:]

	ax.scatter(data[:,0], data[:,1], label='RI-MP2/aug-cc-pVTZ', color='deepskyblue')
	newd = np.linspace(data[:,0][0], data[:,0][-1], 500)
	ax.plot(newd, make_interp_spline(data[:,0], data[:,2])(newd), label='MB-nrg', color='palevioletred')
	ax.axvspan(span[i][0], span[i][1], alpha=0.2, color='lightblue')
#	ax.axvspan(ax.get_xlim()[0], max(span[i][0], ax.get_xlim()[0]), alpha=0.6, color='lightblue')
#	ax.axvspan(min(span[i][1], ax.get_xlim()[1]), ax.get_xlim()[1], alpha=0.6, color='lightblue')

#	ax.set_xlabel(lab[i] + ' Distance (Å)')
	ax.set_xlabel('r ' + lab[i] + ' (Å)')
#	ax.set_xlabel(r'$r_{\small{%s}}$' % lab[i], fontsize=14)
	if (i % 2 == 0):
		ax.set_ylabel('Energy (kcal/mol)')
	#ax.set_title(lab[i] + ' Distance vs Energy')
	ax.set_xlim(min(data[:,0]) - 0.1, max(data[:,0]) + 0.1)
	ax.set_ylim(-0.1 * max(data[:,1]), max(data[:,1]) * 1.1)
	ax.text(-0.07, 1.05, '(' + lab2[i] + ')', transform=ax.transAxes, verticalalignment='top', horizontalalignment='left', fontsize=12)

#	ax.legend()

axes[2][0].set_ylim([-2, 58])
axes[0][0].set_ylim([-15, 150])

# ---- FULL PLOT SETTINGS ---- #

handles, labels = axes.flatten()[-1].get_legend_handles_labels()
fig.legend(handles, labels,
           loc='upper center',
           ncol=2,
           bbox_to_anchor=(0.5, 0.995),
           frameon=True)


plt.tight_layout(rect=[0, 0, 1, 0.97])
plt.savefig("Figure2.pdf")
#plt.savefig("all.png")



#plt.show()

