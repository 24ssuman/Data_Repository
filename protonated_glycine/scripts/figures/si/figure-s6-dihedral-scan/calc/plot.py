import math
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from scipy.interpolate import make_interp_spline


nframes = 35
natoms = 11
tokcal = 627.509

dat = np.loadtxt('all.dat')


	
def plot_data(dat):
    # Create a scatter plot of the reference vs prediction
    plt.figure(figsize=(8, 6))
    
    refmin = dat[0][1]
    predmin = dat[0][2]

    plt.scatter(dat[:, 0] - 180, (dat[:, 1] - refmin) * tokcal, label='RI-MP2/aug-cc-pVTZ', color='deepskyblue')
    #plt.plot(dat[:, 0] - 180, (dat[:, 2] - predmin), label='MB-nrg Prediction', color='Red')
    newd = np.linspace(dat[:,0][0], dat[:,0][-1], 500)
    plt.plot(newd - 180, make_interp_spline(dat[:,0], dat[:,2] - predmin)(newd), label='MB-nrg', color='palevioletred')

    yaxes = plt.ylim()
    xaxes = plt.xlim()
    img1 = mpimg.imread('/home/zsolomon/Pictures/dih.png')
    plt.imshow(img1, aspect='auto', extent=[-60, 60, 0, 4], alpha=1.0)

    plt.ylim(yaxes)
    plt.xlim(xaxes)

    # Label the axes
    plt.xlabel(r'$\Psi$')
    plt.ylabel('Energy (kcal/mol)')
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1), ncol = 2)
    plt.tight_layout(rect=[0, 0, 1, 0.97])
    plt.savefig('FigureS6.pdf')
    plt.show()


plot_data(dat)
