import numpy as np
import cv2
import sys

videoname = sys.argv[1]

cap = cv2.VideoCapture(videoname)

r,h,c,w = int(sys.argv[2]), int(sys.argv[4]), int(sys.argv[3]), int(sys.argv[5])

f = open(videoname+'.klt','w')

# params for ShiTomasi corner detection
feature_params = dict( maxCorners = 100,
                       qualityLevel = 0.3,
                       minDistance = 2,
                       blockSize = 4 )

# Parameters for lucas kanade optical flow
lk_params = dict( winSize  = (30,30),
                  maxLevel = 2,
                  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

# Create some random colors
color = np.random.randint(0,255,(100,3))

# Take first frame and find corners in it
ret, old_frame = cap.read()
# region of interest
roi = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
roi[:] = 0
cv2.rectangle(roi, (r,c), (r+w,c+h), (255,255,255), -1)

old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
p0 = cv2.goodFeaturesToTrack(old_gray, mask = roi, **feature_params)

# Create a mask image for drawing purposes
mask = np.zeros_like(old_frame)

while(1):
    ret,frame = cap.read()
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # calculate optical flow
    p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)

    # Select good points
    good_new = p1[st==1]
    good_old = p0[st==1]

    # draw the tracks
    #for i,(new,old) in enumerate(zip(good_new,good_old)):
        #a,b = new.ravel()
        #c,d = old.ravel()
        #cv2.line(mask, (a,b),(c,d), color[i].tolist(), 2)
        #cv2.circle(frame,(a,b),5,color[i].tolist(),-1)

    hull = cv2.convexHull(good_new)
    
    if (hull != None):
        cv2.fillConvexPoly(frame, np.int32(hull),(0,255,0),8,0)

    for x in np.int32(hull):
        f.write(str(x[0][0])+','+str(x[0][1])+',')
    f.write('\n')

    img = cv2.add(frame,mask)

    cv2.imshow('frame',img)
    if cv2.waitKey(33) == ord('q'):
        break

    # Now update the previous frame and previous points
    old_gray = frame_gray.copy()
    p0 = good_new.reshape(-1,1,2)

cv2.destroyAllWindows()
cap.release()
f.close()
