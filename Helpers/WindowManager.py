##
##  WindowManager.py
##  Occu.py
##
##  Created on October 4, 2017 by Animesh Mishra
##  Copyright (c) 2017 Animesh Ltd. All Rights Reserved
##

import cv2

class WindowManager(object):
    """
    A high-level interface for managing preview windows and keyboard support.
    """

    def __init__(self, windowName = "Occu.py", keypressCallback = None):
        """
        Args:
            windowName (str): Name of the application window
            keypressCallback (func): Event handler for key presses. Must take a single argument, an ASCII keycode.
        """
        self.keypressCallback = keypressCallback
        self._windowName = windowName
        self._isWindowCreated = False

    @property
    def isWindowCreated(self):
        return self._isWindowCreated

    def createWindow(self):
        cv2.namedWindow(self._windowName)
        self._isWindowCreated = True
    
    def show(self, frame):
        cv2.imshow(self._windowName, frame)

    def destroyWindow(self):
        cv2.destroyWindow(self._windowName)
        self._isWindowCreated = False

    def processEvents(self):
        keycode = cv2.waitKey(1)
        if self.keypressCallback is not None and keycode != -1:
            # Discard any non-ASCII info encoded by GTK
            keycode &= 0xFF
            self.keypressCallback(keycode)