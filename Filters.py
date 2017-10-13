##
##  Filters.py
##  Occu.py
##
##  Created on October 13, 2017 by Animesh Mishra
##  Copyright (c) 2017 Animesh Ltd. All Rights Reserved
##

import cv2
import numpy
import Utilities

def recolourRC(source, destination):
    """
    Simulate conversion from BGR to RC.
    The source and destination images must both be in BGR format.

    Blues and greens are replaced with cyans. Psuedocode:
        destination.blue = destination.green = (source.blue + source.green) / 2
        destination.red  = source.red
    """
    # Extract source image's channels as one-dimensional arrays
    blue, green, red = cv2.split(source)

    # Replace the blue channel's values with an average of blue and green
    # addWeighted(source1, weight1, source2, weight2, constant, destination)
    cv2.addWeighted(blue, 0.5, green, 0.5, 0, blue)

    # Replace the values in our destination image with modified channels
    # Using blue twice because we want blue and green channels to be equal.
    cv2.merge((blue, blue, red), destination)

def recolourRGV(source, destination):
    """
    Simulate conversion from BGR to RGV.
    The source and destination images must both be in BGR format.

    Blues are desaturated. Pseudocode:
    destination.blue  = min(source.blue, source.green, source.red)
    destination.green = source.green
    destination.red   = source.red  
    """
    blue, green, red = cv2.split(source)
    cv2.min(blue, green, minimum)
    cv2.min(minimum, red, blue)
    cv2.merge((blue, green, red), destination)

def recolourCMV(source, destination):
    """
    Simulate conversion from BGR to CMV (cyan, magenta, value).abs
    Source and destination images must both be in BGR format.abs

    Yellows are desaturated. Pseudocode:
    destination.blue  = max(source.blue, source.green, source.red)
    destination.green = source.green
    destination.red   = source.red
    """
    blue, green, red = cv2.split(source)
    cv2.max(blue, green, maximum)
    cv2.max(maximum, red, blue)
    cv2.merge((blue, green, red), destination)

# ******************************************************************************************************************* #

## Filter classes

class VFuncFilter(object):
    """
    A filter that applies a function to the value (V) channel of
    a greyscale image or to all channels of a colour image.
    """
    def __init__(self, vFunc = None, dataType = numpy.uint8):
        length = numpy.iinfo(dataType).max + 1
        self._vLookupArray = Utilities.createLookupArray(vFunc, length)

    def apply(self, source, destination):
        """
        Apply the filter with a BGR or grey source/destination
        """
        sourceFlatView = Utilities.createFlatView(source)
        destinationFlatView = Utilities.createFlatView(destination)
        Utilities.applyLookupArray(self._vLookupArray, sourceFlatView, destinationFlatView)

class VCurveFilter(VFuncFilter):
    """
    A filter that applies a curve to the value (V) channel of a greyscale
    image or to all channels of a colour image.
    """
    def __init__(self, vPoints, dataType = numpy.uint8):
        VFuncFilter.__init__(self, Utilities.createCurveFunc(vPoints), dataType)

class BGRFuncFilter(object):
    """
    A filter that applies different functions to each of BGR.
    """
    def __init__(self, vFunc = None, bFunc = None, gFunc = None, rFunc = None, dataType = numpy.uint8):
        length = numpy.iinfo(dataType).max + 1
        self._bLookupArray = Utilities.createLookupArray(Utilities.createCompositeFunc(bFunc, vFunc), length)
        self._gLookupArray = Utilities.createLookupArray(Utilities.createCompositeFunc(gFunc, vFunc), length)
        self._rLookupArray = Utilities.createLookupArray(Utilities.createCompositeFunc(rFunc, vFunc), length)

    def apply(self, source, destination):
        """
        Apply the filter with a BGR source/destination
        """
        blue, green, red = cv2.split(source)
        Utilities.applyLookupArray(self._bLookupArray, blue, blue)
        Utilities.applyLookupArray(self._gLookupArray, green, green)
        Utilities.applyLookupArray(self._rLookupArray, red, red)
        cv2.merge([blue, green, red], destination)

class BGRCurveFilter(BGRFuncFilter):
    """

    """
    def __init__(self, vPoints = None, bPoints = None, gPoints = None, rPoints = None, dataType = numpy.uint8):
        BGRFuncFilter.__init__(self, Utilities.createCurveFunc(vPoints),
                                     Utilities.createCurveFunc(bPoints),
                                     Utilities.createCurveFunc(gPoints),
                                     Utilities.createCurveFunc(rPoints),
                                     dataType)

# ******************************************************************************************************************* #

## Film-like filters

class BGRPortraCurveFilter(BGRCurveFilter):
    """
    A filter that applies Portra-like curves to BGR.

    Portra has a broad highlight range that tends toward warm (amber) colours, while shadows
    are cooler (more blue). As a portrait film, it tends to make people's complexions fairer.
    Also, it exaggerates certain common clothing colours, such as milky white and dark blue.
    """
    def __init__(self, dataType = numpy.uint8):
        BGRCurveFilter.__init__(self, vPoints = [(0,0), (23,20), (157,173), (255,255)],
                                      bPoints = [(0,0), (41,46), (231,228), (255,255)],
                                      gPoints = [(0,0), (52,47), (189,196), (255,255)],
                                      rPoints = [(0,0), (69,69), (213,218), (255,255)],
                                      dataType = dataType)

class BGRProviaCurveFilter(BGRCurveFilter):
    """
    A filter that applies Provia-like curves to BGR.

    Provia has a strong contrast and is slightly cool (blue) throughout most tones. Sky,
    water and shade are enhanced more than the sun.
    """
    def __init__(self, dataType = numpy.uint8):
        BGRCurveFilter.__init__(self, bPoints = [(0,0), (35,25), (205,227), (255,255)],
                                      gPoints = [(0,0), (27,21), (196,207), (255,255)],
                                      rPoints = [(0,0), (59,54), (202,210), (255,255)],
                                      dataType = dataType)

class BGRVelviaCurveFilter(BGRCurveFilter):
    """
    A filter that applies Velvia-like curves to BGR.

    Velvia has deep shadows and vivid colours. It can often produce azure skies in daytime
    and crimson clouds at sunset. The effect is difficult to emulate.
    """
    def __init__(self, dataType = numpy.uint8):
        BGRCurveFilter.__init__(self, vPoints = [(0,0), (128,118), (221,215), (255,255)],
                                      bPoints = [(0,0), (25,21), (122,153), (165,206), (255,255)],
                                      gPoints = [(0,0), (25,21), (95,102), (181,208), (255,255)],
                                      rPoints = [(0,0), (41,28), (183,209), (255,255)],
                                      dataType = dataType)

class BGRCrossProcessCurveFilter(BGRCurveFilter):
    """
    A filter that applies cross-process like curves to BGR.

    Cross-processing produces a strong, blue or greenish-blue tint in shadows and a strong,
    yellow or greenish-yellow in highlights. Black and white are not necessarily preserved.
    Also, contrast is very high. Cross-processed photos take on a sickly appearance. People
    look jaundiced, while inanimate object looks stained.
    """
    def __init__(self, dataType = numpy.uint8):
        BGRCurveFilter.__init__(self, bPoints = [(0,20), (255, 235)],
                                      gPoints = [(0,0), (56,39), (208,226), (255,255)],
                                      rPoints = [(0,0), (56,22), (211,255), (255,255)],
                                      dataType = dataType)