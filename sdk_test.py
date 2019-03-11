import sys, ctypes

from triangulation import *
from segHand import *
from detectFingers import *

def find_xmin(hull):
    xlist = []
    for p in hull:
        xlist.append(p[0][0])

    xmin = min(xlist)
    for i, p in enumerate(hull):
        if p[0][0] == xmin:
            return i


controller = Leap.Controller()
controller.set_policy(Leap.Controller.POLICY_IMAGES)

# change accordingly
save_dir = "/home/morsoni/dev/python/venvs/py2/projects/hand-tracking/images/"

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

            left_fingers, left_hulls = detectFingers(left_image_array)
            right_fingers, right_hulls = detectFingers(right_image_array) 

            if (len(left_hulls) == 1 and len(right_hulls) == 1):
                leftHull = left_hulls[0]
                rightHull = right_hulls[0]

                i = find_xmin(leftHull)
                j = find_xmin(rightHull)
                pos_list = find_position( left_image, right_image, [(leftHull[i][0],rightHull[j][0])] )
                print (pos_list)



            cv.imshow('Fingers L', left_fingers)
            cv.imshow('Fingers R', right_fingers)





            # save images L and R
            #if cv.waitKey(30) == ord('s') :
            #    cv.imwrite(save_dir + "raw_" + str(frame.id) + "_L.png", left_image)
            #    cv.imwrite(save_dir + "raw_" + str(frame.id) + "_R.png", right_image)
            #    print "Frame captured"

cv.destroyAllWindows()