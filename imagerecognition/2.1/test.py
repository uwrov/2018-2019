
import numpy as np
import cv2
import imutils

BLACK = ([40, 35, 40], [145, 133, 128])
RED = ([0, 10, 100], [120, 100, 230])
YELLOW = ([0, 150, 180], [25, 180, 210])
WHITE = 195

def get_shapes(imgs):
    shapes = []
    name = " 1"
    for img in imgs:
        area = []

        black = change_color(img, BLACK)
        black_cnts = get_contours(black, "black" + name)
        area.append(get_area(black))

        red = change_color(img, RED)
        red_cnts = get_contours(red, "red" + name)
        area.append(get_area(red))

        yellow = change_color(img, YELLOW)
        yellow_cnts = get_contours(yellow, "yellow" + name)
        if len(yellow_cnts) == 0:
            yellow_cnts = [0,0,0,0,0,0,0,0,0,0]
        area.append(get_area(yellow))

        white = change_white(img)
        white_cnts = get_contours(white, "white" + name)
        area.append(get_area(white))

        contours = [black_cnts, red_cnts, yellow_cnts, white_cnts]
        color = get_color(contours)
        shapes.append(get_shape(area[color], color))
        name = name + "1"
    print(shapes)

def change_white(img):
    grayscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(grayscale, WHITE, 255, cv2.THRESH_BINARY)

    blur = cv2.bilateralFilter(binary,9,75,75)
    return blur

def change_color(img, color):
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

def get_contours(img, i):
    cnts = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    #cv2.drawContours(img, cnts, 2, (179,178,176), 3)
    #cv2.imshow("contours " + i, img)

    contours = []
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)
        #print(len(approx))
        contours.append(len(approx))

    return contours

def get_color(cnts):
    cntlengths = []
    for cnt in cnts:
        cntlengths.append(len(cnt))
    return cntlengths.index(min(cntlengths))

def get_area(img):
    area = cv2.countNonZero(img)
    return area

def get_shape(area, color):
    if area > 100:
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
    coral = cv2.imread("coral.png", cv2.IMREAD_COLOR)
    cf = cv2.imread("coral_fragment.png", cv2.IMREAD_COLOR)
    star = cv2.imread("star.png", cv2.IMREAD_COLOR)
    sponge = cv2.imread("sponge.png", cv2.IMREAD_COLOR)
    empty = cv2.imread("empty.png", cv2.IMREAD_COLOR)
    images = [coral, cf, star, sponge, empty]
    #images = [coral]
    get_shapes(images)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
