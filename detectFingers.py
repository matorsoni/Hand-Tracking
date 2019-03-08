import cv2 as cv
import numpy as np
from segHand import *

def dist(p1,p2):
    return np.sqrt( (p1[0][0]-p2[0][0])**2 + (p1[0][1]-p2[0][1])**2 )

def removeArray(L,arr):
    ind = 0
    size = len(L)
    while ind != size and not np.array_equal(L[ind],arr):
        ind += 1
    if ind != size:
        L.pop(ind)
    else:
        raise ValueError('array not found in list.')

def partition(originalPoints, distFun, maxDist):
    points = list(originalPoints) # Points to be trated
    
    # List of all partitions
    partitionList = []
    
    # While there are still points to be treated
    while len(points) > 0:

        # Add first element
        p1 = points.pop(0)
        partition = [p1]
        added = [p1]

        # Search elements that belong to same partition 
        while added:
            p1 = added.pop(0)
                   
            # Search all elements close to p1
            peers = []
            for p in points:
                if distFun(p1,p) <= maxDist:
                    peers.append(p)
            
            added += peers
            partition += peers
            
            # Remove newly added points from original list
            for a in peers:
                removeArray(points,a)
            
        # Add partition to the list
        partitionList.append(partition)
    
    return partitionList

def detectFingers(imInput):
	# Color copy of input
	imColor = cv.cvtColor(imInput, cv.COLOR_GRAY2BGR)

	# Binary image from segmented objects
	imSegmented = segHand(imInput)
	_, imBinary = cv.threshold(imSegmented, 254, 255, cv.THRESH_BINARY_INV)

	# Find contours
	contours, _ = cv.findContours(imBinary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
	imContours = imColor.copy()
	cv.drawContours(imContours, contours, -1, (0,0,255), 2)

	# Convex Hull
	# hulls = []
	# for contour in contours:
	#     hulls.append(cv.convexHull(contour, False))


	hulls = []
	for contour in contours:
		hull = cv.convexHull(contour, False)
		part = partition(hull,dist,10)

		meanPoints = []
		for p in part:
			meanPoints.append( [list(map(int,np.round(np.mean(p,0))[0] ) )] )
			# meanPoints.append( [list(map(int, ) )] )   np.int(np.round(np.mean(p,0))[0])
		hulls.append(np.array(meanPoints))
    



	cv.drawContours(imContours, hulls, -1, (0,255,0), 2)
	for hull in hulls:
	    for point in hull:
	        cv.circle(imContours,tuple(point[0]), 5, (255,0,0), 2)

	return imContours
