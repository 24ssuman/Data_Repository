import numpy as np
import matplotlib.pyplot as plt
import sys
import glob
import os
import re

hname = [
    'PGL-NH-----O=C-PGL'
]
input_files = sorted(glob.glob("isomer*.dat"))
lab = ['A', 'B', 'C']
col = ['deepskyblue', 'palevioletred', 'yellowgreen']

plt.figure(figsize=(8, 3))

for i in range(len(input_files)):
	data = np.loadtxt(input_files[i])
	r, g_r = data[:,0], data[:,1]
	plt.plot(r, g_r, label=f"2" + lab[i], c=col[i])

plt.xlim(1.5, 4)
#		plt.set_title(f"{hname[k]} RDF")
plt.xlabel(r"$r_{O9 - H3}$ ($\AA{}$)")

plt.ylabel(r"$g(r)$")
plt.legend(loc='upper right')


plt.tight_layout()
plt.savefig('FigureS10.pdf', dpi=300)
#plt.savefig('rdf.png', dpi=300)



