#include <cv.h>
#include <highgui.h>
#include <fstream>
#include "opencv2/core/core.hpp"
#include "opencv2/features2d/features2d.hpp"
#include "opencv2/highgui/highgui.hpp"
#include "opencv2/calib3d/calib3d.hpp"
#include "opencv2/nonfree/nonfree.hpp"

using namespace cv;
using namespace std;

VideoCapture capture;
char* videoName;


int main( int argc, char** argv )
{
	videoName = argv[1];
	capture.open(videoName);
	if( argc != 2 || !capture.isOpened() ) {
		printf( "No video data\n");
		return -1;
	}
	int roiX=100, roiY=100, roiW=190, roiH=190;
	
	Mat oldFrame;
	Mat newFrame;

	capture >> newFrame;
	while(true)
	{
		oldFrame = newFrame;
		capture >> newFrame;

		if (newFrame.empty())
	        break;

	    if (waitKey(30)=='q')
	    	break;

		//SURF detc = SURF(4000);
		SIFT detc = SIFT();
    	//ORB detc = ORB(50000);
		
		vector<KeyPoint> keyp1;
		vector<KeyPoint> keyp2;
		Mat desc1;
		Mat desc2;
		detc.detect(oldFrame, keyp1);
		detc.detect(newFrame, keyp2);
		detc.compute(oldFrame, keyp1, desc1);
		detc.compute(newFrame, keyp2, desc2);
		BFMatcher bmatcher(2);
	    vector<DMatch> matches;
	    bmatcher.match(desc1, desc2, matches);

		namedWindow("frame2", CV_WINDOW_AUTOSIZE);
	    int idx1;
	    int idx2;

	    for(vector<DMatch>::iterator it=matches.begin(); it != matches.end(); ++it)
	    {
	        idx1 = it->queryIdx;
	        idx2 = it->trainIdx;
	        circle(oldFrame, Point(keyp1[idx1].pt.x, keyp1[idx1].pt.y), 2, Scalar(255,255,255),3, 8,0);
	        circle(newFrame, Point(keyp2[idx2].pt.x, keyp2[idx2].pt.y), 2, Scalar(255,255,255),3, 8,0);
	    }
		imshow("frame2", newFrame);
		//waitKey(0);
	}    
}