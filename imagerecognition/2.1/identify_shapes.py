"""Identifies shapes in a given cell of data

- Take in a cell
- Use CV to identify what kind of shape the image is
  - shapes are either polygons or objects which reach 2 cells
- Return a list of shape identifies (up to you to decide what identifies to use)

"""

import cv2
import pickle

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
        #cv2.imshow(str(i), img)
        process_img(img, str(i))
        i = i + 1

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    shape = "empty"
    pass

def process_img(img, name):
    grayscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imshow(name, grayscale)
   # threshold = cv2.threshold(grayscale, 127, 255, cv2.THRESH_BINARY)
   # cnts = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
   # cnts = imutils.grab_contours(cnts)
    _, binary = cv2.threshold(grayscale, 127, 255, cv2.THRESH_BINARY)
    thresh = cv2.adaptiveThreshold(grayscale, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    cv2.imshow(name + "2", thresh)

    thresh2 = cv2.threshold(thresh, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    #cv2.imshow(name + "3", thresh2)


if __name__ == '__main__':
    # Test driver
    row = []
    with open('list.pkl', 'rb') as f:
        row = pickle.load(f)

    identify_shapes(row)