import cv2
import numpy as np
import imutils

RECTANGLE_THRESHOLD = 150
PIXELS_PER_CM = 2
LENGTH = 110
HEIGHT = 50
WIDTH = 50
DISPLAY_IMAGE_SCALE = 1
IMAGE_CORNER = (30, 30)

captureButtonLastState = False
captureButtonCurrentState = False

def resizeWithAspectRatio(image, width=None, height=None, inter=cv2.INTER_AREA):
    """ Resizes an image while maintaining aspect ratio.

    """

    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    return cv2.resize(image, dim, interpolation=inter)

def getRectangleImage(img, size):
    """ Converts an image to a cropped, translated image of a rectangle
    :param img: The original image (in color)
    :return: A transformed image cropped to the rectangle (or None if none found)
    :return: Points defining the rectangle found
    """
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, binary_img = cv2.threshold(gray_img, RECTANGLE_THRESHOLD, 255, cv2.THRESH_BINARY)
    points = getRectangle(binary_img)

    if points is None:
        #print("getRectangleImage(): No Rectangle Found."
        return None, None

    transformed_img = transformImage(img.copy(), size, points)
    return transformed_img, points

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

    if len(cnts) == 0:
        return None

    largest_contour = cnts[0]
    epsilon = 0.1*cv2.arcLength(largest_contour,True)
    approx = cv2.approxPolyDP(largest_contour,epsilon,True)

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
                       ^ 0 is y and 1 is x

                     b =   0    1      0    1      0    1      0    1
        point[a][0][b] = [[279, 274], [279, 427], [440, 427], [440, 274]]
                     a =   0           1           2           3
    """
    sorted(points, key=lambda point: point[0][1], reverse = True)

    # get left side points
    if(points[0][0][0] < points[1][0][0]):
        topleft = points[0][0]
        bottomleft = points[1][0]
    else:
        topleft = points[1][0]
        bottomleft = points[0][0]

    # get right side points
    if(points[2][0][0] < points[3][0][0]):
        topright = points[2][0]
        bottomright = points[3][0]
    else:
        topright = points[3][0]
        bottomright = points[2][0]
    #print(points)

    quadPoints = np.array([topleft, topright, bottomleft, bottomright], dtype = "float32")
    height = size[0]
    width = size[1]
    finalPoints = np.array([
        [0, 0],
        [height, 0],
        [0, width],
        [height, width]],
        dtype = "float32")

    transform = cv2.getPerspectiveTransform(quadPoints, finalPoints) #Get matrix
    output = cv2.warpPerspective(image, transform, size) #Transform image
    return output

def scaleTupleArray(array, scale):
    output = [None] * len(array)
    for i in range(len(array)):
        output[i] = (int(array[i][0] * scale), int(array[i][1] * scale))
    return output

""" Main
"""

#image = cv2.imread("images/test3.JPG")
end = (WIDTH * PIXELS_PER_CM, HEIGHT * PIXELS_PER_CM)
side = (LENGTH * PIXELS_PER_CM, HEIGHT * PIXELS_PER_CM)
top = (LENGTH * PIXELS_PER_CM, WIDTH * PIXELS_PER_CM)
sizes = [end, side, end, side, top]
imageSizes = scaleTupleArray(sizes, DISPLAY_IMAGE_SCALE)

imageIndex = 0
outputImages = [None] * 5

cap = cv2.VideoCapture(1)

if(cap.isOpened()):
    print("Opened camera.")
            #outputImages = image
            #sizesIndex++
    while(imageIndex < len(sizes)):
        # Capture frame-by-frame
        ret, image = cap.read()
        image = resizeWithAspectRatio(image, width = 800)
        warpedImage, points = getRectangleImage(image.copy(), sizes[imageIndex])

        k = cv2.waitKey(1) & 0xFF
        if k == ord('q'):
            cv2.destroyAllWindows()
            break
        elif k == ord('c'):
            captureButtonCurrentState = True
        else:
            captureButtonCurrentState = False

        x, y = IMAGE_CORNER
        for i in range(imageIndex):
            width, height = imageSizes[i]
            resized_img = cv2.resize(outputImages[i].copy(), (width, height))
            print("x: {}, y: {}, width: {}, height: {}".format(x, y, width, height))
            print(resized_img.shape)
            image[y:y + height, x:x + width] = resized_img
            x += width

        if points is not None and warpedImage is not None:
            cv2.drawContours(image, [points], -1, (0, 0, 255), 4)
            width, height = imageSizes[imageIndex]
            shrink_img = cv2.resize(warpedImage.copy(), (width, height))
            image[y:y + height, x:x + width] = shrink_img
            if (captureButtonCurrentState and not captureButtonLastState):
                # time to capture!!!
                outputImages[imageIndex] = warpedImage;
                print("Captured image {}.".format(imageIndex))
                imageIndex += 1;

        cv2.imshow("Camera View", image)
        captureButtonLastState = captureButtonCurrentState

else:
    print("Failed to get camera.")
#getRectangleImage(image)
