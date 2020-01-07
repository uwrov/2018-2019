import cv2
import numpy

def __main__():
    return

def trim_to_size(img1, img2):
    height1, width1, channels1 = img1.shape
    height2, width2, channels2 = img2.shape
    w_min = min(width1, width2)
    h_min = min(height1, height1)
    img1 = img1[0:h_min, 0:w_min]
    img2 = img2[0:h_min, 0:w_min]
    return img1, img2

def matrixDifference(img1, img2):

    return

def alignImages():
    return

img1 = cv2.imread("images/coral1.PNG")
img2 = cv2.imread("images/coral2.PNG")
img1, img2 = trim_to_size(img1, img2)
cv2.imshow("image1", img1)
cv2.imshow("image2", img2)

cv2.waitKey(0)
