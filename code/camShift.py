import numpy as np
import cv2
import math


cap = cv2.VideoCapture('../videos/original/f01.mp4')
#cap = cv2.VideoCapture('../videos/original/f05.mp4')

# take first frame of the video
ret,frame = cap.read()

# setup initial location of window
#r,h,c,w = 350,190,300,190  # funciona no video 5
r,h,c,w = 100,190,100,190  # funciona no video 1
track_window = (c,r,w,h)

# set up the ROI for tracking
roi = frame[r:r+h, c:c+w]
hsv_roi =  cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv_roi, np.array((0., 60.,32.)), np.array((180.,255.,255.)))
roi_hist = cv2.calcHist([hsv_roi],[0],mask,[180],[0,180])
cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)

# Setup the termination criteria, either 10 iteration or move by atleast 1 pt
term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )

while(1):
  ret ,frame = cap.read()
  if ret == True:
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    dst = cv2.calcBackProject([hsv],[0],roi_hist,[0,180],1)
    # apply meanshift to get the new location

    ret, track_window = cv2.CamShift(dst, track_window, term_crit)
    # Draw it on image
    center=ret[0]
    size=ret[1]
    angle=ret[2]*math.pi/180
    point1=((-size[0]/2*math.cos(angle)-size[1]/2*math.sin(angle))+center[0] , (-size[0]/2*math.sin(angle)+size[1]/2*math.cos(angle))+center[1])
    point2=((size[0]/2*math.cos(angle)-size[1]/2*math.sin(angle))+center[0] , (size[0]/2*math.sin(angle)+size[1]/2*math.cos(angle))+center[1])
    point3=((size[0]/2*math.cos(angle)+size[1]/2*math.sin(angle))+center[0] , (size[0]/2*math.sin(angle)-size[1]/2*math.cos(angle))+center[1])
    point4=((-size[0]/2*math.cos(angle)+size[1]/2*math.sin(angle))+center[0] , (-size[0]/2*math.sin(angle)-size[1]/2*math.cos(angle))+center[1])
    pts = (point1, point2, point3, point4)
    pts = np.int32(pts)
        
    cv2.polylines(frame,[pts],1, (255,255,255))

    cv2.imshow("teste",frame)
    
    if (cv2.waitKey(30)=='q'):
      break
  else:
    break
cv2.destroyAllWindows()
cap.release()