import cv2
import numpy

def __main__():
    return


### Crops the given images to be the same size (min width and height)
def trim_to_size(img1, img2):
    height1, width1, channels1 = img1.shape
    height2, width2, channels2 = img2.shape
    w_min = min(width1, width2)
    h_min = min(height1, height1)
    img1 = img1[0:h_min, 0:w_min]
    img2 = img2[0:h_min, 0:w_min]
    return img1, img2

### pre: Requires both img1 and img2 to be the same dimensions.
def matrix_difference(img1, img2):
    out = cv2.absdiff(img1, img2)
    return out

def alignImages():
    return

img1 = cv2.imread("images/coral1.PNG")
img2 = cv2.imread("images/coral2.PNG")
img1, img2 = trim_to_size(img1, img2)
cv2.imshow("image1", img1)
cv2.imshow("image2", img2)
img_diff = matrix_difference(img1, img2)
cv2.imshow("diff", img_diff)

cv2.waitKey(0)
