import cv2
import numpy

cap = cv2.VideoCapture(0)

cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH,640)
cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT,480)

point = numpy.zeros((50,50,3),numpy.uint8)
point[:] = [64,164,67]
def nothing(x):
    pass

lower = [10,10,10]
upper = [0,0,0]
threshU = 5
threshL = 5

cv2.namedWindow('Trackbar')
cv2.createTrackbar('threshL','Trackbar',0,100,nothing)
cv2.createTrackbar('threshU','Trackbar',0,100,nothing)

def clickEvent(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print "Coordinates :",x,y
        color = image[(y,x)]
        print "clicked "+str(color)
        point[:]=[color[0],color[1],color[2]]
while 1:
    threshL = cv2.getTrackbarPos('threshL','Trackbar')
    threshU = cv2.getTrackbarPos('threshU','Trackbar')
    ret, image = cap.read()
    cv2.imshow('color',point)
    HSV_MAT = cv2.cvtColor(point,cv2.COLOR_BGR2HSV)
    HSV_COLOR = HSV_MAT[(8,8)]
    hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    lower = [HSV_COLOR[0]-threshL,HSV_COLOR[1]-threshL,HSV_COLOR[2]-threshL]
    upper = [HSV_COLOR[0]+threshU,HSV_COLOR[1]+threshU,HSV_COLOR[2]+threshU]
    #dilation = cv2.dilate(erosion,kernel,iterations = 5)
    #print "VALUES : ",lower[0],lower[1],lower[2],upper[0],upper[1],upper[2]
    threshold = cv2.inRange(hsv,numpy.array([lower[0],lower[1],lower[2]]),numpy.array([upper[0],upper[1],upper[2]]))
    kernel = numpy.ones((5,5),numpy.uint8)
    erosion = cv2.erode(threshold,kernel,iterations = 3)
    cv2.imshow('THRESHOLD',erosion)
    cv2.setMouseCallback('IMAGE',clickEvent)
    #a,b,c,d = cv2.boundingRect(erosion)
    #print a,b,c,d
    #cv2.rectangle(image,(a,b),(a+c,b+d),(0,0,255),1)
    cv2.imshow('IMAGE',image)
    if(cv2.waitKey(1)==32):break
cap.release()
cv2.destroyAllWindows()
