"""Identifies shapes in a given cell of data

- Take in a cell
- Use CV to identify what kind of shape the image is
  - shapes are either polygons or objects which reach 2 cells
- Return a list of shape identifies (up to you to decide what identifies to use)

"""

import cv2
import pickle
import imutils

def identify_shapes(row):
    """Identifies the shapes in the row

        Args:
            row: list of images to be analyzed

        Returns:
            A list of strings representing the
            objects located in each cell.
    """

    names = []

    i = 0
    for img in row:
        shape = process_img(img)
        names.append(shape)
        i = i + 1

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    print(names)
    return names

def process_img(img):
    grayscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # get centermost pixel grayscale color
    (h, w) = grayscale.shape[:2]
    height = int(h/2)
    width = int(w/2)
    color = grayscale[height, width]

    # convert image to binary (black background, white shape)
    thresh = 185 #might be worth changing in the future, since this won't always be the background color
    _, binary = cv2.threshold(grayscale, thresh, 255, cv2.THRESH_BINARY)
    if color < thresh - 15:
        thresh = color + 15
        _, binary = cv2.threshold(grayscale, thresh, 255, cv2.THRESH_BINARY_INV)
    else:
        if color < thresh + 15 and color > thresh - 15:
            thresh = 255
        else:
            thresh = color - 15
        _, binary = cv2.threshold(grayscale, thresh, 255, cv2.THRESH_BINARY)

    # get contours of binary image
    cnts = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    # name the shape
    shape = "empty"
    for c in cnts:
        shape = shape_detector(c);
    return shape

def shape_detector(cnts):
    shape = "unidentified"
    peri = cv2.arcLength(cnts, True)
    approx = cv2.approxPolyDP(cnts, 0.04 * peri, True)

    if len(approx) == 10:
        shape = "star"
    elif len(approx) == 4:
        shape = "square"
    else:
        shape = "idk fam"

    return shape

if __name__ == '__main__':
    # Test driver
    row = []
    with open('list.pkl', 'rb') as f:
        row = pickle.load(f)

    identify_shapes(row)
