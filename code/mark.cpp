#include <cv.h>
#include <highgui.h>
#include <fstream>

using namespace cv;
using namespace std;

char* videoName;
VideoCapture capture;
int lastX;
int lastY;

void CallBackFunc(int event, int x, int y, int flags, void* userdata) {

	if  (event == EVENT_MOUSEMOVE ) {
		lastX = x;
		lastY = y;
	}
}

int main( int argc, char** argv )
{
	videoName = argv[1];
	
	capture.open(videoName);

	if( argc != 2 || !capture.isOpened() ) {
		printf( "No video data\n");
		return -1;
	}

	Mat frame;
	namedWindow(videoName, CV_WINDOW_AUTOSIZE);
	setMouseCallback(videoName, CallBackFunc, NULL);

	string outputFile(videoName);
	outputFile.append(".txt");
	ofstream myfile;
  	myfile.open (outputFile.c_str());
	int frames = 0;
	while(true)
	{
		frames++;
	    capture >> frame;
	    if (frame.empty())
	        break;
	    imshow(videoName, frame);
	    waitKey(0);
	    myfile << lastX << " " << lastY << "\n";
	}
	printf("%d\n", frames);
	myfile.close();
	return 0;
}
