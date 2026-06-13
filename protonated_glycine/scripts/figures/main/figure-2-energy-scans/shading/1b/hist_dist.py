import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import math
import numpy as np

natom = 11
nframes = 25897
want_idx = [1, 2, 3, 4, 5, 8, 9, 10, 11]

def dist(v1, v2):
    return math.sqrt(((float(v1[0]) - float(v2[0])) ** 2) + ((float(v1[1]) - float(v2[1])) ** 2) + ((float(v1[2]) - float(v2[2])) ** 2))

def read_xyz(fname, nframes):
    f = open(fname, 'r+')
    a = []; b = []; c = []; d = []
    for i in range(nframes):
        f.readline()
        f.readline()
        coord = []
        for j in range(natom):
            if (j + 1) in want_idx:
                coord.append(f.readline().split())
            else:
                f.readline()
        # A = CO
        a.append(dist(coord[5][1:], coord[6][1:]))
        # B = NH
        for k in range(3):
            b.append(dist(coord[0][1:], coord[k + 1][1:]))
        # C = OH
        c.append(dist(coord[7][1:], coord[8][1:]))
        # D = IHB
        d.append(min(dist(coord[6][1:], coord[1][1:]), dist(coord[6][1:], coord[2][1:]), dist(coord[6][1:], coord[3][1:])))
    return a, b, c, d

stretches = read_xyz('training_set.xyz', nframes)

# Create a figure with two subplots for histograms
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

lab = ['CO', 'NH', 'OH', 'IHB']
c = ['deepskyblue', 'yellowgreen', 'palevioletred', 'slateblue']
xlim = [(0.6, 2), (0.6, 2), (0.6, 2), (1.4, 2.6)]

for i, ax in enumerate(axes.flatten()):	
    
    dat = stretches[i]
   
    print(min(dat), max(dat))
    
    bins = np.linspace(min(dat), max(dat), 50)  # 50 bins between min and max values 
    ax.hist(dat, bins=bins, color=c[i], alpha=0.7, edgecolor='black')
    ax.set_xlabel(lab[i] + ' Distance (Å)')
    ax.set_ylabel('Frequency')
    ax.set_title('Distribution of ' + lab[i] + ' Distances')
#    ax.set_xlim(xlim[i])


plt.tight_layout()
plt.savefig('all_dist_histogram.png')
plt.show()
