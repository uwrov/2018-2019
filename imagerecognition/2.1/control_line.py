import cv2
import numpy as np

def main():
    # Grab video feed from source
    cap = cv2.VideoCapture("http://10.18.223.105:8080/video/mjpeg")

    height, width, _ = cap.read()[1].shape

    while True:
        _, frame = cap.read()
        


        # convert rgb image to hsv for color isolation
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Set bounds for what shades of blue we want
        lower_blue = np.array([100, 130, 0])
        upper_blue = np.array([140, 255, 255])

        # Isolate blue, draw lines on edges
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        mask = cv2.GaussianBlur(mask, (5, 5), 0)
        right = mask[height // 2 : height , width // 2 : width]
        rightFrame = frame[height // 2 : height , width // 2 : width]
        left = mask[height // 2 : height,  0 : width // 2]
        leftFrame = frame[height // 2 : height,  0 : width // 2]
        # cv2.imshow('mask', mask)

        right2 = rect_on_blue(right, rightFrame)
        left2 = rect_on_blue(left, leftFrame)

        cv2.imshow('r', right2)
        cv2.imshow('l', left2)
        
        if cv2.waitKey(27) == 1:
            break

        
def rect_on_blue(mask, img):        
        bluecnts = cv2.findContours(mask.copy(),
                            cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)[-2]
        for cnt in bluecnts:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.line(img, (x, y+h//2), (x+w, y+h//2), (0,0,255), 2)
            cv2.drawContours(img, bluecnts, -1, 255, 3)
            blue_area = max(bluecnts, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(blue_area)
            cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 2)
        
        return img
            

        
        # if len(bluecnts) > 0:
        #     blue_area = max(bluecnts, key=cv2.contourArea)
        #     x, y, w, h = cv2.boundingRect(blue_area)
        #     cv2.line(frame, (x, y+h//2), (x+w, y+h//2), (0,255,0), 2)
        #     cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)
        

                



if __name__ == '__main__':
    main()
