#include <cv.h>
#include <highgui.h>
#include <fstream>

using namespace cv;
using namespace std;

char* videoName;
VideoCapture capture;
int lastX;
int lastY;

int main( int argc, char** argv )
{
	videoName = argv[1];
	
	capture.open(videoName);

	if( argc != 2 || !capture.isOpened() ) {
		printf( "No video data\n");
		return -1;
	}

	string outputFile(videoName);
	outputFile.append(".txt");
	std::ifstream infile(outputFile.c_str());

	Mat frame;
	namedWindow(videoName, CV_WINDOW_AUTOSIZE);
	
	int x, y;

	while(true)
	{
		infile >> x >> y;
	    capture >> frame;
	    if (frame.empty())
	        break;
	    circle(frame, Point(x,y), 21, Scalar(0,0,0),1, 8,0);
	    circle(frame, Point(x,y), 20, Scalar(255,255,255),1, 8,0);
	    circle(frame, Point(x,y), 19, Scalar(0,0,0),1, 8,0);
	    circle(frame, Point(x,y), 2, Scalar(255,255,255),3, 8,0);

	    imshow(videoName, frame);
	    if (waitKey(30)=='q')
	    	break;
	}
	return 0;
}
