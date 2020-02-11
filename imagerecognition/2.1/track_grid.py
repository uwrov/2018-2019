import cv2
import numpy as np

# This script will track where the ROV is over a grid,
# and give a visual representation of position.


def main():
    # Grab video feed from source
    # cap = cv2.VideoCapture('http://10.19.52.3:8080/video/mjpeg')
    # height, width, _ = cap.read()[1].shape

    # while True:
    # _, frame = cap.read()

    im = cv2.imread('poopie.png')

    # convert rgb image to hsv for color isolation
    hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)

    # Set bounds for what shades of pink we want
    lower_pink = np.array([130, 25, 160])
    upper_pink = np.array([170, 255, 255])

    # Isolate blue, draw lines on edges
    mask = cv2.inRange(hsv, lower_pink, upper_pink)
    mask = cv2.GaussianBlur(mask, (5, 5), 0)

    # Isolate lines
    edges = cv2.Canny(mask, 75, 150)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 50, maxLineGap=50)

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(im, (x1, y1), (x2, y2), (0, 255, 0), 5)

    cv2.imshow('hi', im)
    cv2.imshow("bye", mask)
    cv2.waitKey(0)


if __name__ == '__main__':
    main()