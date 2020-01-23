import cv2
import numpy as np

def main():
    cap = cv2.VideoCapture('http://10.19.218.29:8080/video/mjpeg')

    while True:
        _, frame = cap.read()

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        lower_blue = np.array([100, 150, 0])
        upper_blue = np.array([140, 255, 255])

        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        # res = cv2.bitwise_and(hsv, mask)

        cv2.imshow('feed', frame)
        cv2.imshow('mask', mask)
        # cv2.imshow('res', res)

        if cv2.waitKey(1) == 27:
            break


    cv2.destroyAllWindows()

    cap.release()

if __name__ == '__main__':
    main()