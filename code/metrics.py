import numpy as np
import sys
import math
from numpy import genfromtxt
import matplotlib.path as mplPath

videoname = sys.argv[1]
objectRadius = 20
objectArea = math.pi*objectRadius*objectRadius


def polyArea2D(pts):
    lines = np.hstack([pts,np.roll(pts,-1,axis=0)])
    area = 0.5*abs(sum(x1*y2-x2*y1 for x1,y1,x2,y2 in lines))
    return area

mark = genfromtxt(videoname+'.txt', delimiter=' ')
mean = genfromtxt(videoname+'.mean', delimiter=',')
cams = genfromtxt(videoname+'.cams', delimiter=',')
klt = [line.rstrip('\n') for line in open(videoname+'.klt')]

scores = [0,0,0]
hits = [0,0,0]

for x in range(0,mark.shape[0]-1):
	point = (mark[x][0], mark[x][1])
	meanPoly = None
	meanScore = 0.0
	if mean.shape[0]-1 >= x:
		meanPoly = ((mean[x][0],mean[x][1]),(mean[x][2],mean[x][3]),(mean[x][4],mean[x][5]),(mean[x][6],mean[x][7]))
	if meanPoly and mplPath.Path(meanPoly).contains_point(point):
		meanScore = objectArea / polyArea2D(meanPoly)
		hits[0] += 1
	
	camsPoly = None
	camsScore = 0.0
	if cams.shape[0]-1 >= x:
		camsPoly = ((cams[x][0],cams[x][1]),(cams[x][2],cams[x][3]),(cams[x][4],cams[x][5]),(cams[x][6],cams[x][7]))
	if camsPoly and mplPath.Path(camsPoly).contains_point(point):
		camsScore = objectArea / polyArea2D(camsPoly)
		hits[1] += 1
	
	kltPoly = None
	kltScore = 0.0
	if len(klt)-1 >= x:
		coords = [int(n) for n in klt[x][:-1].split(',')]
		kltPoly = zip(*[coords[i::2] for i in range(2)])
	if kltPoly and mplPath.Path(kltPoly).contains_point(point):
		kltScore = objectArea / polyArea2D(kltPoly)
		hits[2] += 1

	scores[0] = scores[0] + meanScore/mark.shape[0]
	scores[1] = scores[1] + camsScore/mark.shape[0]
	scores[2] = scores[2] + kltScore/mark.shape[0]
	
print (scores)
print (hits)