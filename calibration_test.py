import numpy as np
import cv2

img_dir = "/home/morsoni/dev/python/venvs/py2/projects/Hand-Tracking/chess/"
file_name = "chess_3_L.png"
im_original = cv2.imread(img_dir + file_name, cv2.IMREAD_GRAYSCALE)

if file_name[-5] == "L":
    dist = np.load("cam_dist_L.npy")
    mtx = np.load("cam_matrix_L.npy")
elif file_name[-5] == "R":
    dist = np.load("cam_dist_L.npy")
    mtx = np.load("cam_matrix_L.npy")
else: 
    dist = np.zeros(1)
    mtx = np.zeros(1)

im_undistorted = cv2.undistort(im_original, mtx, dist)
cv2.imshow("original", im_original)
cv2.imshow("undistorted", im_undistorted)

cv2.waitKey(0)

cv2.destroyAllWindows()