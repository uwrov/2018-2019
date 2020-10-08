import cv2
import numpy as np
import imutils

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
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    boundariesWhite = [[180, 180, 180], [255, 255, 255]]
    #boundariesPink = [[140, 50, 140], [255, 135, 255]] the old values for pink (too segmented)
    boundariesPink = [[140, 0, 140], [255, 135, 255]]
    return binarize_color(img, boundariesWhite), binarize_color(img, boundariesPink)

#int, int, int, int, string
def drawing_bounding_boxes(x, y, w, h, tp, img):
    count = 0
    if(tp == 'growth'):
        img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),3)
        count += 1
    elif(tp == 'damage'):
        img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,255),3)
        count += 1
    elif(tp == 'bleaching'):
        img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),3)
        count += 1
    elif(tp == 'recovery'):
        img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),3)
        count += 1
    if(count > 4):
        print("too many detected areas!!")
    return img

# THESE IMAGES MUST BE IN GRAYSCALE!!
def classify_change_types(ref_w, ref_p, new_w, new_p, img2):
    scale = 2 #I don't think this is ever used

    # "stitches" white and pink parts into a full coral image
    ref_wp = cv2.bitwise_or(ref_w, ref_p)
    new_wp = cv2.bitwise_or(new_w, new_p)
    cv2.imshow("ref_wp", ref_wp)
    cv2.imshow("new_wp", new_wp)

    # inverts the "stitched" images
    # white = background color
    ref_b = cv2.bitwise_not(ref_wp) #never actually used
    new_b = cv2.bitwise_not(new_wp)
    cv2.imshow("ref_b", ref_b)
    cv2.imshow("new_b", new_b)

    # Growth
    # white in any place coral has ever existed
    # combines new and old coral to have one big happy coral
    growth = cv2.bitwise_or(new_wp, ref_wp)
    cv2.imshow("growth", growth)
    # where old and "growth" differ
    # filters out any lack of change
    # white where growth occured
    shiftedGrowth = cv2.bitwise_xor(ref_wp, growth)
    shiftedGrowth = cv2.GaussianBlur(shiftedGrowth, (5, 5), 0)

    # Note: the above process for determining growth seems a bit convoluted
    # I think we can just do the opposite of "damage"
    # new_growth = cv2.bitwise_and(ref_b, new_wp)
    # cv2.imshow("growth?", new_growth)
    # This appears to have the same result as above

    # Damage
    # compares inverted new coral and regular old coral
    # white in places where damage occured
    damage = cv2.bitwise_and(new_b, ref_wp)

    # Bleaching
    # compares new white coral and old pink coral
    # white where bleaching occured
    bleaching = cv2.bitwise_and(new_w, ref_p)

    # Recovery
    # compares new pink coral and old white coral
    # white where recovery occured
    recovery = cv2.bitwise_and(new_p, ref_w)

    # Drawing bounding boxes
    # I think that the boxes are drawn according to the tiny reference images provided
    # but they're drawn on a big final image so things look wonky
    # it also only works for recovery (and possibly damage since there's none of that in this example)
    # but I think that's because the other images weren't very distinct in where growth/damage occured

    ret, thresh = cv2.threshold(shiftedGrowth, 127, 255, 0)#growth
    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    shiftedGrowth = cv2.cvtColor(shiftedGrowth, cv2.COLOR_GRAY2BGR)
    for c in cnts:
        #cv2.drawContours(shiftedGrowth, c, -1, (0, 0, 255), 2)
        x,y,w,h = cv2.boundingRect(c)
        area = cv2.contourArea(c)
        if(h/w > 1 and h/w < 2 and area > 2000):
            img2 = drawing_bounding_boxes(x, y, w, h, 'growth', img2)
    cv2.imshow('shiftedGrowth', shiftedGrowth)

    ret, thresh = cv2.threshold(damage, 127, 255, 0)#damage
    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    damage = cv2.cvtColor(damage, cv2.COLOR_GRAY2BGR)
    for c in cnts:
        x,y,w,h = cv2.boundingRect(c)
        area = cv2.contourArea(c)
        if(h/w > 1 and h/w < 2 and area > 2000):
            img2 = drawing_bounding_boxes(x, y, w, h, 'damage', img2)
    cv2.imshow("damage", damage)

    ret, thresh = cv2.threshold(bleaching, 127, 255, 0)#bleaching
    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    bleaching = cv2.cvtColor(bleaching, cv2.COLOR_GRAY2BGR)
    for c in cnts:
        x,y,w,h = cv2.boundingRect(c)
        area = cv2.contourArea(c)
        if(h/w > 1 and h/w < 5):
            img2 = drawing_bounding_boxes(x, y, w, h, 'bleaching', img2)
    cv2.imshow("bleaching", bleaching)

    ret, thresh = cv2.threshold(recovery, 127, 255, 0)#recovery
    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    recovery = cv2.cvtColor(recovery, cv2.COLOR_GRAY2BGR)
    for c in cnts:
        x,y,w,h = cv2.boundingRect(c)
        area = cv2.contourArea(c)
        if(h/w > 1 and h/w < 5):
            img2 = drawing_bounding_boxes(x, y, w, h, 'recovery', img2)
    cv2.imshow("recovery", recovery)

    cv2.imshow('final', img2)

# get images
img1 = cv2.imread("old_coral.png")
img2 = cv2.imread("new_coral.png")
# resize images
img1, img2 = trim_to_size(img1, img2)
# show resized images
#cv2.imshow("image1", resize(img1, 480))
#cv2.imshow("image2", resize(img2, 480))

# realign second image to better compare with first image
img2_aligned = alignImages(img2, img1)
# show realigned image
#cv2.imshow("aligned 2", resize(img2_aligned, 480))

# resize realigned image
# this is the big final image that the bounding boxes will be drawn on
res = cv2.resize(img2_aligned,(820,710), interpolation = cv2.INTER_LINEAR)

# converts the corals to black and white images,
# with either the white part or the pink part
# displayed as white and the rest blacked out
img1_w, img1_p = binarization(img1)
img2_w, img2_p = binarization(img2_aligned)
new_wp = cv2.bitwise_or(img2_w, img2_p)
new_wp  = cv2.cvtColor(new_wp, cv2.COLOR_GRAY2BGR)
# white coral shown
cv2.imshow("img1_w", img1_w)
cv2.imshow("img2_w", img2_w)
# pink coral shown
cv2.imshow("img1_p", img1_p)
cv2.imshow("img2_p", img2_p)

# determine any changes between the first and second images
# and draw bounding boxes on final image
classify_change_types(img1_w, img1_p, img2_w, img2_p, res) #Use this to test the new input
#classify_change_types(img3, img4, img5, img6) #Use this to test using sample input


cv2.waitKey(0)

cv2.destroyAllWindows()


#TODO
#   make pink less noisey (damage, growth)
#   draw the bounding boxes on img2

'''
use histogram to get rid of background, then use it to create threshold in middle between white and pink and use that to create two images, one
that is white and one that is pink
'''
