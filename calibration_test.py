import numpy as np
import cv2

dist = np.load("cam_dist.npy")
mtx = np.load("cam_matrix.npy")

img_dir = "/home/morsoni/dev/python/venvs/py2/projects/Hand-Tracking/chess/"
im_original = cv2.imread(img_dir + "chess_13_L.png", cv2.IMREAD_GRAYSCALE)

im_undistorted = cv2.undistort(im_original, mtx, dist)
cv2.imshow("original", im_original)
cv2.imshow("undistorted", im_undistorted)

cv2.waitKey(0)

cv2.destroyAllWindows()