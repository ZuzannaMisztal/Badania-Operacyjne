import scipy.optimize as scipy
import scipy as sc
import numpy as np

A = np.array([[2,1,1,0,0,0,0],[1,2,1,3,2,1,0],[0,0,2,1,2,4,6]])
b = np.array([12000, 24000, 27000])
c = np.array([0,3,1,1,4,2,0])

A_dual = np.transpose(A)
b_dual = c*(-1)
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


A2 = [[2,1,1,0,0,0,0],[1,2,1,3,2,1,0],[0,0,2,1,2,4,6]]
A3 = []
for i in range(len(nierownosc_ostra)):
	if not nierownosc_ostra[i]:
		A3.append(A_dual[i])

A4 = np.array(A3)
A4 = np.transpose(A4)

Q, R = np.linalg.qr(A4)
x = sc.linalg.solve_triangular(R, Q.T.dot(b), lower=False)

j=0
for i in range(len(A[0])):
	print ("x"+str(i+1)+" = ", end="")
	if (nierownosc_ostra[i]):
		print("0")
	else:
		print(x[j])
		j+=1