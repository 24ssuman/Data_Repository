import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.image as mpimg

# -----------------------------
# Load theory and experiment
# -----------------------------

old1 = np.loadtxt(f"weight/3-water/all.dat")
new1 = [np.loadtxt(f"weight/3-water/new_ir_A1.dat"), np.loadtxt(f"weight/3-water/new_ir_B4.dat"), np.loadtxt(f"weight/3-water/new_ir_C2.dat")]
#exp1 = np.loadtxt(f"weight/3-water/experimental.dat")
exp1 = np.loadtxt(f"/home/zsolomon/new-fit-1b-2b/5-paper-figures/main/figure-9-all-ir-spectra/3.dat")
path1 = ['pics/3-water/A1.png', 'pics/3-water/B4.png', 'pics/3-water/C2.png']
pop1 = np.loadtxt(f'weight/3-water/pops.dat')

old2 = np.loadtxt(f"weight/4-water/all.dat")
new2 = [np.loadtxt(f"weight/4-water/new_ir_A2.dat"), np.loadtxt(f"weight/4-water/new_ir_B1.dat")]
#exp2 = np.loadtxt(f"weight/4-water/experimental.dat")
exp2 = np.loadtxt(f"/home/zsolomon/new-fit-1b-2b/5-paper-figures/main/figure-9-all-ir-spectra/4.dat")
path2 = ['pics/4-water/A2.png', 'pics/4-water/B1.png']
pop2 = np.loadtxt(f'weight/4-water/pops.dat')

wat_oh = (3600, 3800)

old = [old1, old2]
new = [new1, new2]
exp = [exp1, exp2]
path = [path1, path2]
pop = [pop1, pop2]

lab = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

#fig, axes = plt.subplots(max(len(new1), len(new2)) + 1, 2, sharex=True, figsize=(16, 2 * (max(len(new1), len(new2)) + 1)), dpi=300, gridspec_kw={'hspace': 0.1})
num = max(len(new1), len(new2)) + 1
fig = plt.figure(figsize=(14, 2 * num), dpi=300)
axes1 = []
axes2 = []
ax = [axes1, axes2]
for i in range(num):
	if i <= len(new1):
		axes1.append(plt.subplot2grid((num, 2), (i, 0)))
	if i <= len(new2):
		axes2.append(plt.subplot2grid((num, 2), (i, 1)))

fig.subplots_adjust(hspace=0.1)

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
    "free_PGL_OH": "darkgreen",
    "hb_PGL_OH": "limegreen",
    "free_NH": "darkred",
    "int_Hbond_NH": "red",
    "water_Hbond_NH": "lightcoral",
    "CH": "orange"
}

# -----------------------------
# Frequency windows per system
# -----------------------------

old_col1 = [  # H2O_0
        (3600, 3800, "free_water_OH"),
        (3400, 3600, "free_PGL_OH"),
        (3200, 3400, "free_NH"),
        (3010, 3100, "hb_PGL_OH"),
        (3100, 3200, "CH"),
        (2400, 3010, "water_Hbond_NH"),
        ]

new_col1 = [
        [  # H2O_0
        (3600, 3800, "free_water_OH"),
        (3200, 3600, "free_PGL_OH"),
        (3050, 3200, "CH"),
        (2400, 3050, "water_Hbond_NH"),
        ],

        [  # H2O_0
        (3400, 3800, "free_water_OH"),
        (3200, 3500, "CH"),
        (3075, 3200, "int_Hbond_NH"),
        (3050, 3075, "hb_PGL_OH"),
        (3010, 3050, "water_Hbond_NH"),
        (2950, 3010, "hb_PGL_OH"),
        (2400, 2950, "water_Hbond_NH"),
        ],
        
        [  # H2O_0
        (3600, 3800, "free_water_OH"),
        (3200, 3600, "free_NH"),
        (3000, 3100, "hb_PGL_OH"),
        (3100, 3200, "CH"),
        (2400, 3000, "water_Hbond_NH"),
        ],
        ]

old_col2 = [  # H2O_0
        (3600, 3800, "free_water_OH"),
        (3100, 3600, "CH"),
        (3015, 3100, "hb_PGL_OH"),
        (2400, 3015, "water_Hbond_NH"),
        ]

new_col2 = [
        [  # H2O_0
        (3600, 3800, "free_water_OH"),
        (3100, 3600, "CH"),
        (3015, 3100, "hb_PGL_OH"),
        (2400, 3015, "water_Hbond_NH"),
        ],

        [  # H2O_0
        (3610, 3800, "free_water_OH"),
        (3200, 3610, "free_PGL_OH"),
        (2400, 3200, "water_Hbond_NH"),
        ],
        ]

old_col = [old_col1, old_col2]
new_col = [new_col1, new_col2]


# -----------------------------
# Plotting loop
# -----------------------------
# --- Experimental ---
		
for j in range(2):

    mask_exp = (exp[j][:,0] >= wat_oh[0]) & (exp[j][:,0] <= wat_oh[1])
    ymax_exp = exp[j][mask_exp,1].max()
    ax[j][0].fill_between(exp[j][:,0], exp[j][:,1] / ymax_exp, color="darkgray", alpha=0.6)
    ax[j][0].legend(handles=[Line2D([], [], linestyle='', color='none')],
              labels=[fr'GlyH$^{{+}}$(H$_2$O)$_{{{ 2 + j + 1}}}$'],
              frameon=False, fontsize=14, loc='upper left', handlelength=0)
    
    # --- Theoretical baseline normalization ---
    base_theory = (old[j][:,0] >= baserange[0]) & (old[j][:,0] <= baserange[1])
    ymin_theory = old[j][base_theory,1].min()
    
    mask_theory = (old[j][:,0] >= wat_oh[0]) & (old[j][:,0] <= wat_oh[1])
    ymax_theory = (old[j]-ymin_theory)[mask_theory,1].max()
    
    x = old[j][:,0]
    y = (old[j][:,1] - ymin_theory) / ymax_theory
    
    ax[j][0].set_xlim(*xrange)
    ax[j][0].set_ylim(0, 2) 
    
    # --- Plot full spectrum lightly in gray for reference ---
    ax[j][0].plot(x, y, color="lightgray", lw=1)
    
    # --- Overlay colored regions ---
    for (low, high, species) in old_col[j]:
        mask = (x >= low) & (x <= high)
        ax[j][0].plot(x[mask], y[mask], color=colors[species], lw=1.25)

    ax[j][0].grid(True, linestyle="--", c='lightgray', alpha=0.7)
    ax[j][0].set_xticklabels([])
    ax[j][0].set_yticks([0, 1, 2])
    ax[j][0].tick_params(axis="y", labelsize=12)


# --- same for new ir ---

for k in range(num - 1):
    for l in range(2):
        if (k < len(new[l])):
            base_theory = (new[l][k][:,0] >= baserange[0]) & (new[l][k][:,0] <= baserange[1])
            ymin_theory = new[l][k][base_theory,1].min()
            
            mask_theory = (new[l][k][:,0] >= wat_oh[0]) & (new[l][k][:,0] <= wat_oh[1])
            ymax_theory = (new[l][k]-ymin_theory)[mask_theory,1].max()
            
            ax[l][k + 1].set_ylim(0, 2)
            ax[l][k + 1].set_xlim(*xrange)
            
            xn = new[l][k][:,0]
            yn = (new[l][k][:,1] - ymin_theory) / ymax_theory
            
            # --- Plot full spectrum lightly in gray for reference ---
            ax[l][k + 1].plot(xn, yn, color="lightgray", lw=1)
            
            ax[l][k + 1].legend(handles=[Line2D([], [], linestyle='', color='none')],
                      labels=[str(2 + l + 1) + lab[k] + ': ' + str((pop[l][k] * 100).round(1)) + '%'],
                      frameon=False, fontsize=14, loc='upper left', handlelength=0)

            # --- Overlay colored regions ---
            for (low, high, species) in new_col[l][k]:
                mask = (xn >= low) & (xn <= high)
                ax[l][k + 1].plot(xn[mask], yn[mask], color=colors[species], lw=1.25)
            
            ax[l][k].set_xticklabels([])
            ax[l][k + 1].set_yticks([0, 1, 2])
            ax[l][k + 1].tick_params(axis="y", labelsize=12)
            ax[l][k + 1].grid(True, linestyle="--", c='lightgray', alpha=0.7)

            img1 = mpimg.imread(path[l][k])
            ny, nx = img1.shape[:2]   # rows (height), columns (width)
            aspect_img = nx / ny    # width / height
            x0 = 2650
            y0 = 0.5
            scale = 500 / (nx * ny)
            dy = ny * scale 
            dx = nx * scale * (1200/7)
            extent = [x0, x0 + dx, y0, y0 + dy]
            ax[l][k + 1].imshow(img1, aspect='auto', extent=extent, alpha=1.0)

ax[0][len(new1)].tick_params(axis="both", labelsize=12)
ax[1][len(new2)].tick_params(axis="both", labelsize=12)

#plt.subplots_adjust(bottom=0.17)
#fig.supxlabel(r"$\omega$ (cm$^{-1}$)", fontsize=16)
fig.supylabel(r"$I(\omega)$", fontsize=16)

fig.text(0.76, -0.018, r"$\omega$ (cm$^{-1}$)", ha='center', fontsize=16)
fig.text(0.28, -0.018, r"$\omega$ (cm$^{-1}$)", ha='center', fontsize=16)

# -----------------------------
# Shared legend outside
# -----------------------------
legend_elements = [Line2D([0], [0], color=c, lw=2, label=label) for label, c in colors2.items()]
#fig.legend(handles=legend_elements, loc="upper center", bbox_to_anchor=(0.5, 1.07), fontsize=12, frameon=False, ncol=4)
fig.legend(handles=legend_elements, loc="lower right", bbox_to_anchor=(0.925, 0.05), fontsize=12, frameon=True, ncol=2)

plt.tight_layout(rect=[0, 0, 1, 0.99])
#plt.savefig("Figure7.png", bbox_inches="tight")
plt.savefig("Figure7.pdf", bbox_inches="tight")
#plt.show()
