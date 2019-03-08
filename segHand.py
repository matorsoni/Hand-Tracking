import numpy as np
import cv2 as cv

def segHand(imInput):
	# Filter original 
	imFiltered = cv.GaussianBlur(imInput, (3,3), 1)

	# Calculate sharper image
	lapKernel = np.array([[1, 1, 1], [1, -8, 1], [1, 1, 1]])
	imLaplacian = cv.filter2D(imFiltered, cv.CV_32F, lapKernel) # Apply laplacian filter

	imSharp = np.float32(imInput) - imLaplacian
	imSharp = np.uint8(np.clip(imSharp, 0, 255) )

	# Otsu Threshold
	_, imThreshold = cv.threshold(imSharp, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)

	# Erosion to remove small objects
	SE = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3,3) ) 
	imThreshErode = cv.erode(imThreshold, SE)
	# imThreshOpen = cv.dilate(imThreshOpen, SE)

	# Distance transformation
	imDist = cv.distanceTransform(imThreshold, cv.DIST_L2, cv.DIST_MASK_3)
	imDist = np.uint8(imDist)

	# imDist = np.uint8(cv.normalize(imDist, imDist, 0, 255, cv.NORM_MINMAX))

	# Threshold of distance

	t_, imDistThresh = cv.threshold(imDist, 3, 255, cv.THRESH_BINARY)

	# threshVal, _ = cv.threshold(imDist, 200, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
	# _, imDistThresh = cv.threshold(imDist, round(2.5*threshVal), 255, cv.THRESH_BINARY)
	# print("Distance threshold: ", round(2.5*threshVal))

	# Closing to remove small holes
	SE = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5,5) ) 
	# imOpening = cv.erode(imDistThresh, SE)
	# imOpening = cv.dilate(imOpening, SE)
	imDistClosing = cv.dilate(imDistThresh, SE)
	imDistClosing = cv.erode(imDistClosing, SE)
	# imDistErode = cv.erode(imDistThresh, SE)

	# Background marker
	SE = cv.getStructuringElement(cv.MORPH_ELLIPSE, (15,15))
	extMarker = cv.dilate(imThreshold, SE)
	extMarker = 255 - extMarker

	# Foreground markers
	contours, _ = cv.findContours(imDistClosing, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
	markers = np.zeros(imInput.shape, dtype=np.int32)
	for i in range(len(contours)):
	    cv.drawContours(markers, contours, i, (i+1), -1)

	# print(np.amax(markers))

	# All markers
	markers += extMarker

	cv.watershed(cv.cvtColor(imFiltered, cv.COLOR_GRAY2BGR), markers)

	# return np.uint8(10*markers)
	return imDistThresh