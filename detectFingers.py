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
    allContours, _ = cv.findContours(imBinary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    imContours = imColor.copy()

    # Convexity analysis
    contours = []
    hulls = []
    defects = []
    fingers = []
    for contour in allContours:
        hullIndices = cv.convexHull(contour, None, False, False) # Calculate convex hulls
        hullIndices = filterHull(contour,hullIndices,8) # Clusters close points together

        defectList = cv.convexityDefects(contour, hullIndices) # Calculates convexity defects
        # print("Defects:", defectList)
        if defectList is not None:
            fingerIndices = filterFingers(contour, defectList) # Identifies which points are fingers
            # print("Fingers:", fingerIndices)
            if len(fingerIndices) >= 4:
                contours.append(contour)
                hulls.append(np.array( [contour[i[0]] for i in hullIndices] ) )
                defects.append(np.array( [contour[d[0][2] ] for d in defectList]) )
                fingers.append(np.array( [contour[i[0]] for i in fingerIndices] ) )


    # Sort finger order
    fingerList = []
    if len(fingers) == 1 and len(fingers[0]) == 5:
        fingerList = np.array(sorted(list(fingers[0]), key = lambda x: x[0][0] ) )
        # print(fingerList)

    # Drawings
    #cv.drawContours(imContours, contours, -1, (0,0,255), 2) # Hand contour
    cv.drawContours(imContours, hulls, -1, (0,255,0), 2) # Convex Hull
    # for hull in hulls:
    #     for point in hull:
    #         cv.circle(imContours,tuple(point[0]), 5, (255,255,0), 2) # Finger candidates
    for defect in defects:
        for point in defect:
            cv.circle(imContours,tuple(point[0]), 5, (255,0,255), 2) # Convex defects
    for finger in fingers:
        for point in finger:
            cv.circle(imContours,tuple(point[0]), 5, (255,0,0), 2) # Fingers

    return fingerList, imContours


# imInput = cv.imread("images/raw_1_L.png", cv.IMREAD_GRAYSCALE)

# cv.imshow('Image', detectFingers(imInput))
# cv.waitKey(0)
# cv.destroyAllWindows()
