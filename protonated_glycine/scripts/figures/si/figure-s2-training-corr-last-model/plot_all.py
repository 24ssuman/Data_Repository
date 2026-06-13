import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.image as mpimg
import numpy as np

cs1 = np.loadtxt('1b-config-space.dat')
c1_all = np.loadtxt('1b-test-correlation.dat')

xlims = np.loadtxt('min_max', delimiter=',', converters={0: lambda s: float(s.strip(b"(")), 1: lambda s: float(s.strip(b")"))})

# cs: dist, dih, ref be
# c: ref, pred, ref be

fig, axes = plt.subplots(1, 2, sharex=False, figsize=(8, 4), dpi=300)
#fig, axes = plt.subplots(1, 4, sharex=False, figsize=(16, 6.5), dpi=300)

mask1 = (c1_all[:, 2] <= 50)

c1 = c1_all[mask1,:]

emin = np.min([
    cs1[:, 2].min(),
    c1[:, 2].min(),
])

emax = np.max([
    cs1[:, 2].max(),
    c1[:, 2].max(),
])

# ---- PLOT 1: 1B CONFIG SPACE ---- #

ax = axes[0]

sc1 = ax.scatter(cs1[:,0], cs1[:,1], c = cs1[:,2], vmin=emin, vmax=emax, cmap='viridis')
#ax.set_title('1B Training Set Configuration Space')
ax.set_xlabel(r'r$_{O9 - H3}$ (Å)', fontsize='14')
ax.set_ylabel(r'$\psi$', fontsize='14')
ax.text(-0.12, 1.02, '(a)', transform=ax.transAxes, verticalalignment='top', horizontalalignment='left')
ax.set_xlim(xlims[0])

# ---- PLOT 1: 1B TEST SET CORRELATION ---- #

ax = axes[1]

sc2 = ax.scatter(c1[:,0], c1[:,1], c = c1[:,2], vmin=emin, vmax=emax, cmap='viridis')
#ax.set_title('1B Test Set Correlation Plot')
ax.set_xlabel('Reference Energy (kcal/mol)')
ax.set_ylabel('Predicted Energy (kcal/mol)')
ax.text(-0.12, 1.02, '(b)', transform=ax.transAxes, verticalalignment='top', horizontalalignment='left')
ax.text(0.05, 0.95, 'RMSD (BE < 50) = 0.4797', transform=ax.transAxes, verticalalignment='top', horizontalalignment='left')
ax.axline((0, 0), slope=1, color='grey', linestyle='--', label='x=y')
ax.set_xlim(xlims[1])

#cbar_ax = fig.add_axes([0.95, 0.5, 0.01, 0.4])  # [left, bottom, width, height]
cbar_ax = fig.add_axes([0.91, 0.1, 0.02, 0.8])  # [left, bottom, width, height]
fig.colorbar(sc1, cax=cbar_ax, label="Binding Energy (kcal/mol)")

#fig.suptitle("all", fontsize=16, y=0.98)

plt.tight_layout(rect=[0, 0, 0.9, 0.97])
#plt.tight_layout(rect=[0, 0.4, 0.93, 0.97])
plt.savefig("FigureS2.pdf", dpi=300)
#plt.show()



