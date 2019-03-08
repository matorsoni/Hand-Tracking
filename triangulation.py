import numpy as np
sys.path.insert(0, "./lib")
import Leap

class Ray:
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction
    
    def point(self, t):
        return self.origin + t * self.direction
    
    def v(self):
        return self.direction
    
    def o(self):
        return self.origin

def direction_from_pixel(image: Leap.Image, pixel):
    slope = image.rectify(Leap.Vector(pixel[0], pixel[1], 0))
    x_angle = np.arctan(slope.x)
    y_angle = np.arctan(slope.y)

    x = np.cos(y_angle) * np.sin(x_angle)
    y = np.sin(y_angle)
    z = - np.cos(y_angle) * np.cos(x_angle)

    return np.array([x, y, z])

def find_closest_point(leftRay: Ray, rightRay: Ray):
    # translation vector from left camera to right camera
    T = rightRay.o - leftRay.o
    v1 = leftRay.v
    v2 = rightRay.v

    # solve linear system to find t1 and t2 such that
    # rightRay(t2)-leftRay(t1) is orthogonal to both v1 and v2
    A = np.array([
        [np.dot(v1,v1) , - np.dot(v1,v2)] ,
        [np.dot(v1,v2) , - np.dot(v2,v2)]
    ])
    b = np.array([ np.dot(T,v1) , np.dot(T,v2) ])

    t1, t2 = np.linalg.solve(A, b)

    # returns the mid point between leftRay(t1) and rightRay(t2)
    return 0.5 * (leftRay(t1) + rightRay(t2))

def CamCoord_to_LeapCoord(position):


def find_position(leftImage: Leap.Image, rightImage: Leap.Image,  pixelPairList, inLeapCoord = False):
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
            print "tranform this coordinates"

        position_list.append(estimated_position)
    
    return position_list


