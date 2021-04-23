import scipy.optimize as scipy
import numpy as np

A = np.array([[0.5,0.4,0.4,0.2],[0.4,0.2,0.0,0.5]])
b = np.array([2000.,2800.])
c = np.array([10.,14.,8.,11.])

A_dual = np.transpose(A)
b_dual = c
c_dual = b


res = scipy.linprog(c_dual, A_dual*(-1), b_dual*(-1)).x
print("rozwiązanie dualne:")
print(res)

nierownosc_ostra = []
for i in range(len(A_dual)):
	if round(res[0]*A_dual[i][0]+res[1]*A_dual[i][1],2) == b_dual[i]:
		nierownosc_ostra.append(False)
	else:
		nierownosc_ostra.append(True)


A2 = [[1,3,2,3,1],[4,6,5,7,1]]
A3 = []
for i in range(len(nierownosc_ostra)):
	if not nierownosc_ostra[i]:
		A3.append(A_dual[i])

A4 = np.array(A3)
A4 = np.transpose(A4)

result = np.linalg.solve(A4, b)

j=0
for i in range(len(A[0])):
	print ("x"+str(i+1)+" = ", end="")
	if (nierownosc_ostra[i]):
		print("0")
	else:
		print(result[j])
		j+=1

