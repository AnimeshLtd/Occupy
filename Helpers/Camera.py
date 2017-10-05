##
##  camera.py
##  Vision
##
##  This script demonstrates how to capture camera frames using OpenCV 3.
##
##  Created on October 4, 2017 by Animesh Mishra
##  Copyright (c) 2017 Animesh Ltd. All Rights Reserved
##

import cv2

# We initialise a camera capture by instantiating a VideoCapture object
# using a device index instead of a file path. The number of cameras and
# their ordering is of course system-dependent. Unfortunately, OpenCV does
# not provide any means of querying the number of cameras or their properties.
# If an invalid index is used to construct VideoCapture, the instance won't
# yield any frames and the read() method will return (false, None). 
camera = cv2.VideoCapture(0)

# The get() method doesn't return an accurate value for the camera's frame
# rate, it always returns 0. So we need to either make an assumption or measure
# frame reate using a timer. Latter approach is better.
fps = 30
frameHeight = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
frameWidth  = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
frameSize   = (frameWidth, frameHeight)

# Capture and save a 10 second video from camera
def record():
    codec = cv2.VideoWriter_fourcc(*"I420")
    videoWriter = cv2.VideoWriter("assets/Capture.avi", codec, fps, frameSize) 
    success, frame = camera.read()
    framesRemaining = (10 * fps) - 1
    while success and framesRemaining > 0:
        videoWriter.write(frame)
        success, frame = camera.read()
        framesRemaining -= 1


# Mouse event handler
clicked = False
def onMouse(event, x, y, flags, param):
    global clicked
    if event == cv2.EVENT_LBUTTONUP:
        clicked = True

# Display live feed from the camera
def showLiveFeed():
    cv2.namedWindow("Occu.py")
    cv2.setMouseCallback("Occu.py", onMouse)
    success, frame = camera.read()
    while success and cv2.waitKey(1) == -1 and not clicked:
            cv2.imshow("Occu.py", frame)
            success, frame = camera.read()
    cv2.destroyWindow("Occu.py")

showLiveFeed()