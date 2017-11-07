import numpy as np
from scipy import ndimage
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import matplotlib.colors
import glob
import os
from PIL import Image
#from netCDF4 import Dataset
#from osgeo import gdal
from numpy import shape

#import images
filename = sorted(glob.glob('*.jpg'))

#Thresholding
for item in filename:
	rgb = mpimg.imread(item)
	hsv = matplotlib.colors.rgb_to_hsv(rgb)
	a = (hsv[:,:,1] > .45) * (rgb[:,:,1] < 80).astype(float) #
	b = ndimage.filters.gaussian_filter(input=a, sigma=5, order=0) #smoothing parameters
	c = b > .8	
	croppedim = c[500:2200, 300:3800] #cropping image 
	#plt.imshow(croppedim)
	#plt.imshow(a, cmap='gray')
	#plt.title(item)	
	#plt.show()
	#c.tofile(os.path.splitext(item)[0] + '.bin') #saving as a binary file

# Create new list with new processed images
filename_new = []
for fi in filename:
	filename_new.append(os.path.splitext(fi)[0] + '_analyzed' + '.jpg')

# Copy the files to a processed images folder
try:
    os.mkdir('../Photos_analyzed')
except:
    pass
for i in range(len(filename)):
    print filename[i], '-->', filename_new[i]
    shutil.copyfile(filename[i], '../Photos_analyzed/' + filename_new[i])


# Data organization
# Using a netCDF to organize photos and scan data from DB1

"""
# create a new netCDF file
file = 'ExperimentScans.nc'
nc = Dataset(file , 'w' , format='NETCDF4') #nc is now shell for data
#print (nc.file_format)

#data input                                                       
datafiles = sorted(glob.glob('*.DAT'))

#Scan Size
xdimension = range(0, 3500)
ydimension = range(0, 1700)
                                                        
#dimensions
x = nc.createDimension('x', len(xdimension))
y = nc.createDimension('y', len(ydimension))
time = nc.createDimension('time', len(datafiles))
                                                        
#variables
x = nc.createVariable('x', 'f4', ('x',))
y = nc.createVariable('y', 'f4', ('y',))
time = nc.createVariable('time', 'f4', ('time',))
nc.createVariable('Scans_Visualization', 'f4', ('y', 'x', 'time'))

#data transformation
t_scan = []
i = 0
for datafile in datafiles:
    z1D = np.fromfile(datafile, dtype=np.float32)
    z = np.reshape(z1D, (-1, 3936))
    z[z == -9999] = np.nan # no data handling
    #z = np.flipud(z) # flip top to bottom
    nc.variables['Scans_Visualization'][:, :, i] = z
    print datafile
    t_scan.append(int(datafile.split('TopoDat_')[1].split('.')[0]))
    i += 1

nc.variables['x'][:] = np.arange(0, len(x)*1E-3, 1E-3) #convert mm to m
nc.variables['y'][:] = np.arange(0, len(y)*1E-3, 1E-3) #convert mm to m
nc.variables['time'][:] = np.array(t_scan)

x.units = 'Meters'
y.units = 'Meters'

nc.close() 

#Create new dataset for photographs of experiments
file = 'ExperimentPhotographs.nc'
nc = Dataset(file , 'w' , format='NETCDF4')

#data input
datafiles_p = glob('*.jpg')

#Image size
xpdimension = range(0, 4288)
ypdimension = range(0, 2848)
rgbdimension = 3
                                                        
#dimensions
xp = nc.createDimension('xp', len(xpdimension))
yp = nc.createDimension('yp', len(ypdimension))
timep = nc.createDimension('timep', len(datafiles_p))
rgb = nc.createDimension('rgb', rgbdimension)

                                                        
#variables
xp = nc.createVariable('xp', 'f4', ('xp',))
yp = nc.createVariable('yp', 'f4', ('yp',))
timep = nc.createVariable('timep', 'f4', ('timep',))
rgb = nc.createVariable('rgb', 'f4', ('rgb',))
nc.createVariable('Photographs_Visualization', 'f4', ('yp', 'xp', 'timep', 'rgb'))

#data transformation
t_pic = []
i = 0
for datafilep in datafiles_p:
    z1Dp = scipy.ndimage.imread(datafilep, False, 'RGB')
    #print(z1Dp.shape)
    #zp = np.ndarray.reshape(z1Dp, (-1, 4288, 3))
    #zp[zp == -9999] = np.nan # no data handling
    z1Dp = np.flipud(z1Dp) # flip top to bottom
    nc.variables['Photographs_Visualization'][:, :, i, :] = z1Dp
    print datafilep
    t_pic.append(int(datafilep.split('Img')[1].split('.')[0]))
    i += 1

nc.variables['xp'][:] = np.arange(0, len(xp)*1E-3, 1E-3)
nc.variables['yp'][:] = np.arange(0, len(yp)*1E-3, 1E-3)
nc.variables['rgb'][:] = np.arange(0, 3)
nc.variables['timep'][:] = np.array(t_pic)

xp.units = 'Meters'
yp.units = 'Meters'

nc.close()
"""

