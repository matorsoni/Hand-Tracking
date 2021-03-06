import numpy as np
import cv2 as cv

def segHand(imInput):
	# Filter original 
	imFiltered = cv.GaussianBlur(imInput, (3,3), 10)
	# cv.imshow('Blurred', imFiltered)

	# Calculate sharper image
	lapKernel = np.array([[1, 1, 1], [1, -8, 1], [1, 1, 1]])
	imLaplacian = cv.filter2D(imFiltered, cv.CV_32F, lapKernel) # Apply laplacian filter

	imSharp = np.float32(imInput) - imLaplacian
	imSharp = np.uint8(np.clip(imSharp, 0, 255) )
	# cv.imshow('Sharp', imSharp)

	# Otsu Threshold
	_, imThreshold = cv.threshold(imSharp, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)

	# Opening to remove noise
	SE = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5,5) ) 
	imErode = cv.erode(imThreshold, SE)
	imOpening = cv.dilate(imErode, SE)

	# Distance transformation
	imDist = cv.distanceTransform(imOpening, cv.DIST_L2, cv.DIST_MASK_3)
	imDist = np.uint8(cv.normalize(imDist, imDist, 0, 255, cv.NORM_MINMAX))
	# cv.imshow('Distance', imDist)

	# Threshold of distance
	threshVal, _ = cv.threshold(imDist, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
	_, imDistThresh = cv.threshold(imDist, round(2.5*threshVal), 255, cv.THRESH_BINARY)
	# cv.imshow('Distance Threshold', imDistThresh)
	# print("Distance threshold: ", round(2.5*threshVal))

	# Background marker
	SE = cv.getStructuringElement(cv.MORPH_ELLIPSE, (15,15))
	extMarker = cv.dilate(imThreshold, SE)
	extMarker = 255 - extMarker

	# Foreground markers
	contours, _ = cv.findContours(imDistThresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
	markers = np.zeros(imDistThresh.shape, dtype=np.int32)
	for i in range(len(contours)):
	    cv.drawContours(markers, contours, i, (i+1), -1)

	# print(np.amax(markers))

	# All markers
	markers += extMarker

	cv.watershed(cv.cvtColor(imFiltered, cv.COLOR_GRAY2BGR), markers)

	# cv.imshow('Markers', np.uint8(markers) )

	return np.uint8(markers)
	# return imOpening