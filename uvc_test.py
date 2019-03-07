import numpy as np
import cv2
import leapuvc

import sys
sys.path.insert(0, "./lib")
import Leap
from segHand import *

# Start the Leap Capture Thread
leap = leapuvc.leapImageThread()
leap.start()
leap.setExposure(30)

captured_frames = 0
save_dir = "/home/morsoni/dev/python/venvs/py2/projects/Hand-Tracking/chess/"
filename_prefix = "chess_"
# Capture images until 'q' is pressed
while((not (cv2.waitKey(1) & 0xFF == ord('q'))) and leap.running):
    newFrame, rawImages = leap.read()
    if(newFrame):

        # Display the raw frame
        cv2.imshow('Frame L', rawImages[0])
        cv2.imshow('Frame R', rawImages[1])
        cv2.imshow('Segmented L', segHand(rawImages[0]))
        cv2.imshow('Segmented R', segHand(rawImages[1]))

        # save images L and R
        if cv2.waitKey(30) == ord('s') :
            cv2.imwrite(save_dir + filename_prefix + str(captured_frames) + "_L.png", rawImages[0])
            cv2.imwrite(save_dir + filename_prefix + str(captured_frames) + "_R.png", rawImages[1])
            print "Frame captured"
            captured_frames += 1

            

cv2.destroyAllWindows()