import cv2
import numpy
import math
from enum import Enum
from statistics import mean

def count_shapes(image):
    border = 50
	#process_contours = GripPipeline()
	#img = cv2.imread(sample_image, cv2.IMREAD_GRAYSCALE)
	#var finished_bi_img = process_contours.process(img)
    threshold = cv2.threshold(image, 100, 255, cv2.THRESH_BINARY)[1]
    contours, __ = cv2.findContours(threshold, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    height, width = image.shape
    print(height,width)
    #contours = filter_contours(contours)
    
   
    ##Not sure if a single line would be regonized as a countor 
    #with two sides or one, therefore leaving the first dictionary just in case.
    shapes = {
        1 : 0,
        2 : 0,
        3 : 0,
        4 : 0,
        5 : 0
    };
    
    box = [numpy.array([[2*border,border],[width - border * 2, border],[width - border * 2,height - border],[2*border,height - border]])]
    for b in box:
        cv2.drawContours(img, [b],0,(255,0,255),2)[0]
    
    prev = []
    
    for cnt in contours:
        x,y,w,h = cv2.boundingRect(cnt)
        midx = x + w / 2
        midy = y + h / 2
        if(x < border * 2 or x > (width - border * 2)):
            pass
        elif(y < border or y > (height - border)):
            pass
        elif(round(w/h,1)-1 <= 0.4 and len(prev)!=0):
            avg = mean(prev)
            
            if(w/avg < 2 or h/avg < 2):
                approx = cv2.approxPolyDP(cnt, 0.03*cv2.arcLength(cnt, True), True)
                cv2.drawContours(img, [approx],0,(255,0,255),2)
                if len(approx) > 4:
                    shapes[5] += 1
                else:
                    shapes[len(approx)] += 1
            else:
                pass
        else:
            print(x,y,w,h)
            print(round(w/h,1))
            prev.append(w)
            prev.append(h)
            approx = cv2.approxPolyDP(cnt, 0.03*cv2.arcLength(cnt, True), True)
            cv2.drawContours(img, [approx],0,(255,0,255),2)
            if len(approx) > 4:
                shapes[5] += 1
            else:
                shapes[len(approx)] += 1
    print(shapes)
    cv2.imshow("image", img)
    cv2.imshow("threshold", threshold)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return(shapes)

'''def filter_contours(input, min_area, min_primeter, min_width, max_width, min_height, max_hight, max_vertex, min_vertex, min_ratio, max_ratio):
    output = []
    for cnt in input:
        x,y,w,h = cv2. boundingRect(cnt)
    if(w < min_width or w > max_width):
        continue
    if(h < min_height or h > max_hight):
        continue
    area = cv2.contourArea(cnt)
    if(area < min_area):
        continue
    if(cv2.arcLength(cnt, True) < min_primeter):
        continue
    if(len(contour) < min_vertex):
        continue'''
        
    

def capture_image(address = "http://192.168.8.102:8081/?action=stream"):
	cap = cv2.VideoCapture(address)
	ret, frame = cap.read()
	return frame
    
def downsize_n_blur(image, radius = 2):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    ksize = int(6*round(radius)+1)
    image = cv2.GaussianBlur(image, (ksize, ksize), round(radius))

    height, width = image.shape
    image = cv2.resize(image, ((int)(width/2), (int)(height/2)), interpolation = cv2.INTER_CUBIC)
    return image
    
def show_img(image):
    cv2.imshow("image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    

img = capture_image()
img = downsize_n_blur(img)
count_shapes(img)
