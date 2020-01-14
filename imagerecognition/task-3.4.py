import cv2
import numpy as np
import imutils
from enum import Enum

class ChangeType(Enum):
    GROWTH = 0
    DAMAGE = 1
    BLEACHING = 2
    RECOVERY = 3

def __main__():
    return

def resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    return cv2.resize(image, dim, interpolation=inter)

def trim_to_size(img1, img2):
    height1, width1, channels1 = img1.shape
    height2, width2, channels2 = img2.shape
    w_min = min(width1, width2)
    h_min = min(height1, height1)
    img1 = cv2.resize(img1, (h_min,w_min))
    img2 = cv2.resize(img2, (h_min,w_min))
    return img1, img2

# align the before and after picture to make sure
# they are in the same orientation when comparing
# color
def alignImages(align, ref):
    img1_gray = cv2.cvtColor(align, cv2.COLOR_BGR2GRAY) # REFERENCE IMAGE
    img2_gray = cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY) # IMAGE TO ALIGN WITH REFERENCE
    height, width, channels = ref.shape

    # create ORB detecor (to find keypoints later)
    orb_detector = cv2.ORB_create(5000)

    kp1, d1 = orb_detector.detectAndCompute(img1_gray, None)
    kp2, d2 = orb_detector.detectAndCompute(img2_gray, None)

    matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck = True)

    matches = matcher.match(d1, d2)

    matches.sort(key = lambda x: x.distance)

    matches = matches[:int(len(matches)*90)]
    no_of_matches = len(matches)

    p1 = np.zeros((no_of_matches, 2))
    p2 = np.zeros((no_of_matches, 2))

    for i in range(len(matches)):
      p1[i, :] = kp1[matches[i].queryIdx].pt
      p2[i, :] = kp2[matches[i].trainIdx].pt

    homography, mask = cv2.findHomography(p1, p2, cv2.RANSAC)
    transformed_img = cv2.warpPerspective(align, homography, (width, height))
    return transformed_img

### pre: Requires both img1 and img2 to be the same dimensions.
def matrix_difference(img1, img2):
    img2_color = img2.copy()
    img2_green = img2.copy()
    img2_green[:, :, 0] = 0
    img2_green[:, :, 2] = 0
    img1_green = img1.copy()
    img1_green[:, :, 0] = 0
    img1_green[:, :, 2] = 0

    diff = cv2.absdiff(cv2.GaussianBlur(img1_green, (5, 5), 0),
                       cv2.GaussianBlur(img2_green, (5, 5), 0))
    diff_gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    #cv2.imshow("diff grey", resize(diff_gray, 480))
    ret, thresh = cv2.threshold(diff_gray, 40, 255, cv2.THRESH_BINARY)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:4]
    for c in cnts:
        cv2.drawContours(img2, [c], -1, (255, 0, 255), 3)
    return img2

def from_binary_color(input):
    if(input[0] == 255 and input[1] == 255 and input[2] == 255):
        return True
    return False

def binarize_color(img, boundaries):
    lower = np.array(boundaries[0], dtype="uint8")
    upper = np.array(boundaries[1], dtype="uint8")
    mask = cv2.inRange(img, lower, upper)
    return mask
    # uncomment below lines if you want to visualize the masking.
    #output = cv2.bitwise_and(img, img, mask = mask)
    #return output


def binarization(img):
    #what are the lower and upper of HSV?
    boundariesWhite = [[150, 150, 150], [255, 255, 255]] #change values later!!!
    boundariesPink = [[140, 50, 140], [255, 125, 255]]
    return binarize_color(img, boundariesWhite), binarize_color(img, boundariesPink)

#
# THESE IMAGES MUST BE IN GRAYSCALE!!
#
def classify_change_types(ref_w, ref_p, new_w, new_p):
    scale = 2
    #height, width, channels = ref_w.shape
    #ref_w = cv2.resize(ref_w, (height // scale, width // scale))
    #ref_p = cv2.resize(ref_p, (height // scale, width // scale))
    #new_w = cv2.resize(new_w, (height // scale, width // scale))
    #new_p = cv2.resize(new_p, (height // scale, width // scale))
    #height, width, channels = ref_w.shape

    # Masks of areas where there is coral
    ref_wp = cv2.add(ref_w, ref_p)
    new_wp = cv2.add(new_w, new_p)

    # Get masks of background color (areas where there is no pink/white)
    ref_b = cv2.bitwise_not(ref_wp) # white = background color
    new_b = cv2.bitwise_not(new_wp)

    # Growth: New pink/white in ref background areas
    growth = cv2.bitwise_and(new_wp, new_wp, ref_b)

    # Damage: New background in ref pink/white
    damage = cv2.bitwise_and(new_b, new_b, ref_wp)

    # Bleaching: New white in ref pink
    bleaching = cv2.bitwise_and(new_w, new_w, ref_p)

    # Recovery: New pink in ref white
    recovery = cv2.bitwise_and(new_p, new_p, ref_w)

    ret, thresh = cv2.threshold(growth, 127, 255, 0)
    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cv2.drawContours(growth, cnts, -1, (0, 255, 0), 2)
    cv2.imshow("growth", growth)

    ret, thresh = cv2.threshold(damage, 127, 255, 0)
    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cv2.drawContours(damage, cnts, -1, (255, 0, 0), 2)
    cv2.imshow("damage", damage)

    ret, thresh = cv2.threshold(bleaching, 127, 255, 0)
    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cv2.drawContours(bleaching, cnts, -1, (255, 0, 255), 2)
    cv2.imshow("bleaching", bleaching)

    ret, thresh = cv2.threshold(recovery, 127, 255, 0)
    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cv2.drawContours(recovery, cnts, -1, (0, 255, 255), 2)
    cv2.imshow("recovery", recovery)


img1 = cv2.imread("images/coral1_mod.PNG")
img2 = cv2.imread("images/coral2.PNG")
img1, img2 = trim_to_size(img1, img2)
cv2.imshow("image1", resize(img1, 480))
cv2.imshow("image2", resize(img2, 480))
img2_aligned = alignImages(img2, img1)
cv2.imshow("aligned 2", resize(img2_aligned, 480))
#img_diff = matrix_difference(img1, img3)
#cv2.imshow("diff", resize(img_diff, 480))

img1_w, img1_p = binarization(img1)
img2_w, img2_p = binarization(img2_aligned)

img3 = cv2.cvtColor(cv2.imread("images/identifytest_ref_white.PNG"), cv2.COLOR_BGR2GRAY)
img4 = cv2.cvtColor(cv2.imread("images/identifytest_ref_pink.PNG"), cv2.COLOR_BGR2GRAY)
img5 = cv2.cvtColor(cv2.imread("images/identifytest_new_white.PNG"), cv2.COLOR_BGR2GRAY)
img6 = cv2.cvtColor(cv2.imread("images/identifytest_new_pink.PNG"), cv2.COLOR_BGR2GRAY)

#classify_change_types(img1_w, img1_p, img2_w, img2_p) #Use this to test the new input
classify_change_types(img3, img4, img5, img6) #Use this to test using sample input


cv2.waitKey(0)
