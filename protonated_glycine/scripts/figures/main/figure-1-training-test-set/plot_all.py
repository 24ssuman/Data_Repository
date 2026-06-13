import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.image as mpimg
import numpy as np

cs1 = np.loadtxt('1b-config-space.dat')
cs2 = np.loadtxt('2b-config-space.dat')
c1_all = np.loadtxt('1b-test-correlation.dat')
c2_all = np.loadtxt('2b-test-correlation.dat')

# cs: dist, dih, ref be
# c: ref, pred, ref be

fig, axes = plt.subplots(1, 4, sharex=False, figsize=(16, 6.5), dpi=300)

mask1 = (c1_all[:, 2] <= 50)
mask2 = (c2_all[:, 2] <= 50)

c1 = c1_all[mask1,:]
c2 = c2_all[mask2,:]

emin = np.min([
    cs1[:, 2].min(),
    cs2[:, 2].min(),
    c1[:, 2].min(),
    c2[:, 2].min()
])

emax = np.max([
    cs1[:, 2].max(),
    cs2[:, 2].max(),
    c1[:, 2].max(),
    c2[:, 2].max()
])

# ---- PLOT 1: 1B CONFIG SPACE ---- #

ax = axes[0]

sc1 = ax.scatter(cs1[:,0], cs1[:,1], c = cs1[:,2], vmin=emin, vmax=emax, cmap='viridis')
#ax.set_title('1B Training Set Configuration Space')
ax.set_xlabel(r'r$_{O9 - H3}$ (Å)', fontsize='14')
ax.set_ylabel(r'$\psi$', fontsize='14')
ax.text(-0.12, 1.02, '(a)', transform=ax.transAxes, verticalalignment='top', horizontalalignment='left')

# ---- PLOT 2: 2B CONFIG SPACE ---- #

ax = axes[1]

sc3 = ax.scatter(cs2[:,0], cs2[:,1], c = cs2[:,2], vmin=emin, vmax=emax, cmap='viridis')
#ax.set_title('2B Training Set Configuration Space')
ax.text(-0.12, 1.02, '(b)', transform=ax.transAxes, verticalalignment='top', horizontalalignment='left')
ax.set_xlabel(r'r$_{C5 - O_W}$ (Å)', fontsize='14')
#ax.set_ylabel('N4-C5-C8-O9 Dihedral Angle (Degrees)')

# ---- PLOT 1: 1B TEST SET CORRELATION ---- #

ax = axes[2]

sc2 = ax.scatter(c1[:,0], c1[:,1], c = c1[:,2], vmin=emin, vmax=emax, cmap='viridis')
#ax.set_title('1B Test Set Correlation Plot')
ax.set_xlabel('Reference Energy (kcal/mol)')
ax.set_ylabel('Predicted Energy (kcal/mol)')
ax.text(-0.12, 1.02, '(c)', transform=ax.transAxes, verticalalignment='top', horizontalalignment='left')
ax.text(0.05, 0.95, 'RMSD (BE < 50) = 0.5024', transform=ax.transAxes, verticalalignment='top', horizontalalignment='left')
ax.axline((0, 0), slope=1, color='grey', linestyle='--', label='x=y')

# ---- PLOT 4: 2B TEST SET CORRELATION ---- #

ax = axes[3]

sc4 = ax.scatter(c2[:,0], c2[:,1], c = c2[:,2], vmin=emin, vmax=emax, cmap='viridis')
#ax.set_title('2B Test Set Correlation Plot')
ax.set_xlabel('Reference Energy (kcal/mol)')
#ax.set_ylabel('Predicted Energy (kcal/mol)')
ax.text(-0.12, 1.02, '(d)', transform=ax.transAxes, verticalalignment='top', horizontalalignment='left')
ax.text(0.05, 0.95, 'RMSD (BE < 50) = 0.2050', transform=ax.transAxes, verticalalignment='top', horizontalalignment='left')
ax.axline((0, 0), slope=1, color='grey', linestyle='--', label='x=y')

# ---- PICTURES UNDERNEATH ---- #

# -- 1B -- #
image_path = '/home/zsolomon/Pictures/labeled_trans_pgl_dih.png'
img1 = mpimg.imread(image_path)
newax = fig.add_axes([0.1, 0.05, 0.35, 0.35], anchor='NE')
newax.imshow(img1)
newax.axis('off')

# -- 2B -- #
image_path = '/home/zsolomon/Pictures/labeled_trans_pgl_2b.png'
img1 = mpimg.imread(image_path)
newax = fig.add_axes([0.4, 0.05, 0.33, 0.33], anchor='NE')
newax.imshow(img1)
newax.axis('off')

# ---- FULL PLOT SETTINGS ---- #

cbar_ax = fig.add_axes([0.95, 0.5, 0.01, 0.4])  # [left, bottom, width, height]
fig.colorbar(sc1, cax=cbar_ax, label="Binding Energy (kcal/mol)")

#fig.suptitle("all", fontsize=16, y=0.98)

plt.tight_layout(rect=[0, 0.4, 0.93, 0.97])
plt.savefig("Figure1.pdf", dpi=300)
#plt.savefig("Figure1.png", dpi=300)
#plt.show()


#for j in range(4):
#	print(axes[j].get_xlim())


