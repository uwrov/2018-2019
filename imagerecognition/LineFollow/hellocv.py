import cv2
import numpy as np 
from matplotlib import pyplot as plt

img = cv2.imread('dog.jpg', 0)
px = img[20, 20]

print(px)
print(img.shape)

butt = img[60:80, 40:60]
img[0:20, 0:20] = butt

plt.imshow(img, cmap = 'gray', interpolation = 'bicubic')
plt.xticks([]), plt.yticks([]) # don't show tick marks
plt.show()

print('image shows!')