##
##  Cameo.py
##  Occu.py
##
##  Created on October 4, 2017 by Animesh Mishra
##  Copyright (c) 2017 Animesh Ltd. All Rights Reserved
##

import cv2
from Helpers import WindowManager, CaptureManager

class Cameo(object):
    def __init__(self):
        self._windowManager  = WindowManager.WindowManager("Cameo", self.onKeyPress)
        self._captureManager = CaptureManager.CaptureManager(cv2.VideoCapture(0), self._windowManager, True)

    def run(self):
        """ Run the main loop """
        self._windowManager.createWindow()
        while self._windowManager.isWindowCreated:
            self._captureManager.enterFrame()
            frame = self._captureManager.frame

            # TODO: Filter the frame

            self._captureManager.exitFrame()
            self._windowManager.processEvents()

    def onKeyPress(self, keycode):
        """ 
        Handle a key press.

        Space   -> Take a screenshot
        Tab     -> Start/stop recording a screencast
        Escape  -> Quit
        """
        if keycode == 32: # Space
            self._captureManager.writeImage("screenshot.png")
        elif keycode == 9: # Tab
            if not self._captureManager.isWritingVideo:
                self._captureManager.startWritingVideo("screencast.flv")
            else:
                self._captureManager.stopWritingVideo()
        elif keycode == 27: # Escape
            self._windowManager.destroyWindow()

if __name__ == "__main__":
    Cameo().run()