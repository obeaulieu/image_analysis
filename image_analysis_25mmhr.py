import numpy as np
from scipy import ndimage
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import matplotlib.colors
import glob
import os
from PIL import Image

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
	plt.imshow(croppedim)
	#plt.imshow(a, cmap='gray')
	plt.title(item)	
	plt.show()
	#c.tofile(os.path.splitext(item)[0] + '.bin') #saving as a binary file


