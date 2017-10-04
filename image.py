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
import numpy
import os
from enum import IntEnum

# imread() uses flags to specify reading mode. They work just fine but
# are ugly as hell (cv2.IMREAD_COLOR, cv2.IMREAD_GRAYSCAL etc.). These
# flags are simply numbers in disguise so I have created a convenience
# type to make the code more readable.
class ReadMode(IntEnum):
    Colour      = 1
    Grayscale   = 0
    Unchanged   = -1

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

##
##  Image and raw bytes
##  
##  An OpenCV image is a 2D or 3D array of type numpy.array. A grayscale image is
##  a 2D array containing byte values (integers from 0 to 255) and a 24-bit BGR 
##  image is a 3D array. We can access the individual pixels like so:
##
##  Grayscale   - image[y, x]
##  BGR         - image[y, x, channel]
##  E.g. image[0, 0] is the pixel at top-left corner of the image. If it's value
##  is 255, it means it's a white pixel.
##
##  We can cast an image to a standard Python bytearray, provided it has 8 bits 
##  per channel. Conversely, provided a bytearray contains bytes in an appropriate 
##  order we can cast and then reshape it to get a numpy.array type that is an image.
##

# Make an array of 120,000 random bytes
randomByteArray = bytearray(os.urandom(120000))
flatNumpyArray = numpy.array(randomByteArray)

# Convert the array to make a 400 x 300 grayscale image
randomGrayImage = flatNumpyArray.reshape(300, 400)
cv2.imwrite("RandomGray.png", randomGrayImage)

# Convert the array to make a 400 x 100 colour image
randomBGRImage = flatNumpyArray.reshape(100, 400, 3)
cv2.imwrite("RandomBGR.png", randomBGRImage)