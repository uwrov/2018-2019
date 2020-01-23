import cv2
import numpy as np
import imutils

RECTANGLE_THRESHOLD = 150
PIXELS_PER_CM = 2
LENGTH = 110
HEIGHT = 50
WIDTH = 50

def getRectangleImage(img, size):
    """ Converts an image to a cropped, translated image of a rectangle
    :param img: The original image (in color)
    :return: A transformed image cropped to the rectangle (or None if none found)
    """
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, binary_img = cv2.threshold(gray_img, RECTANGLE_THRESHOLD, 255, cv2.THRESH_BINARY)
    points = getRectangle(binary_img)
    if points is None:
        print("getRectangleImage(): No Rectangle Found.")
        return None
    processed_img = transformImage(img.copy(), (400, 600), points)

def getRectangle(binary_img):
    """ Finds a rectangle in a binary image and returns its corners (points)
    :param binary_img: black and white image (thresholded image)
    :returns: If there is a rectangle, returns the points as an array.
              Otherwise, returns None.
    """

    #Using cv2.RETR_LIST to prevent nesting contours
    cnts = cv2.findContours(binary_img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    cnts = imutils.grab_contours(cnts)
    # Sorts contours by size and gets largest contour
    cnts = sorted(cnts, key = cv2.contourArea, reverse = True)

    debugImg = cv2.cvtColor(binary_img, cv2.COLOR_GRAY2BGR)
    cv2.drawContours(debugImg, cnts, -1, (255, 0, 255), 3)

    largest_contour = cnts[0]

    epsilon = 0.1*cv2.arcLength(largest_contour,True)
    approx = cv2.approxPolyDP(largest_contour,epsilon,True)

    cv2.drawContours(debugImg, cnts, -1, (0, 255, 255), 8)
    cv2.drawContours(debugImg, [approx], -1, (0, 0, 255), 10)
    cv2.imshow("debug contours", cv2.resize(debugImg, (400, 600)))

    # Extra code to visualize the image
    # test_img = cv2.drawContours(cv2.cvtColor(binary_img.copy(), cv2.COLOR_GRAY2BGR), largest_contour, -1, (255, 0, 255), 8)
    # cv2.imshow("getRectangle Contour Map", test_img)

    if len(approx) == 4:
        return approx
    return None

def transformImage(image, size, points):
    """ Takes in the points of a rectangle and transforms and crops the image to it.
    :param image: The colored, original image.
    :param size: The size of the output image as an array [width, height]
    :param points: The array of points representing the corners of the rectangle.
    :return: A new image
    """

    """ How to get points:
        points[0-3][0][0-1]
               ^ four different points
                       ^ 0 is x and 1 is y

                     b =   0    1      0    1      0    1      0    1
        point[a][0][b] = [[279, 274], [279, 427], [440, 427], [440, 274]]
                     a =   0           1           2           3
    """
    sorted(points, key=lambda point: point[0][0])

    # get left side points
    if(points[0][0][1] < points[1][0][1]):
        topleft = points[0][0]
        bottomleft = points[1][0]
    else:
        topleft = points[1][0]
        bottomleft = points[0][0]

    # get right side points
    if(points[2][0][1] < points[3][0][1]):
        topright = points[2][0]
        bottomright = points[3][0]
    else:
        topright = points[3][0]
        bottomright = points[2][0]
    print(points)

    quadPoints = np.array([topleft, topright, bottomleft, bottomright], dtype = "float32")
    width = size[0]
    height = size[1]
    finalPoints = np.array([
        [0, 0],
        [width, 0],
        [0, height],
        [width, height]],
        dtype = "float32")

    transform = cv2.getPerspectiveTransform(quadPoints, finalPoints) #Get matrix
    output = cv2.warpPerspective(image, transform, size) #Transform image
    cv2.imshow("output", output)




#image = cv2.imread("images/test3.JPG")
end = (WIDTH * PIXELS_PER_CM, HEIGHT * PIXELS_PER_CM)
side = (LENGTH * PIXELS_PER_CM, HEIGHT * PIXELS_PER_CM)
top = (LENGTH * PIXELS_PER_CM, WIDTH * PIXELS_PER_CM)
sizes = [end, side, end, side, top]
sizesIndex = 0
outputImages = []

while(sizesIndex < len(sizes)) {
    #process and show image
    #Get camera feed => pass to getRectangleImage(feed, sizes[sizesIndex])
    #save image when clicked
    if(False): #clicked:
        #outputImages = image
        #sizesIndex++

#show images correctly

#getRectangleImage(image)
cv2.waitKey(0)
