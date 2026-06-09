import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# Load Te-PIGS and classical
nm = [np.loadtxt(f"hf_{i}.dat") for i in range(7)] # normal modes
classical = [np.loadtxt(f"spec_{i}.dat") for i in range(7)] # classical

fig, ax = plt.subplots(7, 1, sharex=True, figsize=(8, 10), dpi=300)

xrange = (2400, 4000)
baserange = (2400, 2800)

for i in range(7):

    # --- Classical ---
    base_classical = (classical[i][:,0] >= baserange[0]) & (classical[i][:,0] <= baserange[1])
    ymin_classical = classical[i][base_classical,1].min()

    mask_classical = (classical[i][:,0] >= xrange[0]) & (classical[i][:,0] <= xrange[1])
    ymax_classical = classical[i][mask_classical,1].max()

    ax[i].fill_between(classical[i][:,0], (classical[i][:,1] - ymin_classical) / ymax_classical, color="dodgerblue", alpha=0.6)

    # --- Normal_mode ---
    mask_nm = (nm[i][:,0] >= xrange[0]) & (nm[i][:,0] <= xrange[1])
    ymax_nm = nm[i][mask_nm,1].max()
    
    for freq, inten in nm[i]:
        ax[i].vlines(x=freq, ymin=0, ymax=inten/ymax_nm, color="black", lw=1.1)

    # --- Settings ---
    ax[i].legend(handles=[Line2D([], [], linestyle='', color='none')], labels=[fr'GlyH$^{{+}}$(H$_2$O)$_{{{i}}}$'],
                 frameon=False, fontsize=16, loc='upper left', handlelength=0)

    ax[i].tick_params(axis="both", labelsize=12)
    ax[i].grid(True, linestyle="--", c='lightgray', alpha=0.7)
    ax[i].set_xlim(*xrange)
    ax[i].set_ylim(0, 1.05)

fig.supxlabel(r"$\omega$ (cm$^{-1}$)", fontsize=14)
fig.supylabel(r"$I(\omega)$", fontsize=14)

plt.tight_layout()
plt.savefig("FigureS11.pdf")

