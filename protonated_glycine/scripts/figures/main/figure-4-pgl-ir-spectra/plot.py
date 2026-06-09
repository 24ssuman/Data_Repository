import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

# -----------------------------
# Load theory and experiment
# -----------------------------
new = np.loadtxt(f"ir.dat")
classical = np.loadtxt(f"classical.dat")
exp = np.loadtxt(f"experimental.dat")
nm = np.loadtxt("hf.dat")

x1 = (1400, 1900)
x2 = (2400, 3800)
xrange = (1400, 3800)
baserange = (2400, 2800)
range = (3600, 3800)


fig, ax = plt.subplots(2, 2, sharey=True, figsize=(8, 5), gridspec_kw={'hspace': 0.1, 'wspace': 0.04, 'width_ratios': [x1[1]-x1[0], x2[1]-x2[0]]})

# -----------------------------
# Colors for each chemical entity
# -----------------------------
colors2 = {
    r"Free GlyH$^+$ O-H": "darkgreen",
    "Free N-H": "darkred",
    "Internal H-bonded N-H": "red",
    "C-H": "orange",
    "Others": "palevioletred"
}

colors = {
    "free_water_OH": "darkblue",
    "hb_water_OH": "deepskyblue",
    "free_PGL_OH": "darkgreen",
    "hb_PGL_OH": "limegreen",
    "free_NH": "darkred",
    "int_Hbond_NH": "red",
    "water_Hbond_NH": "lightcoral",
    "CH": "orange",
    "else":"palevioletred"
}

# -----------------------------
# Frequency windows per system
# -----------------------------

new_col = [  # H2O_0
        (3500, 3800, "free_PGL_OH"),
        (3300, 3500, "free_NH"),
        (3010, 3300, "CH"),
        (2900, 3010, "int_Hbond_NH"),
        (1400, 2900, "else")
        ]

# -----------------------------
# -----------------------------
# Plotting loop
# -----------------------------
# --- Experimental ---
ax1 = ax[0, 0]
ax2 = ax[0, 1]

mask_exp = (exp[:,0] >= xrange[0]) & (exp[:,0] <= xrange[1])
ymax_exp = exp[mask_exp,1].max()
ax1.fill_between(exp[:,0], exp[:,1] / ymax_exp, color="darkgray", alpha=0.5)
ax2.fill_between(exp[:,0], exp[:,1] / ymax_exp, color="darkgray", alpha=0.5)
#ax1.legend(handles=[Line2D([], [], linestyle='', color='none')],
#          labels=[fr'GlyH$^{{+}}$(H$_2$O)$_{{{0}}}$'],
#          frameon=False, fontsize=14, loc='upper left', handlelength=0)

fig.text(
    0.5, 0.82,                        # x=0.5 is center, y=0.97 is near top
    r"GlyH$^{+}$(H$_2$O)$_0$",        # your text
    ha="center", va="top",            # center horizontally, top-align vertically
    fontsize=14
)

base_theory = (new[:,0] >= baserange[0]) & (new[:,0] <= baserange[1])
ymin_theory = new[base_theory,1].mean()

mask_theory = (new[:,0] >= xrange[0]) & (new[:,0] <= xrange[1])
ymax_theory = (new-ymin_theory)[mask_theory,1].max()

xn = new[:,0] 
yn = (new[:,1] - ymin_theory) / ymax_theory 

ax1.set_xlim(*x1)
ax2.set_xlim(*x2)
ax1.set_ylim(0, 1.1) 

# --- Plot full spectrum lightly in gray for reference ---
ax1.plot(xn, yn, color="lightgray", lw=1)
ax2.plot(xn, yn, color="lightgray", lw=1)

# --- Overlay colored regions ---
for (low, high, species) in new_col:
    mask = (xn >= low) & (xn <= high)
    ax1.plot(xn[mask], yn[mask], color=colors[species], lw=1.25)
    ax2.plot(xn[mask], yn[mask], color=colors[species], lw=1.25)
    # Annotate near the middle of the band
    mid = 0.5 * (low + high)

# Hide the spines between axes
ax1.spines.right.set_visible(False)
ax2.spines.left.set_visible(False)
ax2.tick_params(labelleft=False, left=False, right=False, labelbottom=False)
ax1.tick_params(labelbottom=False)
ax1.grid(ls='--', alpha=0.5)
ax2.grid(ls='--', alpha=0.5)

# Diagonal break marks
d = .85  # proportion of vertical to horizontal extent of the slanted line
kwargs = dict(marker=[(-1, -d), (1, d)], markersize=8,
          linestyle="none", color='k', mec='k', mew=1, clip_on=False)
ax1.plot([1, 1], [0, 1], transform=ax1.transAxes, **kwargs)
ax2.plot([0, 0], [0, 1], transform=ax2.transAxes, **kwargs)

ax1 = ax[1, 0]
ax2 = ax[1, 1]

ax1.set_xlim(tuple(x - y for x, y in zip(x1, (0, 0))))
ax2.set_xlim(tuple(x + y for x, y in zip(x2, (0, 0))))
#ax2.set_xlim(tuple(x + y for x, y in zip(x2, (130, 130))))
ax1.set_ylim(0, 1.1) 

mask_nm = (nm[:,0] >= range[0]) & (nm[:,0] <= range[1])
ymax_nm = nm[mask_nm,1].max()

for freq, inten in nm:
        ax1.vlines(x=freq, ymin=0, ymax=inten/ymax_nm, color="black", lw=1.25)
        ax2.vlines(x=freq, ymin=0, ymax=inten/ymax_nm, color="black", lw=1.25)

base_classical = (classical[:,0] >= baserange[0]) & (classical[:,0] <= baserange[1])
ymin_classical = classical[base_classical,1].mean()

mask_classical = (classical[:,0] >= range[0]) & (classical[:,0] <= range[1])
ymax_classical = (classical-ymin_classical)[mask_classical,1].max()

xc = classical[:,0] 
yc = (classical[:,1] - ymin_classical) / ymax_classical

# --- Plot full spectrum lightly in gray for reference ---
c1 = ax1.fill_between(xc, yc, color="dodgerblue", alpha=0.6)
ax2.fill_between(xc, yc, color="dodgerblue", alpha=0.6)

# Hide the spines between axes
ax1.spines.right.set_visible(False)
ax2.spines.left.set_visible(False)
ax2.tick_params(labelleft=False, left=False, right=False)
ax1.set_xticks(np.arange(x1[0], x1[1], 200))
ax1.grid(ls='--', alpha=0.5)
ax2.grid(ls='--', alpha=0.5)

# Diagonal break marks
d = .85  # proportion of vertical to horizontal extent of the slanted line
kwargs = dict(marker=[(-1, -d), (1, d)], markersize=8,
          linestyle="none", color='k', mec='k', mew=1, clip_on=False)
ax1.plot([1, 1], [0, 1], transform=ax1.transAxes, **kwargs)
ax2.plot([0, 0], [0, 1], transform=ax2.transAxes, **kwargs)

plt.subplots_adjust(bottom=0.17)
fig.supxlabel(r"$\omega$ (cm$^{-1}$)", fontsize=12, y=0.05)
fig.supylabel(r"$I(\omega)$", fontsize=12, x=0.05)

# -----------------------------
# Shared legend outside
# -----------------------------

legend_elements = [Line2D([0], [0], color=c, lw=2, label=label) for label, c in colors2.items()]
le2 = [Patch(facecolor='darkgrey', edgecolor='darkgrey', alpha=0.5, label='Experimental Spectra'), Patch(facecolor='dodgerblue', edgecolor='dodgerblue', alpha=0.6, label='Classical MB-nrg'), Line2D([0], [0], color='black', lw=2, label='MB-nrg Normal Modes')]
#fig.legend(handles=legend_elements, loc="upper center", bbox_to_anchor=(0.5, 0.98), fontsize=10, frameon=False, ncol=5)

leg1 = fig.legend(
    handles=legend_elements,
    ncol=5,
    loc='upper center',
    bbox_to_anchor=(0.5, 1),
    frameon=False,
    fontsize=10
)

leg2 = fig.legend(
    handles=le2,
    ncol=3,
    loc='upper center',
    bbox_to_anchor=(0.5, 0.95),
    frameon=False,
    fontsize=10
)

#fig.add_artist(leg1)


#plt.tight_layout(rect=[0, 0, 1, 1])
##plt.savefig("Figure4.png", bbox_inches="tight")
##plt.savefig("Figure4.pdf", bbox_inches="tight")
#plt.savefig("Figure4_nm.pdf", bbox_inches="tight")
##plt.show()




plt.tight_layout(rect=[0, 0, 1, 1])

# --------------------------------------------------
# Continuous horizontal grid lines across broken axes
# --------------------------------------------------
from matplotlib.lines import Line2D

## turn off normal grids first
#for row in [0, 1]:
#    ax[row, 0].grid(True)
#    ax[row, 1].grid(True)

for row in [0, 1]:

    left_ax = ax[row, 0]
    right_ax = ax[row, 1]

    for y in left_ax.get_yticks():

        if y < left_ax.get_ylim()[0] or y > left_ax.get_ylim()[1]:
            continue

        # convert data y-coordinate to figure coordinates
        y_fig = fig.transFigure.inverted().transform(
            left_ax.transData.transform((0, y))
        )[1]

        fig.add_artist(
            Line2D(
                [left_ax.get_position().x1,
                 right_ax.get_position().x0],
                [y_fig, y_fig],
                transform=fig.transFigure,
                color='gray',
                linestyle='--',
                linewidth=0.8,
                alpha=0.5,
                zorder=0
            )
        )

#plt.savefig("Figure4.png", bbox_inches="tight")
#plt.savefig("Figure4.pdf", bbox_inches="tight")
plt.savefig("Figure4_nm.pdf", bbox_inches="tight")
