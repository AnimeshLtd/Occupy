##
##  image.py
##  Vision
##
##  This script demonstrates how to read/write image using OpenCV 3
##  and showcases some common image operations.
##  
##  Library functions used:
##      - imread()
##      - imwrite()
##
##  Created on October 4, 2017 by Animesh Mishra
##  Copyright (c) 2017 Animesh Ltd. All Rights Reserved
##

import cv2
from enum import IntEnum

# imread() uses flags to specify reading mode. They work just fine but
# are ugly as hell (cv2.IMREAD_COLOR, cv2.IMREAD_GRAYSCAL etc.). These
# flags are simply numbers in disguise so I have created a convenience
# type to make the code more readable.
class ReadMode(IntEnum):
    Colour = 1
    Grayscale = 0
    Unchanged = -1

# Read an image on disk. By default imread() returns an image in BGR colour
# format, even if the file is grayscale. BGR is same as RGB but the byte
# order is reversed. imread() discards any alpha channel by default, to 
# preserve transparency use cv2.IMREAD_UNCHANGED flag. 
grayImage = cv2.imread("Untitled.jpg", ReadMode.Grayscale)

# Display the grayscale image in a window titled "Vision"
cv2.imshow("Vision", grayImage)
# Record key press
key = cv2.waitKey(0)
# Close the window if ESC key (27) is pressed, otherwise if the 'S' key
# is pressed, save the grayscale image to disk and then close the window.
if key == 27:
    cv2.destroyAllWindows()
elif key == ord("s"):
    cv2.imwrite("GrayUntitled.png", grayImage)
    cv2.destroyAllWindows()