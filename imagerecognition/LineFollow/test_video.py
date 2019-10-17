import cv2
import time # Remove Later
import numpy as np

video = cv2.VideoCapture("./img/vert2.mp4")
target_low = (0, 0, 0)
target_high = (50, 50, 50)

while True:
    ret, frame = video.read()
    if not ret:
        video = cv2.VideoCapture("./img/vert2.mp4")
        continue

    image = frame
    image = cv2.resize(image, (0,0), fx=0.25, fy=0.25)
    image = cv2.GaussianBlur(image, (5,5), 3)

    Blackline= cv2.inRange(image, target_low, target_high)
    kernel = np.ones((3,3), np.uint8)
    Blackline = cv2.erode(Blackline, kernel, iterations=1)          # Remove noise
    Blackline = cv2.dilate(Blackline, kernel, iterations=9)	        # Restore box sizes
    contours, hierarchy = cv2.findContours(Blackline.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(image, contours, -1, (0, 200, 0), 3)	

    for c in contours:
        x,y,w,h = cv2.boundingRect(c)	   
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 3)
        cv2.line(image, (x+(w//2), 200), (x+(w//2), 250),(255,0,0),3)

    cv2.imshow("orginal with line", image)	
    time.sleep(0.025)
    key = cv2.waitKey(1)

    if key == 27:
        break

cv2.waitKey(0)
cv2.destroyAllWindows()