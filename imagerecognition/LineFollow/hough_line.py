import cv2
import numpy as np

def auto_canny(img, sigma = 0.33):
    v = np.median(img)
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(img, lower, upper)
    return edged

img = cv2.imread("./img/square.jpg")
img = cv2.resize(img, (0, 0), fx = 0.25, fy = 0.25)

# 1
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
mask = cv2.inRange(img, (0, 0, 0), (50, 50, 50))
edges = auto_canny(mask)
# edges = cv2.Canny(img, 75, 120)
lines = cv2.HoughLinesP(edges, 1, np.pi/180, 10, maxLineGap=50)

# # 2
# imghsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
# low_black = np.array([0, 0, 0])
# high_black = np.array([50, 50, 50])
# mask = cv2.inRange(imghsv, low_black, high_black)
# edges = cv2.Canny(mask, 110, 120)
# lines = cv2.HoughLinesP(edges, 1, np.pi/180, 50, maxLineGap=50)

# low_purp = np.array([60, 60, 60])
# high_purp = np.array([70, 70, 70])
# mask = cv2.inRange(img, low_purp, high_purp)
# edge_purp = cv2.Canny(mask, 70, 120)
# lines_purp = cv2.HoughLinesP(edge_purp, 1, np.pi/180, 50, maxLineGap=50)

for line in lines:
    x1, y1, x2, y2 = line[0]    # Output of HoughLinesP() is an array of arrays containing
                                # each two pairs of numbers, the first pair representing (x1, y1) and the second (x2, y2)
    cv2.arrowedLine(img, (x1, y1), (x2, y2), (0, 255, 0), 3)

# cv2.imshow("Edges", mask)
cv2.imshow("edges", edges)
cv2.imshow("Image", img)

cv2.waitKey(0)
cv2.destroyAllWindows()