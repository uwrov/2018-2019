import numpy as np
from imutils import contours
import cv2
from constants import CntSizeTol as size_tols

# Hi! This script will
# --- Process an image to find a grid
# --- Explore each of the cells found in the grid


def main():
    img = cv2.imread('images/section_obj.png')
    process_row(img)


# Takes in a row, returns a list of cells in the row
# cells[0] is leftmost cell, cells[2] is rightmost cell
def process_row(img):
    # === process images and isolate contents of cells ===
    grid = isolate_grid_lines(img)
    grid = fix_lines(grid)
    cells = identify_cells(img, grid)

    draw_cells(img, cells)

    # cv2.imshow('grid', grid)
    # cv2.waitKey(0)
    cv2.destroyAllWindows()

    return cells


# Returns dict full of color bounds
def _get_bounds():
    return {
        'pink': [np.array([130, 25, 160]), np.array([170, 255, 255])],
        'blue': [np.array([100, 150, 0]), np.array([140, 255, 255])],
        'yell': [np.array([20, 100, 100]), np.array([30, 255, 255])]
    }


# Returns color-masked image, with colors defined in get_bounds
def isolate_grid_lines(img):
    # convert rgb image to hsv for color isolation
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    bounds = _get_bounds()

    masks = {}
    for c in bounds:
        lower = bounds[c][0]
        upper = bounds[c][1]
        masks[c] = _make_mask(lower, upper, hsv)

    return sum(masks.values())


# Helper method which creates color masks of an hsv encoded image
def _make_mask(lower, upper, hsv):
    mask = cv2.inRange(hsv, lower, upper)

    return cv2.GaussianBlur(mask, (3, 3), 0)


# Repairs gaps in grid lines,
# not perfect but increases tolerance of box recognition
def fix_lines(img):
    # Fixes horizontal and vertical lines
    # TODO: Find appropriate iteration amount which isn't magic
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 5))
    thresh = cv2.morphologyEx(img, cv2.MORPH_CLOSE,
                              vertical_kernel, iterations=6)
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 1))
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE,
                              horizontal_kernel, iterations=4)

    return thresh


# Returns a list of contours of the cells in the row
def identify_cells(img, grid):
    # Find the contours of the image
    invert = 255 - grid.copy()
    cnts = cv2.findContours(invert, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_KCOS)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    (cnts, _) = contours.sort_contours(cnts, method="left-to-right")

    # split row into cells
    cells = []
    tols = (size_tols.LOWER_BOUND.value, size_tols.UPPER_BOUND.value)

    for c in cnts:
        area = cv2.contourArea(c)

        if area > tols[0] and area < tols[1]:
            rect = cv2.boundingRect(c)
            x, y, w, h = rect

            cells.append(img[y:y+h, x:x+w])

    return cells


# draws the found cells
def draw_cells(img, cnts):
    # Iterate through each box
    for cell in cnts:
        cv2.imshow('cell', cell)
        cv2.waitKey(0)


if __name__ == "__main__":
    main()
