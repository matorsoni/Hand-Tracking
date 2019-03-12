import numpy as np

def norm(v):
    return np.sqrt( v[0][0]**2 + v[0][1]**2 )

def cosAngle(point, d1, d2):
    v1 = d1 - point
    v2 = d2 - point

    return np.sum(v1*v2) / (norm(v1) * norm(v2) )

def filterFingers(contour, defect):
    fingerIndices = []

    for i in range(len(defect)):
        j = i-1
        if j < 0:
            j = len(defect)-1

        # Coordinates of finger candidate and adoint defects
        point = contour[defect[i][0][0]]
        d1 = contour[defect[i][0][2]]
        d2 = contour[defect[j][0][2]]

        # Defect intensity of points d1 and d2
        di1 = defect[i][0][3]
        di2 = defect[j][0][3]

        # Threshold parameters
        fingerMaxAngle = 40
        minDefect = 3500 #7000

        if cosAngle(point, d1, d2) > np.cos(fingerMaxAngle*np.pi/180) and (di1 > minDefect or di2 > minDefect):
            fingerIndices.append( [defect[i][0][0] ] )

            # print(point, di1, di2)

    return np.array(fingerIndices)