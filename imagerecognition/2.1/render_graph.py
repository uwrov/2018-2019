"""Create visualization of coral reef

Take in a list of lists of shape identifiers
Produce a 9x3 grid which visualizes the graph
"""

import numpy as np
import cv2
import sys
from identify_shapes import identify_shapes

coral = cv2.imread("coral.png", cv2.IMREAD_COLOR)
cf = cv2.imread("coral_fragment.png", cv2.IMREAD_COLOR)
star = cv2.imread("star.png", cv2.IMREAD_COLOR)
sponge = cv2.imread("sponge.png", cv2.IMREAD_COLOR)
empty = cv2.imread("empty.png", cv2.IMREAD_COLOR)

grid = [
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

for row in grid:
    shapes = identify_shapes(row)
    #print(shapes)

rows = 3
cols = 9
scale = 70

width = rows * scale
length = cols * scale
grid = np.zeros((width, length, 3), np.uint8)
grid.fill(255)

x = np.linspace(start=0, stop=width, num=width)
y = np.linspace(start=0, stop=length, num=length)

vert_lines = []
for i in range(cols):
    coord = [int(y[i*scale]), 0, int(y[i*scale]), width-1]
    vert_lines.append(coord)
    [x1, y1, x2, y2] = vert_lines[i]
    cv2.line(grid, (x1,y1), (x2,y2), (0,0,0), 1)
cv2.line(grid, (length-1,0), (length-1,width-1), (0,0,0), 1)

horiz_lines = []
for i in range(rows):
    coord = [0, int(x[i*scale]), length-1, int(x[i*scale])]
    horiz_lines.append(coord)
    [x1, y1, x2, y2] = horiz_lines[i]
    cv2.line(grid, (x1,y1), (x2,y2), (0,0,0), 1)
cv2.line(grid, (0,width-1), (length-1,width-1), (0,0,0), 1)

cv2.imshow('grid', grid)
cv2.waitKey(0)
