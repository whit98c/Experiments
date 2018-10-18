#!/bin/bash

USBNAME=webcam
LSUSB=$(lsusb | grep --ignore-case $USBNAME)
FOLD="/dev/bus/usb/"$(echo $LSUSB | cut --delimiter=' ' --fields='2')"/"$(echo $LSUSB | cut --delimiter=' ' --fields='4' | tr --delete ":")
echo $LSUSB
echo $FOLD

sudo ./usbreset $FOLD

sleep 5

sudo ./usbreset $FOLD

sleep 5

fswebcam -r 1920x1080 kitchen-`date +"%Y-%m-%d-%H-%M-%S"`.jpg
