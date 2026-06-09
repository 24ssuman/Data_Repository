import numpy as np
import glob
import os
import matplotlib.pyplot as plt
import math

lab = ['A', 'B', 'C', 'D']
types = [2, 6, 8, 9] 	# 1-indexed
h = [[2, 9], [8, 9], [2, 6]]
hname = ['PGL-NH-----O-Water', 'PGL-OH-----O-Water', 'PGL-NH-----O=C-PGL']
t = 10
nframes = int(125001 * t)
n_bins = 100

def dist(a, b):
	return math.sqrt((float(a[0]) - float(b[0])) ** 2 + (float(a[1]) - float(b[1])) ** 2 + (float(a[2]) - float(b[2])) ** 2)



def read_lammpstrj(fname):
	a = []
	b = []
	c = []
	ds = [a, b, c]
	f = open(fname, 'r+')
	for j in range(nframes):
		line = f.readline()
		while ('ITEM: ATOMS' not in line):
			if ('ITEM: NUMBER OF ATOMS' in line):
				line = f.readline()
				natom = int(line)
			else:
				line = f.readline()
		line = line.split()
		type_idx = line.index('type') - 2
		x = line.index('x') - 2
		z = line.index('z') - 1
		want = []
		for i in range(natom):
			line = f.readline().split()
			if int(line[type_idx]) in types:
				want.append(line)
		for k in range(len(ds)):
			curr = h[k]
			temp = []
			hbonded = []
			for l in range(len(want)):
				for m in range(l, len(want)):
					wl = int(want[l][type_idx])
					wm = int(want[m][type_idx])
					if (wl in curr and wm in curr and wm != wl):
						currd = dist(want[l][x:z], want[m][x:z])
						if k == 2 and l not in hbonded and m not in hbonded:
							ds[k].append(currd)
						else:
							ds[k].append(currd)
							if k == 0 and currd < 2.0:
								hbonded.append(l)
								hbonded.append(m)
				
			
	return ds
		
	
	


input_files = sorted(glob.glob("isomer*.dat"))
per_iso = []
for q in range(len(input_files)):
	per_iso.append(read_lammpstrj(input_files[q]))


def compute_rdf(distances, n_bins=100):
    r_max = np.max(distances) + 1
    hist, bin_edges = np.histogram(distances, bins=n_bins, range=(0, r_max))
    r = 0.5 * (bin_edges[1:] + bin_edges[:-1])
    dr = bin_edges[1] - bin_edges[0]
    g_r = hist / len(distances)
    return r, g_r

def main():
    input_files = sorted(glob.glob("isomer_*.dat"))
    for infile in input_files:
        print(f"Processing {infile} ...")
        ds = read_lammpstrj(infile)
        base = os.path.splitext(infile)[0]  # e.g. "isomer-1"
        for i, d in enumerate(ds):
            r, g_r = compute_rdf(d, n_bins)
            outfile = f"{base}_rdf_case{i+1}.dat"
            np.savetxt(outfile, np.column_stack((r, g_r)))
            print(f"  Saved {outfile}")

if __name__ == "__main__":
    main()

