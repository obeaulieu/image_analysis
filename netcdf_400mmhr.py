import numpy as np
from scipy import ndimage
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import matplotlib.colors
import glob
import os
from PIL import Image
from netCDF4 import Dataset
#from osgeo import gdal
from numpy import shape

#import images
filenames = sorted(glob.glob('*.jpg'))

# time steps
runtime_seconds = []
for filename in filenames:
	_runtime = filename.split('_')[-1].split('.')[0]
	runtime_seconds.append(int(_runtime))
	#print _runtime

#Scan Size
xdimension = range(0, 3500)
ydimension = range(0, 1700)

# create a new netCDF file for each experimet
ncfile = '400mmhr_photos.nc'
nc = Dataset(ncfile , 'w' , format='NETCDF4') #nc is now shell for data

#dimensions
x = nc.createDimension('x', len(xdimension))
y = nc.createDimension('y', len(ydimension))
time = nc.createDimension('time', len(filenames))
#dimension variables
x = nc.createVariable('x', 'f4', ('x',))
y = nc.createVariable('y', 'f4', ('y',))
time = nc.createVariable('time', 'u4', ('time',))
nc.variables['x'][:] = np.arange(0, len(xdimension)*1E-3, 1E-3) #convert mm to m
nc.variables['y'][:] = np.arange(0, len(ydimension)*1E-3, 1E-3) #convert mm to m
nc.variables['time'][:] = runtime_seconds
# dimension units
x.units = 'Meters'
y.units = 'Meters'

# variables
nc.createVariable('channel_map', 'u1', ('y', 'x', 'time'))

#Thresholding
i = 0
for filename in filenames:
	print filename
	rgb = mpimg.imread(filename)
	hsv = matplotlib.colors.rgb_to_hsv(rgb)
	a = (hsv[:,:,1] > .50) * (rgb[:,:,1] < 90).astype(float) #
	b = ndimage.filters.gaussian_filter(input=a, sigma=5, order=0) #smoothing parameters
	c = b > .8
	croppedim = c[500:2200, 300:3800] #cropping image 
	#plt.imshow(croppedim)
	#plt.show()
	nc.variables['channel_map'][:,:,i] = croppedim
	i += 1

nc.close() 


