# VideoTrackingMO446
Performance evaluation of tracking algorithms

------

###Instructions for downloading videos from youtube (select mp4 format)

`http://savefrom.net/`

###Tool to change frame rate (choose 12 fps):

    sudo apt-get install gpac
    MP4Box -add teste.mp4#video -raw 1 -new test
    MP4Box -add test_track1.h264:fps=12 -new teste2.mp4
