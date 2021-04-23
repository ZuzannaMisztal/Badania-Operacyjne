import numpy as np

matrix = np.array([[20, -150, -250], 
                  [150, -80, -100],
                  [250, 100, 40]])

minA= [min(matrix[i]) for i in range (3)]
maxA = max(minA)
print("Minmax firmy A to", maxA, "dla decyzji nr", minA.index(maxA)+1)
     
maxB= [max(matrix[:,i]) for i in range (3)]
minB = min(maxB)
print("Minmax firmy B to", minB, "dla decyzji nr", maxB.index(minB)+1)