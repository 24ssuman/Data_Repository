import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# -----------------------------
# Load theory and experiment
# -----------------------------
nplot = 7
theory = [np.loadtxt(f"spec_{i}.dat") for i in range(nplot)]
exp = [np.loadtxt(f"{i}.dat") for i in range(nplot)]

fig, ax = plt.subplots(len(theory), 1, sharex=True, figsize=(8, 12), dpi=300)

ranges = [(3400, 3800), (3600, 3800), (3600, 3800), (3600, 3800), (3600, 3800), (3600, 3800), (3600, 3800)]
xrange = (2600, 3800)
baserange = (2400, 2800)

# -----------------------------
# Colors for each chemical entity
# -----------------------------
colors2 = {
    "Free water O-H": "darkblue",
    "H-bonded water O-H": "deepskyblue",
    r"Free GlyH$^+$ O-H": "darkgreen",
    r"H-bonded GlyH$^+$ O-H": "limegreen",
    "Free N-H": "darkred",
    "Internal H-bonded N-H": "red",
    "Water H-bonded N-H": "lightcoral",
    "C-H": "orange"
}

colors = {
    "free_water_OH": "darkblue",
    "hb_water_OH": "deepskyblue",
#    "hb_water_OH": "lightblue",
    "free_PGL_OH": "darkgreen",
    "hb_PGL_OH": "limegreen",
    "free_NH": "darkred",
    "int_Hbond_NH": "red",
    "water_Hbond_NH": "lightcoral",
    "CH": "orange"
#    "CH": "purple"
}

# -----------------------------
# Frequency windows per system
# -----------------------------
freq_windows = {
    0: [  # H2O_0
        (3500, 3800, "free_PGL_OH"),
        (3300, 3500, "free_NH"),
        (3010, 3300, "CH"),
        (2400, 3010, "int_Hbond_NH"),
    ],
    1: [  # H2O_1
        (3600, 3800, "free_water_OH"),
        (3500, 3600, "free_PGL_OH"),
        (3200, 3500, "free_NH"),
        (3000, 3200, "CH"),
        (2400, 3000, "water_Hbond_NH"),
        (2900, 3000, "hb_PGL_OH"),
        (2800, 2900, "int_Hbond_NH"),
    ],
    2: [  # H2O_2
        (3600, 3800, "free_water_OH"),
        (3500, 3600, "free_PGL_OH"),
        (3200, 3500, "free_NH"),
        (3100, 3200, "CH"),
        (3050, 3100, "hb_PGL_OH"),
        (3000, 3050, "int_Hbond_NH"),
        (2960, 3000, "hb_PGL_OH"),
        (2400, 2960, "water_Hbond_NH")
    ],
    3: [  # H2O_3
        (3600, 3800, "free_water_OH"),
        (3400, 3600, "free_PGL_OH"),
        (3200, 3400, "free_NH"),
        (3010, 3100, "hb_PGL_OH"),
        (3100, 3200, "CH"),
        (2400, 3010, "water_Hbond_NH"),
    ],
    4: [  # H2O_4
        (3600, 3800, "free_water_OH"),
        (3100, 3600, "CH"),
        (3015, 3100, "hb_PGL_OH"),
        (2400, 3015, "water_Hbond_NH"),
    ],
    5: [  # H2O_5
        (3610, 3800, "free_water_OH"),
        (3200, 3610, "hb_water_OH"),
        (3100, 3200, "CH"),
        (3075, 3100, "hb_PGL_OH"),
        (2400, 3075, "water_Hbond_NH"),
        (2850, 2920, "hb_PGL_OH"),
    ],
    6: [  # H2O_6
        (3600, 3800, "free_water_OH"),
        (3200, 3600, "hb_water_OH"),
        (2400, 3200, "water_Hbond_NH"),
        (3030, 3120, "hb_PGL_OH"),
        (2960, 3000, "hb_PGL_OH"),
        (2700, 2800, "hb_PGL_OH"),
    ],
}

# -----------------------------
# Plotting loop
# -----------------------------
for i in range(len(theory)):
    # --- Experimental ---
    mask_exp = (exp[i][:,0] >= ranges[i][0]) & (exp[i][:,0] <= ranges[i][1])
    ymax_exp = exp[i][mask_exp,1].max()
    ax[i].fill_between(exp[i][:,0], exp[i][:,1] / ymax_exp, color="darkgray", alpha=0.5)
#    ax[i].fill_between(exp[i][:,0], exp[i][:,1] / exp_area[i], color="darkgray", alpha=0.6)
    ax[i].legend(handles=[Line2D([], [], linestyle='', color='none')],
                 labels=[fr'GlyH$^{{+}}$(H$_2$O)$_{{{i}}}$'],
                 frameon=False, fontsize=14, loc='upper left', handlelength=0)

    # --- Theoretical baseline normalization ---
    base_theory = (theory[i][:,0] >= baserange[0]) & (theory[i][:,0] <= baserange[1])
    ymin_theory = theory[i][base_theory,1].min()

    mask_theory = (theory[i][:,0] >= ranges[i][0]) & (theory[i][:,0] <= ranges[i][1])
    ymax_theory = (theory[i]-ymin_theory)[mask_theory,1].max()

    x = theory[i][:,0]
#    y = (theory[i][:,1] - ymin_theory) 
    y = (theory[i][:,1] - ymin_theory) / ymax_theory

    # --- Plot full spectrum lightly in gray for reference ---
    ax[i].plot(x, y, color="lightgray", lw=1)

    ax[i].set_xlim(*xrange)
    ax[i].set_ylim(0, 1.3)
#    ax[i].set_ylim(0, 1.25 * max(ymax_theory, ymax_exp / exp_area[i])) 

    # --- Overlay colored regions ---
    if i in freq_windows:
        for (low, high, species) in freq_windows[i]:
            mask = (x >= low) & (x <= high)
            #ax[i].plot(x[mask], y[mask], color=colors[species], lw=2, label=species)
            ax[i].plot(x[mask], y[mask], color=colors[species], lw=1.25)
            # Annotate near the middle of the band
            mid = 0.5 * (low + high)
            #ax[i].text(mid, 0.92, species.replace("_", " "), color=colors[species],
            #           fontsize=9, ha="center", va="top")

    ax[i].tick_params(axis="both", labelsize=12)
    ax[i].grid(True, linestyle="--", c='lightgray', alpha=0.7)

fig.supxlabel(r"$\omega$ (cm$^{-1}$)", fontsize=16)
fig.supylabel(r"$I(\omega)$", fontsize=16)

# -----------------------------
# Shared legend outside
# -----------------------------
legend_elements = [Line2D([0], [0], color=c, lw=2, label=label) for label, c in colors2.items()]
fig.legend(handles=legend_elements, loc="upper center", bbox_to_anchor=(0.5, 1.02), fontsize=8, frameon=False, ncol=4)

plt.tight_layout(rect=[0, 0, 1, 0.99])
#plt.savefig("Figure9.png", bbox_inches="tight")
plt.savefig("Figure9.pdf", bbox_inches="tight")

