import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import glob
import os
from scipy.interpolate import make_interp_spline
from matplotlib.lines import Line2D
import matplotlib.image as mpimg
import re
from matplotlib.gridspec import GridSpec


input_files = sorted(glob.glob("*.dat"))
nplot = len(input_files)
dat = [np.loadtxt(input_files[i]) for i in range(nplot)]
image_path = '/home/zsolomon/Pictures/si-energies/'
img_files = sorted(glob.glob(image_path + '*.png'))
#lab = ['C8-O9', 'N4-H1', 'O10-H11', 'O9-H3', 'H1-O$_W$', 'H11-O$_W$']
lab = ['N4-H1', 'O9-H3', 'O9-H3', 'C8-O9', 'O10-H11']
pos = [[0.15, 0.74, 0.2, 0.2], [0.65, 0.71, 0.2, 0.2], [0.13, 0.43, 0.19, 0.19], [0.65, 0.4, 0.2, 0.2], [0.15, 0.05, 0.22, 0.22], [0.65, 0.01, 0.25, 0.25]]
lab2 = ['a', 'b', 'c', 'd', 'e', 'f']
#span = [[1.1, 1.33], [0.9, 1.2], [0.86, 1.1], [1.25, 4.25], [1, 11], [1, 11]] 
#mask = [(0.8, 2.0), (0.6, 1.5), (0.6, 1.6)]
mask = [(0.6, 1.4), (1.7, 2.1), (1.0, 1.5), (0.8, 1.6)]
masklab = ['a', 'c', 'd', 'e']
# d ref mb-nrg

cols = (3, 2)

fig, axd = plt.subplot_mosaic(
    [
        ['a', 'a', 'b', 'b', 'c', 'c'],
        ['.', 'd', 'd', 'e', 'e', '.'],
    ],
    figsize=(14, 7),
    dpi=300,
    constrained_layout=False
)

# Put axes into a list matching your loop logic
axes1 = [axd['a'], axd['b'], axd['c']]
axes2 = [axd['d'], axd['e']]
ax = [axes1, axes2]

for label, ax_ in axd.items():
    if label != '.':
        ax_.text(
            -0.07, 1.05, f'({label})',
            transform=ax_.transAxes,
            fontsize=12,
            va='top', ha='left'
        )




# ---- PLOT ALL IN FOR LOOP ---- #

for i in range(2):
	for j in range(cols[i]):
		curr = 3 * i + j
		data = dat[curr]
		
		if lab2[curr] in masklab:
			this_mask = mask[masklab.index(lab2[curr])]
			temp = (data[:,0] >= this_mask[0]) & (data[:,0] <= this_mask[1])
			data = data[temp,:] 
	
		ax[i][j].scatter(data[:,0], data[:,1], label='RI-MP2/aug-cc-pVTZ', color='deepskyblue')
		newd = np.linspace(data[:,0][0], data[:,0][-1], 500)
		ax[i][j].plot(newd, make_interp_spline(data[:,0], data[:,2])(newd), label='MB-nrg', color='palevioletred')
		ax[i][j].plot(newd, make_interp_spline(data[:,0], data[:,3])(newd), label='Early Stage MB-nrg', color='yellowgreen')
	
		ax[i][j].set_xlabel('r ' + lab[curr] + ' (Å)')
		if (j == 0):
			ax[i][j].set_ylabel('Energy (kcal/mol)')
		ax[i][j].set_ylim(-0.1 * max(data[:,1]), max(data[:,1]) * 1.1)
	
		ax[1][0].set_ylim([-15, 160])
		
		yaxis = ax[i][j].get_ylim()
		xaxis = ax[i][j].get_xlim()

		img = mpimg.imread(img_files[curr])
		ax[i][j].imshow(img, aspect='auto', extent=[xaxis[0] + (xaxis[1] - xaxis[0])/5, xaxis[0] + 3.5 * (xaxis[1] - xaxis[0])/5, (yaxis[1] - yaxis[0])/3, 2.5 * (yaxis[1] - yaxis[0])/3], alpha=1.0)
		
		ax[i][j].set_ylim(yaxis)
		ax[i][j].set_xlim(xaxis)
		


# ---- FULL PLOT SETTINGS ---- #

handles, labels = ax[0][0].get_legend_handles_labels()

fig.legend(
    handles, labels,
    loc='upper center',
    bbox_to_anchor=(0.5, 1.0),
    ncol=3,
    fontsize=12,
    frameon=True,
)



plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig("FigureS3.pdf")

#plt.show()

