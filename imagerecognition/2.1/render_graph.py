"""Create visualization of coral reef

Take in a list of lists of shape identifiers
Produce a 9x3 grid which visualizes the graph
"""

import numpy as np
import cv2
from identify_shapes import identify_shapes

ROWS = 3
COLS = 9
SCALE = 70

def side_of_pool():
    pool_side = np.zeros((100, 300, 3), np.uint8)
    pool_side.fill(255)
    font = cv2.FONT_HERSHEY_SIMPLEX
    text = "Side of pool"
    textsize = cv2.getTextSize(text, font, 1, 2)[0]
    textX = int((pool_side.shape[1] - textsize[0]) / 2)
    textY = int((pool_side.shape[0] + textsize[1]) / 2)
    cv2.putText(pool_side, text, (textX, textY), font, 1, (0,0,0), 2, cv2.LINE_AA)
    rotation_matrix = cv2.getRotationMatrix2D((pool_side.shape[1]/2, pool_side.shape[0] * 3/2), 90, 1)
    pool = cv2.warpAffine(pool_side, rotation_matrix, (pool_side.shape[0], pool_side.shape[1]),
                             flags=cv2.INTER_LINEAR,
                             borderMode=cv2.BORDER_TRANSPARENT)
    return pool[2:, :-1]

def make_grid():
    width = ROWS * SCALE
    length = COLS * SCALE
    grid = np.zeros((width, length, 3), np.uint8)
    grid.fill(255)

    x = np.linspace(start=0, stop=width, num=width)
    y = np.linspace(start=0, stop=length, num=length)

    vert_lines = []
    for i in range(COLS):
        coord = [int(y[i*SCALE]), 0, int(y[i*SCALE]), width-1]
        vert_lines.append(coord)
        [x1, y1, x2, y2] = vert_lines[i]
        cv2.line(grid, (x1,y1), (x2,y2), (0,0,0), 1)
    cv2.line(grid, (length-1,0), (length-1,width-1), (0,0,0), 1)

    horiz_lines = []
    for i in range(ROWS):
        coord = [0, int(x[i*SCALE]), length-1, int(x[i*SCALE])]
        horiz_lines.append(coord)
        [x1, y1, x2, y2] = horiz_lines[i]
        cv2.line(grid, (x1,y1), (x2,y2), (0,0,0), 1)
    cv2.line(grid, (0,width-1), (length-1,width-1), (0,0,0), 1)

    return grid

def map_shapes(grid):
    for x_coord in range(COLS):
        row = gridNames[x_coord]
        shape = identify_shapes(row)
        for y_coord in range(ROWS):
            x = SCALE * x_coord + int(SCALE/4)
            y = SCALE * y_coord + int(SCALE/4)
            currShape = shape[y_coord]
            if currShape != "empty":
                cv2.putText(grid, currShape, (x,y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 1, cv2.LINE_AA)
    return grid

def attach_imgs(imgs):
    h_min = min(img.shape[0] for img in imgs)
    imgs_resize = [cv2.resize(img, (int(img.shape[1] * h_min / img.shape[0]), h_min), cv2.INTER_CUBIC) for img in imgs]
    return cv2.hconcat(imgs_resize)

if __name__ == '__main__':
    coral = cv2.imread("coral.png", cv2.IMREAD_COLOR)
    cf = cv2.imread("coral_fragment.png", cv2.IMREAD_COLOR)
    star = cv2.imread("star.png", cv2.IMREAD_COLOR)
    sponge = cv2.imread("sponge.png", cv2.IMREAD_COLOR)
    empty = cv2.imread("empty.png", cv2.IMREAD_COLOR)

    gridNames = [
        [empty, empty, empty],
        [empty, star, empty],
        [empty, empty, cf],
        [empty, empty, empty],
        [empty, empty, star],
        [empty, empty, empty],
        [cf, empty, coral],
        [empty, empty, coral],
        [empty, sponge, empty]
        ]

    pool = side_of_pool()
    grid = make_grid()
    grid = map_shapes(grid)
    final_img = attach_imgs([pool, grid])

    #cv2.imwrite('grid.jpg', final_img)
    cv2.imshow('grid', final_img)

    cv2.waitKey(0)
