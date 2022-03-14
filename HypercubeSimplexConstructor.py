# -*- coding: utf-8 -*-
"""
Created on Fri Feb 18 16:37:56 2022

@author: dtket
"""
#import pysal
import numpy as np      # if using numpy in cpython
import matplotlib.pyplot as plt
def Hypercube(M,iters):
    for i in range(iters):
        if (i > 0):
            M=FINAL
        m      = M.shape[0]
        I      = np.identity(m)
        TOP    = np.concatenate((M,I),axis=1)
        BOTTOM = np.concatenate((I,M),axis=1)
        FINAL  = np.concatenate((TOP,BOTTOM),axis=0)
    
    return FINAL

def Simplex(M,iters):
    for i in range(iters):
        if (i > 0):
            M=FINAL
        m      = M.shape[0]
        RIGHT  = np.ones((m,1))
        BOTTOM = np.ones((1,m+1))
        BOTTOM[0,m] = 0
        temp   = np.concatenate((M,RIGHT),axis=1)
        FINAL  = np.concatenate((temp,BOTTOM),axis=0)
    
    return FINAL
def MakeGrid(n):
   N = np.zeros([n,1])
   N[1]=1    
   offdi = la.toeplitz(N)
   I = np.eye(n)
   A = np.kron(offdi,I) + np.kron(I,offdi)
   return A
def MakeLine(n):
   N = np.zeros([n,1])
   N[1]=1    
   offdi = la.toeplitz(N)
   return offdi

def Normer(M):
    norms = np.linalg.norm(M,ord=1, axis=0)
    FINAL = M/norms
    return FINAL

def CalculateAbsorptionTimes(M,w):
    C=Normer(M)
    c  = C.shape[0]
    p = [*range(0, c, 1)]
#    w = c-1  #this controls which vertex is absorbing
    p[c-1] = w
    p[w] = c-1
    C[:,:] = C[p,:]
    C[:,:] = C[:,p]
    ONES = np.array(np.ones((c-1,1)))
    D=C[0:c-1,0:c-1]
    I = np.identity(c-1)
    X1=np.linalg.inv(I-D)
    AbsorptionTimes = np.dot(X1,ONES)
    return AbsorptionTimes
    

Point    = np.array([[0]])
Line     = Hypercube(Point,1)
#Line    = Simplex(Point,1)
Square   = Hypercube(Line,1)
Triangle = Simplex(Line,1)
SqPyr    = Simplex(Square,1)
TriPrism = Hypercube(Triangle,1)
Cube     = Hypercube(Square,1)
Tetrahed = Simplex(Triangle,1)
FourCell = Simplex(Tetrahed,1)
FourCube= Hypercube(Cube,1)

#plt.matshow(Hypercube(Point,6))
#plt.show()


A= MakeGrid(3)
#plt.matshow(A)
#plt.show()
B=nx.DiGraph(A)
nx.draw(B)
CalculateAbsorptionTimes(A,0)

a1 = max(max(CalculateAbsorptionTimes(Line,0)))
a2 = max(max(CalculateAbsorptionTimes(Square,0)))
a3 = max(max(CalculateAbsorptionTimes(Triangle,0)))
a4 = max(max(CalculateAbsorptionTimes(SqPyr,0)))
a5 = max(max(CalculateAbsorptionTimes(TriPrism,0)))
a6 = max(max(CalculateAbsorptionTimes(Cube,0)))
a7 = max(max(CalculateAbsorptionTimes(Tetrahed,0)))
a8 = max(max(CalculateAbsorptionTimes(FourCell,0)))
a9 = max(max(CalculateAbsorptionTimes(FourCube,0)))


MaxAbs=[a1,a2,a3,a4,a5,a6,a7,a8,a9]

print(MaxAbs)

#Shapes=[Line,Square,Triangle,SqPyr,TriPrism,Cube,Tetrahed,FourCell,FourCube]
#for shape in Shapes:
#    print(CalculateAbsorptionTimes(shape,0))
