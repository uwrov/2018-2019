import cv2
import numpy
import math
from enum import Enum

def count_shapes(image):
	img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	#process_contours = GripPipeline()
	#img = cv2.imread(sample_image, cv2.IMREAD_GRAYSCALE)
	#var finished_bi_img = process_contours.process(img)
	threshold = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)[1]
	contours, __ = cv2.findContours(threshold, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

	##Not sure if a single line would be regonized as a countor 
	#with two sides or one, therefore leaving the first dictionary just in case.
	shapes = {
		1 : 0,
		2 : 0,
		3 : 0,
		4 : 0,
		5 : 0
	};
	for cnt in contours:
		x,y,__,__ = cv2.boundingRect(cnt)
		if x <= 5 and y <= 5:
			pass
		else:
			approx = cv2.approxPolyDP(cnt, 0.03*cv2.arcLength(cnt, True), True)
			cv2.drawContours(img, [approx],0,(255,0,255),2)
			if len(approx) > 4:
				shapes[5] += 1
			else:
				shapes[len(approx)] += 1


	cv2.imshow("image" , img)
	cv2.imshow("threshold", threshold)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

	print(shapes)
	return(shapes)



def capture_image(address = "http://192.168.8.102:8081/?action=stream"):
	cap = cv2.VideoCapture(address)
	ret, frame = cap.read()
	return frame

img = capture_image()
count_shapes(img)