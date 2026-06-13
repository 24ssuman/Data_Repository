import numpy as np
import glob
import os
import matplotlib.pyplot as plt
import math
#from scipy.optimize import minimize
from scipy.optimize import lsq_linear

# ---- LOAD DATA ---- #
exp = np.loadtxt('experimental.dat')

mb_files = sorted(glob.glob('new_ir*.dat'))
iso = []
for i in range(len(mb_files)):
	iso.append(np.loadtxt(mb_files[i]))

# ---- SET ZERO REGION ---- #
zero = [1800, 2400]

# ---- SET ARRAY ---- #

model = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
length = len(model)
xs_A = [(3656, 3755), (3595, 3656), (3522, 3595), (3345, 3522), (3255, 3345), (3080, 3255), (2990, 3080), (2000, 2010), (2651, 2990), (2000, 2010)]
xs_B = [(3656, 3771), (3538, 3656), (2000, 2010), (3389, 3538), (3301, 3389), (3097, 3301), (3050, 3097), (2899, 3050), (2797, 2899), (2000, 2010)]
xs_exp = [(3677, 3770), (3598, 3677), (3511, 3598), (3305, 3511), (3177, 3305), (3029, 3177), (2952, 3029), (2803, 2952), (2671, 2803), (2546, 2671)]
xs_iso = [xs_A, xs_B]
#xs = [(3700, 3800), (3600, 3700), (3500, 3600), (3100, 3200), (3030, 3100), (2960, 3030), (2900, 2920), (2800, 2900)]

# ---- FIND RELATIVE PEAK HEIGHTS ---- #
def find_max_in_range(dat, x):
	mask = (dat[:,0] >= x[0]) & (dat[:,0] <= x[1])
	return dat[mask, 1].max()

def norm_by_oh(ar):
	norm_val = ar[0]
	for i in range(len(ar)):
		ar[i] /= norm_val
		if ar[i] < 0.025:
			ar[i] = 0
	return ar

def rel_peaks(dat, xs):
	ar = []
	for i in range(len(xs)):
		ar.append(find_max_in_range(dat, xs[i]))
	return norm_by_oh(ar)

# ---- EXPERIMENTAL ---- #
exp_ar = rel_peaks(exp, xs_exp)
print(exp_ar)

# ---- ISOMERS ---- #
iso_ar = []
for j in range(len(iso)):
	iso_ar.append(rel_peaks(iso[j], xs_iso[j]))
	print(iso_ar[j])

#exp_ar = [1.0, 0.43, 0.93, 0.43, 0.12, 0.13, 0.12, 0.41]
#iso_ar = [[1.0, 0.54, 1.06, 0, 0.82, 0.24, 0.16, 2.65],
#		[1.0, 0.23, 0, 0.80, 0.16, 0, 3.70, 0]]


# ---- FIT ---- #

exp_ar = np.asarray(exp_ar)
iso_ar = np.asarray(iso_ar)
A = iso_ar.T

# Least-squares fit with non-negative coefficients
result = lsq_linear(A, exp_ar, bounds=(0, np.inf))

coeffs = result.x

# Reconstructed spectrum
fit = A @ coeffs 


rmsd = np.sqrt(np.mean((exp_ar - fit)**2))

#print("Isomer coefficients:")
#for i, c in enumerate(coeffs):
#    print(f"  Isomer {i+1}: {c:.6f}")

# Normalize to populations (optional)
pop = coeffs / coeffs.sum()
print("\nNormalized populations:")
for i, p in enumerate(pop):
    print(f"  Isomer {i+1}: {p:.4f}")

print(f"\nRMSD: {rmsd:.4e}")



