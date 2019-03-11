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

        point = contour[defect[i][0][0]]
        d1 = contour[defect[i][0][2]]
        d2 = contour[defect[j][0][2]]

        if cosAngle(point, d1, d2) > 0.8:
            fingerIndices.append( [defect[i][0][0] ] )

    return np.array(fingerIndices)