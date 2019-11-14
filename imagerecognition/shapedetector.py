
import cv2

class ShapeDetector:
    def __init__(self):
        pass

    def detect(self, c):
        #initialize the shape name and approximate the contour
        shape = "unidentified"
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)

        # if the shape is a triangle, it will have 3 vertices
        if len(approx) == 3:
            shape = "triangle"
        elif len(approx) == 4:
            shape = "square"
        elif len(approx) == 2:
            shape = "line"
        else:
            shape = "circle"

        return shape
