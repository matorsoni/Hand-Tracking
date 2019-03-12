import sys, ctypes

from triangulation import *
from segHand import *
from detectFingers import *

controller = Leap.Controller()
controller.set_policy(Leap.Controller.POLICY_IMAGES)

while((not (cv.waitKey(1) & 0xFF == ord('q')))):
    
    if(controller.is_connected):
        frame = controller.frame()
        left_image = frame.images[0]
        right_image = frame.images[1]

        if(left_image.is_valid and right_image.is_valid):
            # first allocate images as ctypes array
            # https://developer-archive.leapmotion.com/documentation/python/api/Leap.Image.html#Leap.Image.data_pointer
            left_ctype_array_def = ctypes.c_ubyte * left_image.width * left_image.height
            left_ctype_array = left_ctype_array_def.from_address(int(left_image.data_pointer))
            right_ctype_array_def = ctypes.c_ubyte * right_image.width * right_image.height
            right_ctype_array = right_ctype_array_def.from_address(int(right_image.data_pointer))

            # them as numpy array
            left_image_array = np.ctypeslib.as_array(left_ctype_array)
            right_image_array = np.ctypeslib.as_array(right_ctype_array)

            # Add segmentation + pixel selection + triangulation


            left_fingers, leftIm = detectFingers(left_image_array)
            right_fingers, rightIm = detectFingers(right_image_array) 

            cv.imshow('Fingers L', leftIm)
            cv.imshow('Fingers R', rightIm)

            if (len(left_fingers) == 5 and len(right_fingers) == 5):
                pos_list = find_position( left_image, right_image, zip(left_fingers, right_fingers), True )
                
                print "------------------------------------"
                for i, pos in enumerate(pos_list) :
                    print "Finger {}: x = {} ; y = {} ; z = {}".format(i, pos[0], pos[1], pos[2])

cv.destroyAllWindows()