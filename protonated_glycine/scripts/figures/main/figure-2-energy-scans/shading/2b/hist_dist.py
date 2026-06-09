import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import math
import numpy as np

natom = 14
nframes = 21138
want_idx = [2, 3, 4, 11, 12]

def dist(v1, v2):
    return math.sqrt(((float(v1[0]) - float(v2[0])) ** 2) + ((float(v1[1]) - float(v2[1])) ** 2) + ((float(v1[2]) - float(v2[2])) ** 2))

def read_xyz(fname, nframes):
    f = open(fname, 'r+')
    a = []; b = []; 
    for i in range(nframes):
        f.readline()
        f.readline()
        coord = []
        for j in range(natom):
            if (j + 1) in want_idx:
                coord.append(f.readline().split())
            else:
                f.readline()
        d = []
        for k in range(len(want_idx) - 1):
            d.append(dist(coord[k][1:], coord[-1][1:]))
        mind = min(d)
        idx = d.index(mind)
        if (idx == 3):
            b.append(mind)
        else:
            a.append(mind)
    return a, b

stretches = read_xyz('training_set.xyz', nframes)

# Create a figure with two subplots for histograms
fig, axes = plt.subplots(1, 2, figsize=(14, 10))

lab = ['NH', 'OH']
c = ['deepskyblue', 'palevioletred']
#xlim = [(0.6, 2), (0.6, 2), (0.6, 2), (1.4, 2.6)]

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
