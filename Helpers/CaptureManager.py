##
##  CaptureManager.py
##  Occu.py
##
##  Created on October 4, 2017 by Animesh Mishra
##  Copyright (c) 2017 Animesh Ltd. All Rights Reserved
##

import cv2
import numpy
import time

class CaptureManager(object):
    """
    A high-level interface for dispatching images from the capture stream to one or more outputs - image file,
    video file or a window.
    """
    def __init__(self, capture, previewWindowManager = None, shouldMirrorPreview = False):
        """
        A CaptureManager instance is initialised with a VideoCapture instance and has the enterFrame() and exitFrame()
        methods that should typically be called on every iteration of an application's main loop. Between a call to
        enterFrame() and a call to exitFrame(), the application may (any number of times) set a channel property and
        get a frame property. The channel property is initially 0 and only multi-head cameras use other values. The
        frame property is an image corresponding to the current channel's state when enterFrame() was called.

        VideoWriter instance needs a frame rate, but OpenCV doesn't provide any way to get accurate frame rate
        for a camera. So we use a frame counter and Python's standard time.time() to estimate the frame rate
        if necessary. The approach has its pitfalls, depending on frame rate fluctuations and system-dependent
        implementatio of time.time() the accuracy of the estimate might still be poor. However, it would still
        better than just assuming a particular frame rate for a given camera.

        Args:
            capture (VideoCapture): The capture stream
            previewWindowManager (WindowManager): If provided, capture feed is shown on screen
            shouldMirrorPreview (bool): If True, the live camera feed is mirrored (but not the saved file)
        """
        self.previewWindowManager = previewWindowManager
        self.shouldMirrorPreview  = shouldMirrorPreview

        self._capture       = capture
        self._channel       = 0
        self._enteredFrame  = False
        self._frame         = None
        self._imageFileName = None
        self._videoFileName = None
        self._videoEncoding = None
        self._videoWriter   = None

        self._startTime     = None
        self._framesElapsed = int(0)
        self._fpsEstimate   = None

    @property
    def channel(self):
        return self._channel

    @channel.setter
    def channel(self, value):
        if self._channel != value:
            self._channel = value
            self._frame   = None

    @property
    def frame(self):
        if self._enteredFrame and self._frame is None:
            _, self._frame = self._capture.retrieve(self.channel)
        return self._frame

    @property
    def isWritingImage(self):
        return self._imageFileName is not None

    @property
    def isWritingVideo(self):
        return self._videoFileName is not None

    def enterFrame(self):
        """Capture the next frame, if any."""
        # First check that the previous frame was exited properly
        assert not self._enteredFrame, \
            "Previous frame was not exited properly by calling exitFrame()."
        
        if self._capture is not None:
            # Only synchronises a frame, actual retrieval from a channel happens
            # when the frame property is read (see self.frame)
            self._enteredFrame = self._capture.grab()

    def exitFrame(self):
        """Draws the frame to a window, writes it to file and then releases the frame."""

        # Check whether any grabbed frame is retrievable.
        # The getter may retrieve and cache the frame
        if self.frame is None:
            self._enteredFrame = False
            return

        # Update the FPS estimate and related variables
        if self._framesElapsed == 0:
            self._startTime = time.time()
        else:
            timeElapsed = time.time() - self._startTime
            self._fpsEstimate = self._framesElapsed / timeElapsed
        self._framesElapsed += 1

        # Draw the frame to a window
        if self.previewWindowManager is not None:
            if self.shouldMirrorPreview:
                mirroredFrame = numpy.fliplr(self._frame).copy()
                self.previewWindowManager.show(mirroredFrame)
            else:
                self.previewWindowManager.show(self._frame)
        
        # Write the image file to disk
        if self.isWritingImage:
            cv2.imwrite(self._imageFileName, self._frame)
            self._imageFileName = None

        # Write video to disk
        self._writeVideoFrame()

        # Release the frame
        self._frame = None
        self._enteredFrame = False

    def writeImage(self, fileName):
        """Write the next exited frame to an image file"""
        self._imageFileName = fileName

    def startWritingVideo(self, fileName, encoding = cv2.VideoWriter_fourcc(*"FLV1")):
        """Start writing exited frames to a video file"""
        self._videoFileName = fileName
        self._videoEncoding = encoding

    def stopWritingVideo(self):
        """Stop writing exited frames to a video file"""
        self._videoFileName = None
        self._videoEncoding = None
        self._videoWriter   = None

    def _writeVideoFrame(self):
        if not self.isWritingVideo:
            return

        if self._videoWriter is None:
            fps = self._capture.get(cv2.CAP_PROP_FPS)
            if fps == 0.0:
                # The capture's FPS is unknown so use an estimate
                if self._framesElapsed < 20:
                    # Wait for more frames so that the estimate
                    # is more reliable
                    return
                else:
                    fps = self._fpsEstimate

            size = (int(self._capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
                    int(self._capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
            self._videoWriter = cv2.VideoWriter(self._videoFileName, self._videoEncoding, fps, size)
        
        self._videoWriter.write(self._frame)