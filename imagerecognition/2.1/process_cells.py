import numpy as np
from imutils import contours
import cv2

# Hi! This script will
# --- Process an image to find a grid
# --- Explore each of the cells found in the grid


def main():
    process_img('images/section.png')


def process_img(filename):
    # === declare image, specify area of interest ==
    img = cv2.imread(filename)
    # height, width, _ = img.shape

    # xbnd = width//4
    # ybnd = height//6

    # img = img[3*ybnd:5*ybnd, xbnd:3*xbnd]
    cv2.imshow('img', img)

    # === process images and isolate contents of cells ===
    grid = isolate_grid_lines(img)
    grid = fix_lines(grid)
    cnts = isolate_cells(grid)

    process_cells(img, cnts)

    # cv2.imshow('grid', grid)
    # cv2.waitKey(0)
    cv2.destroyAllWindows()


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


# Returns a list of the contents of the boxes in the row
def isolate_cells(img):
    # Find the contours of the image
    invert = 255 - img.copy()
    cnts = cv2.findContours(invert, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_KCOS)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    (cnts, _) = contours.sort_contours(cnts, method="left-to-right")

    # Sort into rows
    filtered_contours = []
    for (i, c) in enumerate(cnts, 1):
        area = cv2.contourArea(c)
        # TODO: Find appropriate bounds for the area to be in
        if area > 8600 and area < 150000:
            filtered_contours.append(c)

    return filtered_contours


# Will run through and process the cells found by isolate_cells
def process_cells(img, cnts):
    # Iterate through each box
    for cnt in cnts:
        mask = np.zeros(img.shape, dtype=np.uint8)
        cv2.drawContours(mask, [cnt], -1, (255, 255, 255), -1)
        result = cv2.bitwise_and(img, mask)
        result[mask == 0] = 255

        # TODO: Run through shape recognition software for each box
        # TODO: Tell graphing software what is in each box

        cv2.imshow('result', result)
        cv2.waitKey(0)


if __name__ == "__main__":
    main()
