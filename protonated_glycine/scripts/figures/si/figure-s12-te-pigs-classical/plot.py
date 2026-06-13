import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# Load Te-PIGS and classical
quantum = [np.loadtxt(f"spec_{i}.dat") for i in range(7)] # normal modes
classical = [np.loadtxt(f"classical_{i}.dat") for i in range(7)] # classical

fig, ax = plt.subplots(7, 1, sharex=True, figsize=(8, 10), dpi=300)

xrange = (2400, 4000)
baserange = (2400, 2800)

for i in range(7):

    # --- Classical ---
    base_classical = (classical[i][:,0] >= baserange[0]) & (classical[i][:,0] <= baserange[1])
    ymin_classical = classical[i][base_classical,1].min()

    mask_classical = (classical[i][:,0] >= xrange[0]) & (classical[i][:,0] <= xrange[1])
    ymax_classical = classical[i][mask_classical,1].max()

    ax[i].fill_between(classical[i][:,0], (classical[i][:,1] - ymin_classical) / ymax_classical, color="dodgerblue", alpha=0.6, label='Classical MB-nrg')

    # --- Te-PIGS ---
    base_quantum = (quantum[i][:,0] >= baserange[0]) & (quantum[i][:,0] <= baserange[1])
    ymin_quantum = quantum[i][base_quantum,1].min()

    mask_quantum = (quantum[i][:,0] >= xrange[0]) & (quantum[i][:,0] <= xrange[1])
    ymax_quantum = quantum[i][mask_quantum,1].max()

    ax[i].fill_between(quantum[i][:,0], (quantum[i][:,1] - ymin_quantum) / ymax_quantum, color="palevioletred", alpha=0.6, label='MB-nrg/Te-PIGS')


    # --- Settings ---
    ax[i].legend(handles=[Line2D([], [], linestyle='', color='none')], labels=[fr'GlyH$^{{+}}$(H$_2$O)$_{{{i}}}$'],
                 frameon=False, fontsize=16, loc='upper left', handlelength=0)

    ax[i].tick_params(axis="both", labelsize=12)
    ax[i].grid(True, linestyle="--", c='lightgray', alpha=0.7)
    ax[i].set_xlim(*xrange)
    ax[i].set_ylim(0, 1.05)

fig.supxlabel(r"$\omega$ (cm$^{-1}$)", fontsize=14)
fig.supylabel(r"$I(\omega)$", fontsize=14)

handles, labels = ax[0].get_legend_handles_labels()

fig.legend(
    handles, labels,
    loc='upper center',
    bbox_to_anchor=(0.5, 1.02),
    ncol=3,
    fontsize=12,
    frameon=False,
)

plt.tight_layout(rect=[0, 0, 1, 0.99])
plt.savefig("FigureS12.pdf", bbox_inches="tight")

