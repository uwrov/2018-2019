"""Identifies shapes in a given cell of data

- Take in a cell
- Use CV to identify what kind of shape the image is
  - shapes are either polygons or objects which reach 2 cells
- Return a list of shape identifies
  - options include: 'coral', 'coral fragment', 'star', 'sponge', 'empty'

"""

import cv2
import pickle
import numpy as np
import imutils

BLACK = ([40, 35, 40], [145, 133, 128])
RED = ([0, 10, 100], [120, 100, 230])
YELLOW = ([0, 150, 180], [25, 180, 210])
WHITE = 195

def identify_shapes(row):
    """Identifies the shapes in the row

        Args:
            row: list of images to be analyzed

        Returns:
            A list of strings representing the
            objects located in each cell.
    """

    names = []

    for img in row:
        shape = get_shapes(img)
        names.append(shape)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return names

def get_shapes(img):
    """Identifies the shape of the image

        Args:
            img: the image to be analyzed

        Returns:
            The shape identified in the image
    """

    area = []

    # analyze the image for all possible colors
    black = change_color(img, BLACK)
    black_cnts = get_contours(black)
    area.append(get_area(black))

    red = change_color(img, RED)
    red_cnts = get_contours(red)
    area.append(get_area(red))

    yellow = change_color(img, YELLOW)
    yellow_cnts = get_contours(yellow)
    # if there are no contours, use this fake value instead
    if len(yellow_cnts) == 0:
        yellow_cnts = [0,0,0,0,0,0,0,0,0,0]
    area.append(get_area(yellow))

    white = change_white(img)
    white_cnts = get_contours(white)
    area.append(get_area(white))

    # determine which color was the most appropriate and return the shape
    contours = [black_cnts, red_cnts, yellow_cnts, white_cnts]
    color = get_color(contours)
    return get_shape(area[color], color)

def change_white(img):
    """Prepares the image to be tested as a 'sponge'

        Args:
            img: the image to be analyzed

        Returns:
            The blurred, binary version of the image
            with whitish values staying white
            and all other values turning black
    """
    grayscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(grayscale, WHITE, 255, cv2.THRESH_BINARY)

    blur = cv2.bilateralFilter(binary,9,75,75)
    return blur

def change_color(img, color):
    """Prepares the image to be tested as a specified shape

        Args:
            img: the image to be analyzed
            color: the color associated with the shape being tested
                (black = coral, red = star, yellow = coral fragment,
                white = sponge and is handled differently in 'change_white')

        Returns:
            The blurred, binary version of the image
            with the specified color turning white
            and all other values turning black
    """
    boundaries = [color]

    output = img
    # loop over the boundaries
    for (lower, upper) in boundaries:
    	# create NumPy arrays from the boundaries
        lower = np.array(lower, dtype = "uint8")
        upper = np.array(upper, dtype = "uint8")
    	# find the colors within the specified boundaries and apply
    	# the mask
        mask = cv2.inRange(img, lower, upper)
        output = cv2.bitwise_and(img, img, mask = mask)
    	# show the images
    	#cv2.imshow("images", np.hstack([cf, output]))

    grayscale = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(grayscale, 1, 255, cv2.THRESH_BINARY)

    blur = cv2.bilateralFilter(binary,9,75,75)
    return blur

def get_contours(img):
    """Gets the contours of the binary image

        Args:
            img: the binary image that was returned from
            either 'change_white' or 'change_color'

        Returns:
            An array of the contours of the image
    """
    cnts = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    #cv2.drawContours(img, cnts, 2, (179,178,176), 3)

    contours = []
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)
        contours.append(len(approx))

    return contours

def get_color(cnts):
    """Determines the color of the shape we're trying to identify

        Args:
            cnts: an array of all the contour arrays after
            analyzing all possible colors of an image,
            organized as: [black_cnts, red_cnts, yellow_cnts, white_cnts]

        Returns:
            The index of 'cnts' that has the shortest array length,
            which corresponds to which color it is
    """
    # The shorter the length of the array at a given index, the more likely
    # that the image is a cohesive shape (rather than a bunch of noise that
    # was picked up)
    cntlengths = []
    for cnt in cnts:
        cntlengths.append(len(cnt))
    return cntlengths.index(min(cntlengths))

def get_area(img):
    """Calculates the area of the shape

        Args:
            img: the binary image that was returned from
            either 'change_white' or 'change_color'

        Returns:
            The area of the white part of the image
    """
    area = cv2.countNonZero(img)
    return area

def get_shape(area, color):
    """Identifies the shape

        Args:
            area: the area of the shape
            color: the numerical value associated with
            the color this image was determined to be

        Returns:
            The name of the shape
    """
    # if the area is large enough, it probably was not random noise
    # from an empty image and there is an actual object
    if area > 1000:
        if color == 0:
            return "coral"
        elif color == 1:
            return "star"
        elif color == 2:
            return "coral fragment"
        else:
            return "sponge"
    else:
        return "empty"

if __name__ == '__main__':
    # Test driver
    # row = []
    # with open('list.pkl', 'rb') as f:
    #     row = pickle.load(f)

    coral = cv2.imread("coral.png", cv2.IMREAD_COLOR)
    cf = cv2.imread("coral_fragment.png", cv2.IMREAD_COLOR)
    star = cv2.imread("star.png", cv2.IMREAD_COLOR)
    sponge = cv2.imread("sponge.png", cv2.IMREAD_COLOR)
    empty = cv2.imread("empty.png", cv2.IMREAD_COLOR)
    row = [coral, cf, star, sponge, empty]

    shapes = identify_shapes(row)
