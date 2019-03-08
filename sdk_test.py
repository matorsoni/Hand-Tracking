import cv2, sys, ctypes, numpy as np
sys.path.insert(0, "./lib")
import Leap
from segHand import *

controller = Leap.Controller()
controller.set_policy(Leap.Controller.POLICY_IMAGES)

# change accordingly
save_dir = "/home/morsoni/dev/python/venvs/py2/projects/hand-tracking/images/"

while((not (cv2.waitKey(1) & 0xFF == ord('q')))):

    if(controller.is_connected):
        frame = controller.frame()
        image_list = frame.images

        if(image_list[0].is_valid and image_list[1].is_valid):
            # allocate images as np.array
            # https://developer-archive.leapmotion.com/documentation/python/api/Leap.Image.html#Leap.Image.data_pointer
            left_ctype_array_def = ctypes.c_ubyte * image_list[0].width * image_list[0].height
            right_ctype_array_def = ctypes.c_ubyte * image_list[1].width * image_list[1].height
            # first as ctypes array
            left_ctype_array = left_ctype_array_def.from_address(int(image_list[0].data_pointer))
            right_ctype_array = right_ctype_array_def.from_address(int(image_list[1].data_pointer))
            # them as numpy array
            left_image = np.ctypeslib.as_array(left_ctype_array)
            right_image = np.ctypeslib.as_array(right_ctype_array)
            
            # https://developer-archive.leapmotion.com/documentation/python/api/Leap.Image.html#Leap.Image.distortion
            

            cv2.imshow('Frame L', left_image)
            cv2.imshow('Frame R', right_image)

            cv2.imshow('Segmentation L', segHand(left_image))
            cv2.imshow('Segmentation R', segHand(right_image))



            # save images L and R
            if cv2.waitKey(30) == ord('s') :
                cv2.imwrite(save_dir + "raw_" + str(frame.id) + "_L.png", left_image)
                cv2.imwrite(save_dir + "raw_" + str(frame.id) + "_R.png", right_image)
                print "Frame captured"

            #left_pixel_list = [ (x1,y1),(x2,y2) ...]; right_pixel_list = [...]
            #for left_pixel, right_pixel in zip(left_pixel_list, right_pixel_list) : 
            #   left_slopes = image_list[0].rectify(Leap.vector(left_pixel[0], left_pixel[1], 0))
            #   right_slopes = image_list[1].rectify(Leap.vector(right_pixel[0], right_pixel[1], 0))  
            #
            #   o1 = np.zeros(3); v1 = np.array() # origin and direction of left light ray
            #   o2 = np.array(); v2 = np.array() # origin and direction of right light ray
            #
            #   A = np.array([[np.dot(v1, v1), -np.dot(v1, v2)],
            #                   [np.dot(v1, v2), -np.dot(v2, v2)]])
            #   b = np.array([np.dot(o2 - o1, v1), np.dot(o2 - o1, v2)])
            #   alpha, beta = np.linalg.solve(A, b)
            #
            #   estimated_position = 0.5*(left_origin + alpha*left_ray + right_origin + beta*right_ray)

cv2.destroyAllWindows()