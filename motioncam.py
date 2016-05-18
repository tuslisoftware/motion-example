#!/usr/bin/env python

"""
Basic Motion Detection
Author: Tusli Software LLC (info@tuslisoftware.com)
Written: May 18, 2016
Updated: May 18, 2016

A demonstration of basic motion detection using OpenCV.
"""

import cv2
import time
from datetime import datetime
import numpy as np
import os.path

DISPLAY = True

# Set up the camera, and set the capture width and height
capture = cv2.VideoCapture(0)
capture.set(3, 640)
capture.set(4, 480)

# Wait for camera to start
time.sleep(1.0)

# Get the initial image to create the average image
f, frame = capture.read()

# Convert the image to grayscale
gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

# Convert the grayscale image to a multi-dimensional array of 32-bit floats
avg = np.float32(gray)

# Run until the user presses 'q'
while True:

    # Read a frame from the camera
    f, frame = capture.read()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    # Add the grayscale image to the average image
    cv2.accumulateWeighted(gray, avg, 0.3)

    # Scale the average image to 8-bit image
    res = cv2.convertScaleAbs(avg)

    # Get the absolute difference between res and diff
    diff = cv2.absdiff(gray, res)

    # Threshold diff. Pixels >= 60 will be white, pixels < 60 will be black
    f, thresh = cv2.threshold(diff, 60, 255, 0)

    # Count the white pixels in the threshold image. White pixels mean motion
    wp = cv2.countNonZero(thresh)

    # If there are enough white pixels, save the image
    if wp > 100:

        # The filename will be the date and time
        fname = datetime.strftime(datetime.now(), '%Y-%m-%d_%H.%M.%S') + ".jpg"

        # Check if the image file exists. If not, save the image
        if not os.path.isfile(fname):
            cv2.imwrite(fname, frame)

    # For efficiency and to turn in the background, set DISPLAY to False
    if DISPLAY:
        cv2.imshow("Frame", frame)

    # Wait and check if the user pressed 'q'
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

# Clean up any open windows
cv2.destroyAllWindows()
