import cv2 as cv
import numpy as np
from segHand import segHand
from filterHull import filterHull
from filterFingers import filterFingers

def detectFingers(imInput):
    # Color copy of input
    imColor = cv.cvtColor(imInput, cv.COLOR_GRAY2BGR)

    # Binary image from segmented objects
    imSegmented = segHand(imInput)
    _, imBinary = cv.threshold(imSegmented, 254, 255, cv.THRESH_BINARY_INV)

    # Find contours
    contours, _ = cv.findContours(imBinary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    imContours = imColor.copy()

    # Convexity analysis
    hulls = []
    defects = []
    fingers = []
    for contour in contours:
        hullIndices = cv.convexHull(contour, None, False, False) # Calculate convex hulls
        hullIndices = filterHull(contour,hullIndices,10) # Clusters close points together

        defectList = cv.convexityDefects(contour, hullIndices) # Calculates convexity defects
        fingerIndices = filterFingers(contour, defectList) # Identifies which points are fingers

        defects.append( ([contour[d[0][2] ] for d in defectList]) )
        hulls.append(np.array( [contour[i[0]] for i in hullIndices] ) )
        fingers.append(np.array( [contour[i[0]] for i in fingerIndices] ) )

    # Drawings
    # cv.drawContours(imContours, contours, -1, (0,0,255), 1) # Hand contour
    # cv.drawContours(imContours, hulls, -1, (0,255,0), 2) # Convex Hull
    # for hull in hulls:
    #     for point in hull:
    #         cv.circle(imContours,tuple(point[0]), 5, (255,0,0), 2) # Finger candidates
    # for defect in defects:
    #     for point in defect:
    #         cv.circle(imContours,tuple(point[0]), 5, (255,0,255), 2) # Convex defects
    for finger in fingers:
        for point in finger:
            cv.circle(imContours,tuple(point[0]), 5, (255,255,0), 2) # Fingers

    return imContours


imInput = cv.imread("images/raw_2_L.png", cv.IMREAD_GRAYSCALE)

cv.imshow('Image', detectFingers(imInput))
cv.waitKey(0)
cv.destroyAllWindows()