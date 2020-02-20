import cv2
import numpy as np


def main():
    filter = True

    cam = cv2.VideoCapture(1)

    while(True):
        ret, img = cam.read()

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

            if filter:
                for i in range(len(lines)):
                    if line_flags[i]:
                        filtered_lines.append(lines[i])

                print('Number of filtered lines:', len(filtered_lines))
            else:
                filtered_lines = lines

            for line in filtered_lines:
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

        cv2.imshow('hough.jpg', img)
        if cv2.waitKey(27) == 1:
            break

    cv2.destroyAllWindows()
    cam.release()


if __name__ == '__main__':
    main()
