import matplotlib.pyplot as plt
import numpy as np
import math




def get_data(fname, nlines):
	f = open(fname, 'r+')
	freq = []
	inten = []
	for i in range(nlines):
		line = f.readline().split()
		freq.append(float(line[0]))
		inten.append(float(line[1]))
	return freq, inten


xi, yi = get_data('ir.dat', 12500)
xn, yn = get_data('nh3.dat', 1562)
xpoh, ypoh = get_data('poh.dat', 1562)
xwoh, ywoh = get_data('woh.dat', 1562)
xv, yv = get_data('vv.dat', 1562)

figure, axis = plt.subplots(5, 1, figsize=(5,5))

axis[0].plot(xv, yv)
axis[0].set_title('vvtcf')
ax0 = plt.subplot(5, 1, 1)
ax0.set_xlim([2200, 3800])
#ax0.set_ylim([0, 0.0007])

axis[1].plot(xpoh, ypoh)
axis[1].set_title('pgl-oh stretches')
ax1 = plt.subplot(5, 1, 2)
ax1.set_xlim([2200, 3800])
#ax2.set_ylim([0, 0.0014])

axis[2].plot(xwoh, ywoh)
axis[2].set_title('water-oh stretches')
ax2 = plt.subplot(5, 1, 3)
ax2.set_xlim([2200, 3800])
#ax2.set_ylim([0, 0.0014])


axis[3].plot(xn, yn)
axis[3].set_title('nh stretches')
ax3 = plt.subplot(5, 1, 4)
ax3.set_xlim([2200, 3800])
#ax3.set_ylim([0, 0.0009])


axis[4].plot(xi, [v + 6 for v in yi])
axis[4].set_title('ir spectra')
ax4 = plt.subplot(5, 1, 5)
ax4.set_xlim([2200, 3800])
ax4.set_ylim([0, 45])


ax0.grid(which='both')
ax1.grid(which='both')
ax2.grid(which='both')
ax3.grid(which='both')
ax4.grid(which='both')


plt.tight_layout()

plt.savefig('high.png')
plt.show()
