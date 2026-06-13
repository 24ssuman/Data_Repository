import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

# Example Data (can be different for each table if you want)

dat = np.loadtxt('tab.dat')
#data1 = np.append([[r'r$_{N4-O9}$ (Å)'], [r'r$_{C8-O9}$ (Å)'], [r'$\Psi$'], ['lab4']], dat[0:4,:], axis=1)
data1 = np.append([[r'r$_{N4-O9}$ (Å)'], [r'r$_{C8-O9}$ (Å)'], [r'$\Psi$']], np.round(dat[0:3,:], 5), axis=1)
data2 = np.append([[r'r$_{N4-O9}$ (Å)'], [r'r$_{C8-O9}$ (Å)'], [r'$\Psi$']], np.round(dat[4:7,:], 5), axis=1)
data3 = np.append([[r'r$_{N4-O9}$ (Å)'], [r'r$_{C8-O9}$ (Å)'], [r'$\Psi$']], np.round(dat[8:11,:], 5), axis=1)
#data2 = dat[4:8,:]
#data3 = dat[8:,:]

lab = ['Cis-syn', 'Trans-anti', 'Trans-syn']
col_labels = ['Parameter', 'RI-MP2/\naug-cc-pVTZ', 'MB-nrg']

fig, axes = plt.subplots(1, 3, figsize=(12, 6))

tables = [data1, data2, data3]
images = ["cis_syn.png", "trans_anti.png", "trans_syn.png"]
idx = 0

for ax, data in zip(axes, [data1, data2, data3]):
    ax.axis('tight')
    ax.axis('off')
    table = ax.table(
        cellText=data,
        colLabels=col_labels,
        loc='center'
    )
    table.scale(1, 1.5)
    ax.set_title(lab[idx], y=-0.01, pad=10, verticalalignment='top')

    xaxes = ax.get_xlim()
    yaxes = ax.get_ylim()
    img1 = mpimg.imread('/home/zsolomon/Pictures/' + images[idx])
    if (idx == 1):
        ax.imshow(img1, aspect='auto', extent=[0.025, -0.025, -0.045, -0.015], alpha=1.0)
    else:
        ax.imshow(img1, aspect='auto', extent=[-0.025, 0.025, -0.045, -0.015], alpha=1.0)
    #if (idx == 1):
    #    ax.invert_xaxis()

    ax.set_xlim(xaxes)
    ax.set_ylim(yaxes)
    idx += 1

plt.tight_layout()
plt.savefig('FigureS5.pdf', dpi=300)
plt.show()

