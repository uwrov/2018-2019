import cv2
import numpy as np


# Hello, currently this script will :
# -- Isolate and draw Pink Lines
# -- Identify what kind of lines a pink line is (vertical vs horizontal)
# -- Define what we want the increment barrier to be

def main():
    process_vid()
    process_img('poopie.png')


def process_vid(src='poopie.png'):
    cam = cv2.VideoCapture(src)

    while(True):
        ret, img = cam.read()

        grid_lines = find_grid(img)
        identify(grid_lines, 0.1)

        cv2.imshow('frame', img)

        if cv2.waitKey(27) == 1:
            break

    # === Free resources ===
    cam.release()
    cv2.destroyAllWindows()


def process_img(filename):
    img = cv2.imread(filename)
    grid_lines = find_grid(img)
    identify(grid_lines, 0.1)

    # ------ What line we consider when incrementing -----
    boundary = 500.
    boundary_line = [[boundary, np.pi/2]]
    print("boundary:", boundary_line)

    grid_lines.append(boundary_line)
    draw_lines(grid_lines, img)

    # Display image
    cv2.imshow('hough.jpg', img)

    # === Keep image until we want to get rid of it ===
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def draw_lines(lines, img):
    for line in lines:
        rho, theta = line[0]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1 = int(x0 + 1000*(-b))
        y1 = int(y0 + 1000*(a))
        x2 = int(x0 - 1000*(-b))
        y2 = int(y0 - 1000*(a))

        cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)


# returns a list of the pink mason lines found in the given image/frame
def find_grid(img):
    # convert rgb image to hsv for color isolation
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Set bounds for what shades of pink we want
    lower_pink = np.array([130, 25, 160])
    upper_pink = np.array([170, 255, 255])

    # Isolate blue, draw lines on edges
    mask = cv2.inRange(hsv, lower_pink, upper_pink)
    mask = cv2.GaussianBlur(mask, (5, 5), 0)

    # Isolate lines
    edges = cv2.Canny(mask, 75, 150)
    lines = cv2.HoughLines(edges, 1, np.pi/180, 100)

    if lines is not None:
        rho_threshold = 20
        theta_threshold = 2

        # how many lines are similar to a given one
        similar_lines = {i: [] for i in range(len(lines))}
        for i in range(len(lines)):
            for j in range(len(lines)):
                if i == j:
                    continue

                rho_i, theta_i = lines[i][0]
                rho_j, theta_j = lines[j][0]
                if abs(rho_i - rho_j) < rho_threshold and \
                   abs(theta_i - theta_j) < theta_threshold:
                    similar_lines[i].append(j)

        # ordering the INDECES of the lines by how many are similar to them
        indices = [i for i in range(len(lines))]
        indices.sort(key=lambda x: len(similar_lines[x]))

        # line flags is the base for the filtering
        line_flags = len(lines)*[True]
        for i in range(len(lines) - 1):
            # if we already disregarded the ith element in
            # the ordered list then we don't care
            # (we will not delete anything based on it and
            # we will never reconsider using this line again)
            if not line_flags[indices[i]]:
                continue

            # we are only considering very unique lines
            for j in range(i + 1, len(lines)):
                if not line_flags[indices[j]]:
                    continue

                rho_i, theta_i = lines[indices[i]][0]
                rho_j, theta_j = lines[indices[j]][0]
                if abs(rho_i - rho_j) < rho_threshold and \
                   abs(theta_i - theta_j) < theta_threshold:
                    # if it is similar and has not yet been dropped
                    line_flags[indices[j]] = False

        print('number of Hough lines:', len(lines))

        filtered_lines = []

        for i in range(len(lines)):
            if line_flags[i]:
                filtered_lines.append(lines[i])

        print('Number of filtered lines:', len(filtered_lines))

        return filtered_lines


def identify(lines, tol):
    hor_ct = 0
    ver_ct = 0

    for line in lines:
        # rho = line[0][0]
        the = line[0][1] % (np.pi)
        print(the)

        if abs(the) <= tol or abs(the - np.pi) <= tol:
            print('vertical line: ', line)
            ver_ct += 1
        if abs(np.pi/2 - the) <= tol:
            print('horizontal line: ', line)
            hor_ct += 1

    print('horizontal count', hor_ct)
    print('vertical count', ver_ct)


if __name__ == '__main__':
    main()
