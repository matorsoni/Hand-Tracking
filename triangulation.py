import numpy as np
import sys

sys.path.insert(0, "./lib")
import Leap

class Ray:
    def __init__(self, origin = np.zeros(3), direction = np.array([1,0,0])):
        self.origin = origin
        self.direction = direction
    
    def point(self, t):
        return self.origin + t * self.direction

    def v(self):
        return self.direction

    def o(self):
        return self.origin

def direction_from_pixel(image, pixel):
    '''
    Corrects distortion for this specific pixel and returns its light ray direction.
    image: Leap.Image ; pixel: (int, int)

    https://developer-archive.leapmotion.com/documentation/python/api/Leap.Image.html#Leap.Image.distortion
    '''
    if (pixel[0] >= 0 and pixel[0] <= image.width and pixel[1] >= 0 and pixel[1] <= image.height) :
        slope = image.rectify(Leap.Vector(pixel[0], pixel[1], 0))
        x_angle = np.arctan(slope.x)
        y_angle = np.arctan(slope.y)

        x = np.cos(y_angle) * np.sin(x_angle)
        y = np.sin(y_angle)
        z = - np.cos(y_angle) * np.cos(x_angle)

        return np.array([x, y, z])
    
    else :
        print "Pixel not in image"
        return np.zeros(3)

def find_closest_point(leftRay, rightRay):
    '''
    Simple triangulation to find the point closest to leftRay and rightRay
    leftRay: Ray ; rightRay: Ray
    '''
    # translation vector from left camera to right camera
    T = rightRay.o() - leftRay.o()
    v1 = leftRay.v()
    v2 = rightRay.v()

    # solve linear system to find t1 and t2 such that
    # rightRay(t2)-leftRay(t1) is orthogonal to both v1 and v2
    A = np.array([
        [np.dot(v1,v1) , - np.dot(v1,v2)] ,
        [np.dot(v1,v2) , - np.dot(v2,v2)]
    ])
    b = np.array([ np.dot(T,v1) , np.dot(T,v2) ])

    t1, t2 = np.linalg.solve(A, b)

    # returns the mid point between leftRay(t1) and rightRay(t2)
    return 0.5 * (leftRay.point(t1) + rightRay.point(t2))

def CamCoord_to_LeapCoord(posCam):
    '''
    Position in left camera coordinates to Leap coordinates
    T ([P]camera) = [P]leap
    T = |-1  0  0  dx  |
        | 0  0 -1  -dy |
        | 0  1  0  0   |
        | 0  0  0  1   |
    '''
    dx = 2.5 # maybe change these
    dy = 0.5
    T_transp = np.array([
        [-1,  0, 0, 0],
        [0,   0, 1, 0],
        [0,  -1, 0, 0],
        [dx, -dy, 0, 1]
    ])
    posLeap = np.dot(np.append(posCam,1), T_transp)

    return np.array([posLeap[0], posLeap[1], posLeap[2]])


def find_position(leftImage, rightImage, pixelPairList, inLeapCoord = False):
    '''
    leftImage: Leap.Image ; rightImage: Leap.Image ; pixelPairList: list ; inLeapCoord: bool
    '''
    # List of 3D positions in the Leap Motion coordinate system
    # https://developer-archive.leapmotion.com/documentation/v2/python/devguide/Leap_Overview.html#coordinate-system
    position_list = []

    for leftPixel, rightPixel in pixelPairList:
        # We calculate the light rays in the left camera coordinate system
        leftOrigin = np.zeros(3)
        leftDirection = direction_from_pixel(leftImage, leftPixel)
        leftRay = Ray(leftOrigin, leftDirection)

        rightOrigin = np.array([4, 0, 0]) # in cm
        rightDirection = direction_from_pixel(rightImage, rightPixel)
        rightRay = Ray(rightOrigin, rightDirection)

        estimated_position = find_closest_point(leftRay, rightRay)

        if inLeapCoord:
            position_list.append(CamCoord_to_LeapCoord(estimated_position))
        else:
            position_list.append(estimated_position)
    
    return position_list


