#!/bin/bash

`lsusb -d 05e3:0608 | head -n 1 | awk  '{print "sudo ./usbreset /dev/bus/usb/"$2"/"substr($4,0,4)}'`
`lsusb -d 05e3:0608 | tail -n 1 | awk  '{print "sudo ./usbreset /dev/bus/usb/"$2"/"substr($4,0,4)}'`

#Sleep to give the OS time to load the webcam
sleep 5

fswebcam images/image.jpeg
