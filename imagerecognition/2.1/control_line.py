import cv2
import numpy as np

def main():
    # Grab video feed from source
    cap = cv2.VideoCapture("http://10.19.197.178:8080/video/mjpeg")
    while True:
        _, frame = cap.read()
        cv2.imshow('feed', frame)

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
        mask = cv2.GaussianBlur(mask, (5, 5), 0)

        #if camera cannot detect line
        #print left or right

        #if line.x is not width/3


        bluecnts = cv2.findContours(mask.copy(),
                            cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)[-2]
        if len(bluecnts) > 0:
            blue_area = max(bluecnts, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(blue_area)
            cv2.line(frame, (x, y+h//2), (x+w, y+h//2), (0,255,0), 2)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)

        if bluecnts is not (width/3):
            print("wrong")


if __name__ == '__main__':
    main()
