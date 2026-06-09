import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import matplotlib.image as mpimg

# List your three input files
files = ['tot_e_vs_nb.dat', 'delta.dat', 'delta_pgl.dat', 'delta_water.dat']
labels = ['All Interactions', r'GlyH$^+$- H$_2$O Interactions', 'H$_2$O - H$_2$O Interactions']
colors = ['deepskyblue', 'palevioletred', 'yellowgreen']

fig, axes = plt.subplots(1, 2, figsize=(12,4), gridspec_kw={'width_ratios' : [1, 2]}, dpi=300)

ax = axes[0]
data = np.loadtxt(files[0])
nb = data[1:,0]
ref = data[1:,1]
ax.bar(nb, np.abs(ref), width=0.2, color='deepskyblue')

yaxes = ax.get_ylim()


ax.set_ylabel(r"$|\epsilon|$ (kcal/mol)")
ax.set_xlim(1.5, 6.5)
ax.set_xticks([2, 3, 4, 5, 6], ["2B", "3B", "4B", "5B", "6B"])

img1 = mpimg.imread('/home/zsolomon/Pictures/mb_decomp.png')
ax.imshow(img1, aspect='auto', extent=[2.25, 6.25, 25, 78], alpha=1.0)

ax.set_ylim(yaxes)

ax = axes[1]

for fname, label, color in zip(files[1:], labels, colors):
    # Load data: nb, rmsd, min, max
    data = np.loadtxt(fname)
    nb = data[:,0]
    rmsd = data[:,1]
    ymin = data[:,2]
    ymax = data[:,3]
    
    # Error bars are distances from rmsd
    yerr = [rmsd - ymin, ymax - rmsd]
    
    ax.errorbar(
        nb, rmsd, yerr=yerr,
        fmt='*-', label=label, color=color, 
        ecolor=color,
        elinewidth=0.8,
        capsize=2
    )
    for cap in ax.collections:
        cap.set_alpha(0.35)

#    ax.errorbar(nb, rmsd, yerr=yerr, fmt='o-', label=label, color=color,
#                 capsize=3, markersize=5, linewidth=1.5)

ax.set_ylabel(r"$\Delta\epsilon_{n\mathrm{B}}$ (kcal/mol)")
ax.legend()
#ax.grid(True, linestyle="--", alpha=0.6)
ax.set_xlim(1.75, 6.25)
ax.set_ylim(-1, 1)
ax.axhline(0, ls='--', c='black', lw=1)
ax.set_xticks([2, 3, 4, 5, 6], ["2B", "3B", "4B", "5B", "6B"])



plt.tight_layout()
plt.savefig('FigureS1.pdf')
#plt.show()
