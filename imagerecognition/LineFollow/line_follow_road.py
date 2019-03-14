import cv2
import numpy as np 

video = cv2.VideoCapture("./img/road_car_view.mp4")

while True:
    ret, frame = video.read()                       #   Read each frame of the video
    # If the video has finished, restart it!
    if not ret:
        video = cv2.VideoCapture("./img/road_car_view.mp4")
        continue

    # Add a Gaussian mask to make things less sensitive
    frame = cv2.GaussianBlur(frame, (5, 5), 0)

    # This program tracks a yellow line in a video, but because we can't
    # expect it to be the same color, we must have a range we consider to be 'yellow'
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)    #   Prepare for processing
    low_yellow = np.array([18, 94, 140])
    high_yellow = np.array([48, 255, 255])
    mask = cv2.inRange(hsv, low_yellow, high_yellow)
    edges = cv2.Canny(mask, 75, 150)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 50, maxLineGap=50)
    
    # If we don't have any lines (if there's not any yellow edges in the frame),
    # there will be an error, so check before
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.arrowedLine(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)

    cv2.imshow("Mask", mask)
    cv2.imshow("Frame", frame)

    key = cv2.waitKey(25)           #   Wait 25 ms for each frame

    if key == 27:
        break

video.release()
cv2.destroyAllWindows()