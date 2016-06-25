import cv2
import numpy

cap = cv2.VideoCapture(0)

cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH,640)
cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT,480)

extractedColorMat = numpy.zeros((50,50,3),numpy.uint8)
extractedColorMat[:] = [64,164,67]

def nothing(x):
    pass

lowerRangeThreshold = [10,10,10]
upperRangeThreshold = [0,0,0]
upperTolerance = 5
lowerTolerance = 5

cv2.namedWindow('Control Window',flags=cv2.cv.CV_WINDOW_NORMAL)
cv2.resizeWindow('Control Window',480,240)
cv2.moveWindow('Control Window',0,0)
cv2.namedWindow('Camera Feed',flags=cv2.cv.CV_WINDOW_NORMAL)
cv2.resizeWindow('Camera Feed',330,240)
cv2.moveWindow('Camera Feed',481,0)
cv2.namedWindow('THRESHOLD',flags=cv2.cv.CV_WINDOW_NORMAL)
cv2.moveWindow('THRESHOLD',0,280)
cv2.createTrackbar('lowerTolerance','Control Window',10,100,nothing)
cv2.createTrackbar('upperTolerance','Control Window',10,100,nothing)

def clickEvent(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print "Coordinates :",x,y
        color = image[(y,x)]
        print "clicked "+str(color)
        extractedColorMat[:]=[color[0],color[1],color[2]]
while 1:
    lowerTolerance = cv2.getTrackbarPos('lowerTolerance','Control Window')
    upperTolerance = cv2.getTrackbarPos('upperTolerance','Control Window')
    ret, image = cap.read()
    cv2.imshow('Control Window',extractedColorMat)
    HSV_MAT = cv2.cvtColor(extractedColorMat,cv2.COLOR_BGR2HSV)
    HSV_COLOR = HSV_MAT[(8,8)]
    hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    lowerRangeThreshold = [HSV_COLOR[0]-lowerTolerance,HSV_COLOR[1]-lowerTolerance,HSV_COLOR[2]-lowerTolerance]
    upperRangeThreshold = [HSV_COLOR[0]+upperTolerance,HSV_COLOR[1]+upperTolerance,HSV_COLOR[2]+upperTolerance]
    #dilation = cv2.dilate(erosion,kernel,iterations = 5)
    #print "VALUES : ",lowerRangeThreshold[0],lowerRangeThreshold[1],lowerRangeThreshold[2],upperRangeThreshold[0],upperRangeThreshold[1],upperRangeThreshold[2]
    threshold = cv2.inRange(hsv,numpy.array([lowerRangeThreshold[0],lowerRangeThreshold[1],lowerRangeThreshold[2]]),numpy.array([upperRangeThreshold[0],upperRangeThreshold[1],upperRangeThreshold[2]]))
    #kernel = numpy.ones((5,5),numpy.uint8)
    #erosion = cv2.erode(threshold,kernel,iterations = 3)
    cv2.imshow('THRESHOLD',threshold)
    cv2.setMouseCallback('Camera Feed',clickEvent)
    #a,b,c,d = cv2.boundingRect(erosion)
    #print a,b,c,d
    #cv2.rectangle(image,(a,b),(a+c,b+d),(0,0,255),1)
    cv2.imshow('Camera Feed',image)
    if(cv2.waitKey(1)==32):break
cap.release()
cv2.destroyAllWindows()
