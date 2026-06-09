import numpy as np
import matplotlib.pyplot as plt

#read data files and extract frequencies

def readfreq_qchem(fname):
	f=open(fname, 'r+')
	lines = f.readlines()
	data = []        
	for line in lines:
		data.append(float(line.split()[0])) 
	return data 

def readfreq_mb(fname):
	f=open(fname,'r+')
	lines = f.readlines()
	data = []
	for line in lines:
		data.append(float(line.split()[0]))
	return data

#define data file paths
qchem = "mp2.dat"
mb = "wb97mv.dat"

qchemdat = readfreq_qchem(qchem)
mbdat = readfreq_mb(mb)

index = list(range(1, 27))

#make plot
fig, axes = plt.subplots(2, 1, figsize=(12,8))

ax = axes[0]
ax.grid(True, axis='y', ls='--', alpha=0.5)
ax.set_axisbelow(True)

br1 = np.arange(len(qchemdat))
br2 = [x+0.25 for x in br1]

ax.bar(br1, qchemdat, color = 'darkgreen', width = 0.25, label = 'RI-MP2')
ax.bar(br2, mbdat, color = 'goldenrod', width = 0.25, label = r'$\omega$B97M-V')

#ax.set_xlabel('Normal Mode Indexes',  fontsize = 15)
ax.set_ylabel(r'$\omega$ (cm$^{-1}$)',  fontsize =15)
ax.set_xticks([r+0.25 for r in range(len(br1))], range(1,28), fontsize=12)
ax.tick_params(axis='y', labelsize=12)

#ax.text(-0.05, 1.02, '(a)', transform=ax.transAxes, verticalalignment='top', horizontalalignment='left', fontsize=15)

ax.legend(loc='upper left',fontsize=15)

ax = axes[1]
ax.grid(True, axis='y', ls='--', alpha=0.5)
ax.set_axisbelow(True)

mb_qchem = []
i = 0
while qchemdat[i] == 0:
	mb_qchem.append(0)
	i += 1

while i < len(qchemdat):
	ab = abs(mbdat[i] - qchemdat[i])
	err = abs(mbdat[i] - qchemdat[i])/qchemdat[i] * 100
	mb_qchem.append(ab)
	#mb_qchem.append(err)
	print(err, ab)
	i += 1

br1 = np.arange(len(mb_qchem))
ax.bar(br1, mb_qchem, color = 'green', width = 0.25, label = 'wB97M-V vs RI-MP2')

ax.set_xlabel('Normal Mode Indices',  fontsize = 15)
ax.set_ylabel(r'$\Delta \omega$ (cm$^{-1}$)',  fontsize =15)
ax.set_xticks([r for r in range(len(br1))], range(1,28), fontsize =12)
ax.set_ylim(0, np.max(mb_qchem[2:]) * 1.25)
ax.tick_params(axis='y', labelsize=12)

#ax.text(-0.05, 1.02, '(b)', transform=ax.transAxes, verticalalignment='top', horizontalalignment='left', fontsize=15)

#ax.legend(loc='upper right',fontsize=15)
plt.tight_layout()
plt.savefig("FigureS7.pdf")
#plt.show()
