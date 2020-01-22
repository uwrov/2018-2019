import cv2

def main():
    cap = cv2.VideoCapture('http://10.0.0.27:8080/video/mjpeg')

    while True:
        _, frame = cap.read()
        cv2.imshow('feed', frame)
        if cv2.waitKey(1) == 27:
            break

    cv2.destroyAllWindows()

    cap.release()

if __name__ == '__main__':
    main()