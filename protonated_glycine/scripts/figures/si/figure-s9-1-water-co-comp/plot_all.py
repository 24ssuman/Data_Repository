import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.image as mpimg

# -----------------------------
# Load theory and experiment
# -----------------------------
theory = [np.loadtxt("1A.dat"), np.loadtxt("1B.dat")]
path = ['pics/1A.png', 'pics/1B.png']
lab = ["A", "B"]
exp = np.loadtxt("experimental.dat")

fig, ax = plt.subplots(len(theory), 1, sharex=True, figsize=(8, 4), dpi=300)

wat_oh = (3600, 3800)
ranges = [(3400, 3800), (3600, 3800), (3600, 3800), (3600, 3800), (3600, 3800), (3600, 3800), (3600, 3800)]
xrange = (1400, 1900)
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
    "C-H": "orange",
    "Others": "black"
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
    "else":"black"
}

# -----------------------------
# Frequency windows per system
# -----------------------------
freq_windows = {
    "A": [
        (3600, 3800, "free_water_OH"),
        (3500, 3600, "free_PGL_OH"),
        (3200, 3500, "free_NH"),
        (3000, 3200, "CH"),
        (2400, 3000, "water_Hbond_NH"),
        (1400, 2400, "else"),
    ],

    "B": [
        (3500, 3800, "free_water_OH"),
        (3300, 3500, "free_NH"),
        (3100, 3300, "CH"),
        (2400, 2900, "int_Hbond_NH"),
        (2900, 3100, "hb_PGL_OH"),
        (1400, 2400, "else"),
    ],
}

# -----------------------------

# -----------------------------
# Plotting loop
# -----------------------------
for i in range(len(theory)):
    # --- Experimental ---
    mask_exp = (exp[:,0] >= wat_oh[0]) & (exp[:,0] <= wat_oh[1])
    ymax_exp = exp[mask_exp,1].max()
#    ax[i].fill_between(exp[:,0], exp[:,1] / ymax_exp, color="darkgray", alpha=0.5)
    ax[i].legend(handles=[Line2D([], [], linestyle='', color='none')],
                 labels=['1' + lab[i]],
                 frameon=False, fontsize=14, loc='upper left', handlelength=0)

    # --- Theoretical baseline normalization ---
    base_theory = (theory[i][:,0] >= baserange[0]) & (theory[i][:,0] <= baserange[1])
    ymin_theory = theory[i][base_theory,1].min()

    mask_theory = (theory[i][:,0] >= ranges[i][0]) & (theory[i][:,0] <= ranges[i][1])
    ymax_theory = (theory[i]-ymin_theory)[mask_theory,1].max()

    x = theory[i][:,0]
    y = (theory[i][:,1] - ymin_theory) / ymax_theory

    # --- Plot full spectrum lightly in gray for reference ---
    ax[i].plot(x, y, color="lightgray", lw=1)

    ax[i].set_xlim(*xrange)
    ax[i].set_ylim(0, 1.3)

    # --- Overlay colored regions ---
    if lab[i] in freq_windows:
        for (low, high, species) in freq_windows[lab[i]]:
            mask = (x >= low) & (x <= high)
            ax[i].plot(x[mask], y[mask], color=colors[species], lw=1.5)
            # Annotate near the middle of the band
            mid = 0.5 * (low + high)

    ax[i].tick_params(axis="both", labelsize=12)
    ax[i].grid(True, linestyle="--", c='lightgray', alpha=0.7)
    
    img1 = mpimg.imread(path[i])
    ny, nx = img1.shape[:2]   # rows (height), columns (width)
    aspect_img = nx / ny    # width / height
    print(aspect_img)
    
    x0 = 1650
    y0 = 0.4
    scale = 500 / (nx * ny)
    dy = ny * scale 
    dx = nx * scale * (500/5)
    extent = [x0, x0 + dx, y0, y0 + dy]
    print(extent)
    ax[i].imshow(img1, aspect='auto', extent=extent, alpha=1.0)

#    axL.text(

fig.supxlabel(r"$\omega$ (cm$^{-1}$)", fontsize=16)
fig.supylabel(r"$I(\omega)$", fontsize=16)

# -----------------------------
# Shared legend outside
# -----------------------------
#legend_elements = [Line2D([0], [0], color=c, lw=2, label=label) for label, c in colors2.items()]
#fig.legend(handles=legend_elements, loc="upper right", bbox_to_anchor=(0.95, 0.95), fontsize=6.5, frameon=True, ncol=3)

plt.tight_layout(rect=[0, 0, 1, 0.99])
plt.savefig("FigureS9.pdf", bbox_inches="tight")
#plt.show()
