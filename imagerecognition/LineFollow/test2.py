import cv2
import numpy as np

image = cv2.imread("./img/line.png")

# Gather dimensions of image to form grid over it. Try to find things in each box
image = cv2.resize(image, (0,0), fx=2, fy=2)
height, width = image.shape[:2]

vert_h = width//3
horz_h = height//3
xs = list(range(0, width + 1, vert_h))
ys = list(range(0, height + 1, horz_h))

for ii in range(3):
    for jj in range(3):
        pt1 = (xs[ii], ys[jj])
        pt2 = (xs[ii+1], ys[jj+1])

        cv2.rectangle(image, pt1, pt2, (255, 255, 0), 3)
        seg = image[ys[jj]:ys[jj+1], xs[ii]:xs[ii+1]]

        #----------------------------------------------------------------------------------------------
        gray_seg = cv2.cvtColor(seg, cv2.COLOR_BGR2GRAY)
        
        kernel = np.ones((3, 3), np.uint8)
        black = cv2.inRange(seg, (0,0,0), (50,50,50))
        # black = cv2.erode(black, kernel, iterations = 1)
        black = cv2.dilate(black, kernel, iterations = 10)
        contours, _ = cv2.findContours(black.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(seg, contours, -1, (0, 200, 0), 3)
        #-----------------------------------------------------------------------------------------------

        for c in contours:
            x,y,w,h = cv2.boundingRect(c)
            cv2.rectangle(seg, (x, y), (x+w, y+h), (0,0,255), 3)
            cv2.line(seg, (x+(w//2), (y + h//2)-5), (x+(w//2), (y + h//2)+5), (255,0,255),3)

cv2.imshow('img', image)
# cv2.imshow('noise reduced', noise_begone)

cv2.waitKey(0)
cv2.destroyAllWindows()