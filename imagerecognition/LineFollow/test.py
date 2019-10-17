import cv2
import numpy as np

image = cv2.imread("./img/line.png")
image = cv2.resize(image, (0,0), fx=3, fy=3)

height, width = image.shape[:2]
vert_h = int(width / 3)
horz_h = int(height / 3)
xs = list(range(0, width + 1, vert_h))
ys = list(range(0, height + 1, horz_h))

print(xs[2])
print(ys)
y0 = 1
x0 = 1
image = image[ys[y0]:ys[y0+1], xs[x0]:xs[x0+1]]

Blackline= cv2.inRange(image, (0,0,0), (50,50,50))
kernel = np.ones((3,3), np.uint8)
Blackline = cv2.erode(Blackline, kernel, iterations=1)
Blackline = cv2.dilate(Blackline, kernel, iterations=9)	
contours, hierarchy = cv2.findContours(Blackline.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(image, contours, -1, (0, 200, 0), 3)	

if len(contours) > 0 :
   x,y,w,h = cv2.boundingRect(contours[0])	   
   cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 3)
   cv2.line(image, (x+(w//2), (height//6) - 10), (x+(w//2), (height//6) + 10),(255,0,0),3)

# cv2.imshow("blackline", Blackline)
cv2.imshow("orginal with line", image)	

cv2.waitKey(0)
cv2.destroyAllWindows()