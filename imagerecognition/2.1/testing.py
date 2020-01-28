import cv2
import numpy as np
import math

def main():
    cap = cv2.VideoCapture('http://10.19.182.26:8080/video/mjpeg')
    height, width, _ = cap.read()[1].shape

    while True:
        _, frame = cap.read()

        # convert rgb image to hsv for color isolation
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Set bounds for what shades of blue we want
        lower_blue = np.array([100, 150, 0])
        upper_blue = np.array([140, 255, 255])

        # Isolate blue, draw lines on edges
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        mask = cv2.GaussianBlur(mask, (5,5), 0)

        # ~~~~~~~~~~~~~~~~~~~~~~~ Rectangle Approach ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # bluecnts = cv2.findContours(mask.copy(),
        #                     cv2.RETR_EXTERNAL,
        #                     cv2.CHAIN_APPROX_SIMPLE)[-2]
        # if len(bluecnts) > 0:
        #     blue_area = max(bluecnts, key=cv2.contourArea)
        #     x, y, w, h = cv2.boundingRect(blue_area)
        #     cv2.line(frame, (x, y+h//2), (x+w, y+h//2), (0,255,0), 2)
        #     cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)


        # ~~~~~~~~~~~~~~~~~~~~~~~` Lines approach ~~~~~~~~~~~~~~~~~~~~~~~`
        edges = cv2.Canny(mask, 75, 150)
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, 50, maxLineGap=50)
        llines = []
        # TODO: isolate longest line, hopefully it's a good representation of the blue line we care about. 
        # 
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)
                lineDistance = np.sqrt((x2 - x1)^2 + (y2 - y1)^2)
                # print(lineDistance) 
                llines.append(lineDistance)
            # find index of longest line and draws the longest line in array    
            i_max = llines.index(max(llines))
            x1, y1, x2, y2 = lines[i_max][0]
            cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 255), 5)
        cv2.line(frame, (0, height//2), (width, height//2),(0,0,255),5)

        cv2.imshow('feed', frame)
        cv2.imshow('mask', mask)
        


        if cv2.waitKey(1) == 27:
            break


    cv2.destroyAllWindows()

    cap.release()

if __name__ == '__main__':
    main()