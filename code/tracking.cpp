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

	Mat frame1;
	Mat frame2;
	capture >> frame1;
	capture >> frame2;

	SURF surf = SURF(4000);
	vector<KeyPoint> keyp1;
	vector<KeyPoint> keyp2;
	Mat desc1;
	Mat desc2;
	surf.detect(frame1, keyp1);
	surf.detect(frame2, keyp2);
	surf.compute(frame1, keyp1, desc1);
	surf.compute(frame2, keyp2, desc2);
	BFMatcher bmatcher(2);
    vector<DMatch> matches;
    bmatcher.match(desc1, desc2, matches);

   	namedWindow("frame1", CV_WINDOW_AUTOSIZE);
	namedWindow("frame2", CV_WINDOW_AUTOSIZE);
    int idx1;
    int idx2;

    for(vector<DMatch>::iterator it=matches.begin(); it != matches.end(); ++it)
    {
        idx1 = it->queryIdx;
        idx2 = it->trainIdx;
        circle(frame1, Point(keyp1[idx1].pt.x, keyp1[idx1].pt.y), 2, Scalar(255,255,255),3, 8,0);
        circle(frame2, Point(keyp2[idx2].pt.x, keyp2[idx2].pt.y), 2, Scalar(255,255,255),3, 8,0);
    }
    imshow("frame1", frame1);
	imshow("frame2", frame2);

	waitKey(0);    
}