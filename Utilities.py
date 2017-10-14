##
##  Utilties.py
##  Occu.py
##
##  Created on October 13, 2017 by Animesh Mishra
##  Copyright (c) 2017 Animesh Ltd. All Rights Reserved
##

import cv2
import numpy
import scipy.interpolate

def createCurveFunc(points):
    """
    First step towards curve-based filters is to convert control points to a 
    function. This function returns a function derived from control points.

    Arguments:
        points: an array of (x,y) pairs. Must be ordered such that x increases
                from one indes to the next. Typically, for natural-looking effects,
                y values should increase too and the first and last control points
                should be (0,0) and (255,255) in order to preserve black and white.
                x will be treated as a channel's input value and y as the corresponding
                output value.
    """
    if points is None:
        return None
    
    pointsCount = len(points)
    if pointsCount < 2:
        return None

    arrayX, arrayY = zip(*points)
    
    if pointsCount < 4:
        kind = "linear"     # quadratic interpolation is not implemented
    else:
        kind = "cubic"      # cubic spline interpolation

    return scipy.interpolate.interp1d(arrayX, arrayY, kind, bounds_error = False)

def createCompositeFunc(func0, func1):
    """
    Return a composite of two curves functions. Useful if we want to apply
    two curves in succession to an image.
    """
    if func0 is None:
        return func1
    if func1 is None:
        return func0
    return lambda x: func0(func1(x))

def createFlatView(array): 
    """
    Returns a one-dimensional view of an array of any dimensionality.

    We use this when we want to apply the same curve to all channels of an image.
    Splitting and remerging channels would be wasteful becasue we do not need to
    distinguish between channels. We just need one-dimensional indexing as used
    by applyLookupArray().

    This function works for images with any number of channels.
    """
    # array.view() returns a numpy.view object, which only owns a reference to the
    # the data, not a copy.
    flatView        = array.view()
    flatView.shape  = array.size
    return flatView

##
##  The curves function might be expensive and we don't want to run it once per channel,
##  per pixel. Fortunately we are typically dealing with just 256 possible input values
##  (in 8 bits per channel) and we can cheaply precompute and store that many output
##  values. Then, our per-channel, per-pixel cost is just a lookup of the cached output
##  value.
##
def createLookupArray(func, length = 256):
    """
    Return a lookup for whole-number inputs to a function. The lookup values are
    clamped to [0, length-1].
    """
    if func is None:
        return None

    lookupArray = numpy.empty(length)
    
    i = 0
    while i < length:
        func_i = func(i)
        lookupArray[i] = min(max(0, func_i), length -1)
        i += 1
        
    return lookupArray

def applyLookupArray(lookupArray, source, destination):
    """
    Map a source to a destination using a lookup.
    """
    if lookupArray is None:
        return
    destination[:] = lookupArray[source]