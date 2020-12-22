#%%
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage

df = np.load("eg2.npy")
# x/y grid center points
x_cords = np.linspace(0.1, 5.9, 30)
y_cords = np.linspace(0.1, 1.9, 10)
xv, yv = np.meshgrid(x_cords, y_cords, sparse=False, indexing="ij")
# one timestep only

df = df[:, :, 13]
# source coords
x_s = 0.5
y_s = 1
# populate z set
z = np.zeros((30, 10))
for x in range(30):
    for y in range(10):
        z[x, y] = df[x, y] / 0.095 * 100


# contour plotprint(
plt.figure(figsize=(12, 6))
plt.contourf(xv, yv, z)
plt.plot(x_s, y_s, "xr", markersize=12)
plt.xlabel("x distance / m")
plt.ylabel("y distance / m")
plt.show()
# grid plot
plt.figure(figsize=(12, 6))
plt.pcolormesh(xv, yv, z, cmap=plt.cm.Greens_r)
plt.show()
plt.plot(x_s, y_s, "xr", markersize=12)
plt.xlabel("x distance / m")
plt.ylabel("y distance / m")
plt.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax)
plt.show()
# %%
import pylab as plb
from scipy.optimize import curve_fit
from scipy import asarray as ar,exp

x = y_cords
y = z
n = len(y)                          #the number of data
mean = sum(x*y)/n                   #note this correction
sigma = np.sqrt(sum(y*(x-mean)**2)/n)       #note this correction
#%%
def gaus(x,a,x0,sigma):
    return a*exp(-(x-x0)**2/(2*sigma**2))

popt,pcov = curve_fit(gaus,x,y,p0=[1,mean,sigma])

plt.plot(x,y,'b+:',label='data')
plt.plot(x,gaus(x,*popt),'ro:',label='fit')
plt.legend()
plt.title('Fig. 3 - Fit for Time Constant')
plt.xlabel('Time (s)')
plt.ylabel('Voltage (V)')
plt.show()
# %%
