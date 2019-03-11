import numpy as np

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

def filterHull(contour, hullIndices, maxDist):
    indices = [i[0] for i in hullIndices] # Points to be trated
    
    # List of all partitions
    newIndices = []
    
    # While there are still points to be treated
    while len(indices) > 0:

        # Add first element
        p1 = indices.pop(0)
        partition = [p1]
        added = [p1]

        # Search elements that belong to same partition 
        while added:
            p1 = added.pop(0)
                   
            # Search all elements close to p1
            peers = []
            for p in indices:
                if dist(contour[p1],contour[p]) <= maxDist:
                    peers.append(p)
            
            added += peers
            partition += peers
            
            # Remove newly added points from original list
            for a in peers:
                removeArray(indices,a)
        
        meanPoint = np.mean(contour[partition],0)
        distances = [dist(meanPoint, contour[i]) for i in partition]
        # print(distances, np.argmin(distances))

        # Add partition to the list
        newIndices.append([partition[np.argmin(distances)] ] )

    return np.array(newIndices)