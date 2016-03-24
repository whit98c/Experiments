#!/bin/sh

DATE=$(date "+%Y%m%d%H%M")

fswebcam -r 1280x720 -S 4 -d /dev/video0 webcam-$DATE.png
./dropbox_uploader.sh upload webcam.png webcam-$DATE.png
