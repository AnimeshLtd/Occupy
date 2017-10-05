##
##  video.py
##  Vision
##
##  This script demonstrates how to read/write video files using OpenCV 3
##  and showcases some common video formats.
##
##  OpenCV provides the VideoWriter and VideoCapture classes that support
##  various video file formats. Supported formats vary by system but should
##  always include AVI.
##  
##  Via its read() method, a VideoCapture instance may be polled for new frames
##  until it reached the end of the video file. Each frame is an image in BGR
##  format.
##
##  The write() method of a VideoWriter instance appends a given BGR image to 
##  a video file stream. VideoWriter needs a video codec to be specified. Here
##  are some options:
##      +   cv2.cv.CV_FOURCC("I", "4", "2", "0")
##              Uncompressed YUV, 4:2:0 chroma subsampled. Extension should be .avi
##      +   cv2.cv.CV_FOURCC("P", "I", "M", "1")
##              MPEG-1. Extension should be .avi
##      +   cv2.cv.CV_FOURCC("M", "J", "P", "G")
##              Motion-JPEG. Extension should be .avi
##      +   cv2.cv.CV_FOURCC("T", "H", "E", "O")
##              Ogg-Vorbis. Extension should be .ogv
##      +   cv2.cv.CV_FOURCC("F", "L", "V", "1")
##              Flash video. Extension should be .flv
##
##  Created on October 4, 2017 by Animesh Mishra
##  Copyright (c) 2017 Animesh Ltd. All Rights Reserved
##

import cv2

videoCapture = cv2.VideoCapture("assets/Input.avi")

# Get frame rate and size information. This is required by VideoWriter.
fps = videoCapture.get(cv2.CAP_PROP_FPS)
height = int(videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT))
width = int(videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH))
frameSize = (width, height)

# Initialise VideoWriter with a YUV codec
codec = cv2.VideoWriter_fourcc(*"I420")
videoWriter = cv2.VideoWriter("assets/Output.avi", codec, fps, frameSize)

# Append each frame in Input.avi to Output.avi
success, frame = videoCapture.read()
while success: # continues until there are no more frames
    videoWriter.write(frame)
    success, frame = videoCapture.read()