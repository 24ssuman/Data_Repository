import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator


tokcal = 23.06035
idx = [2, 3, 3, 2, 3, 4]
#idx = [2, 4, 3, 2, 3, 4]
lab = []
col = []
letters = ['A', 'B', 'C', 'D']
c = ['deepskyblue', 'palevioletred', 'yellowgreen', 'slateblue']

mbx = np.loadtxt('mbx.dat')
tepigs = np.loadtxt('te-pigs.dat')

ix = 0
num = 0
iso = 0
curr = [mbx[num] - 0.005, tepigs[num] + 0.005/tokcal]
for i in range(len(mbx)):
	mbx[i] -= curr[0]
	tepigs[i] -= curr[1]
	lab.append(str(iso + 1) + letters[ix])
	col.append(c[ix])
	ix += 1
	print(lab[i] + ': subtracting index ' + str(num) + ' from index ' + str(i) + ': ' + str(mbx[i] + curr[0]) + ' - ' + str(curr[0]) + ' = ' + str(mbx[i]))
	if ix >= idx[iso]:
		num += idx[iso]
		ix = 0
		iso += 1
		try:
			curr = [mbx[num] + 0.005, tepigs[num] + 0.005/tokcal]
		except:
			break


positions = []
group_centers = []

bar_width = 0.25
group_gap = 0.5 
x = 0
start = 0

for niso in idx:
    group_pos = []
    for _ in range(niso):
        positions.append(x)
        group_pos.append(x)
        x += bar_width

    group_centers.append(np.mean(group_pos))
    x += group_gap


fig, ax = plt.subplots(1, 1, figsize=(12,4))

#ax = plt.gca()
#ax.xaxis.set_major_locator(MultipleLocator(0.5))  # grid every 0.5 kcal/mol
plt.grid(axis='y', alpha=0.5, ls='--')
ax.set_axisbelow(True)

#br1 = np.arange(len(mbx))
#br2 = [x+0.25 for x in br1]

plt.bar(positions, mbx, color = col, width = bar_width, label = 'MB-nrg')
#ax.set_xticks(group_centers)
#ax.set_xticklabels([1,2,3,4,5,6])  # number of waters
#ax.set_xlabel("Number of Waters")

plt.xlabel('Isomer',  fontsize = 15)
plt.ylabel(r'Relative Energy (kcal/mol)',  fontsize =15)
plt.xticks(positions, lab, fontsize=12)
plt.tick_params(axis='y', labelsize=12)

#ax.text(-0.05, 1.02, '(a)', transform=ax.transAxes, verticalalignment='top', horizontalalignment='left', fontsize=15)

#plt.legend(loc='upper right',fontsize=15)

plt.tight_layout()
plt.savefig("FigureS8.pdf")
#plt.show()
