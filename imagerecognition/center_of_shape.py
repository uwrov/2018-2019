# -*- coding: utf-8 -*-
"""
Created on Wed Dec 19 18:38:44 2018

@author: Peyton Lee

Following tutorial from:
    https://www.pyimagesearch.com/2016/02/01/opencv-center-of-contour/
"""

import cv2
import imutils
import argparse

#constructs argument parse, parses arguments
#An Argument Parser sets up certain arguments/parameters
#required to initialize a command or python script.
#In this case, we require that an image path be included.
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="path to the input image")
args = vars(ap.parse_args())

#load in the image, convert to grayscale, blur
#threshold it (only show above certain value)
image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]
cv2.bitwise_not ( thresh, thresh );

#find countours in the thresholded image
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

# loop over the contours
for c in cnts:
	# compute the center of the contour
	M = cv2.moments(c)
	cX = int(M["m10"] / M["m00"])
	cY = int(M["m01"] / M["m00"])
 
	# draw the contour and center of the shape on the image
	cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
	cv2.circle(image, (cX, cY), 7, (255, 255, 255), -1)
	cv2.putText(image, "center", (cX - 20, cY - 20),
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
 
	# show the image
	cv2.imshow("Image", image)
	cv2.waitKey(0)
