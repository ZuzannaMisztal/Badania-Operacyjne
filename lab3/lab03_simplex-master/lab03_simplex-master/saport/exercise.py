import numpy as np

arr = np.array([-8, -9, 0, 0, 0])
result = np.where(arr == min(arr))
print(result[0][0])