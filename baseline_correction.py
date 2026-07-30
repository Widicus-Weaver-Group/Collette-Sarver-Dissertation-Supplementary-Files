import matplotlib.pyplot as plt
import numpy as np
import pybaselines
from pybaselines import utils
import csv

data = np.genfromtxt('/Users/morgangiese/Desktop/Practice/rawspectra/x1y1.csv', delimiter=",", skip_header=0, names=["x", "y"]) #'datafile' is name of file
xdata = data['x']
ydata = data['y']


bkg_1 = pybaselines.polynomial.imodpoly(ydata, xdata, poly_order=3)[0]

plt.plot(xdata, ydata, label='raw data', lw=1.5)
plt.plot(xdata, bkg_1, '--', label='modpoly')

plt.legend()
plt.show()


newintensities = ydata - bkg_1


plt.plot(xdata, ydata, label='raw data', lw=1.5)
plt.plot(xdata, newintensities, '--', label='newspectra')

plt.legend()
plt.show()
