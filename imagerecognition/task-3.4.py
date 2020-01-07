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

# align the before and after picture to make sure
# they are in the same orientation when comparing
# color
def alignImages(img1, img2):
    img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY) # REFERENCE IMAGE
    img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY) # IMAGE TO ALIGN WITH REFERENCE
    height, width = img2.shape

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
    transformed_img = cv2.warpPerspective(img1_gray, homography, (width, height))
    return transformed_img

### pre: Requires both img1 and img2 to be the same dimensions.
def matrix_difference(img1, img2):
    out = cv2.absdiff(img1, img2)
    return out

img1 = cv2.imread("images/coral1.PNG")
img2 = cv2.imread("images/coral2.PNG")
img1, img2 = trim_to_size(img1, img2)
cv2.imshow("image1", img1)
cv2.imshow("image2", img2)
img_diff = matrix_difference(img1, img2)
cv2.imshow("diff", img_diff)

cv2.waitKey(0)
