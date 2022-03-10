# -*- coding: utf-8 -*-
"""
Created on Thu Feb 10 10:41:43 2022

@author: dtket
"""
import numpy as np      # if using numpy in cpython

def TDM(a, b, c, d):
    n = len(a)
    ac, bc, cc, dc = map(np.array, (a, b, c, d))
    xc = []
    for j in range(1, n):
        if(bc[j - 1] == 0):
            ier = 1
            return
        ac[j] = ac[j]/bc[j-1]
        bc[j] = bc[j] - ac[j]*cc[j-1]
    if(b[n-1] == 0):
        ier = 1
        return
    for j in range(1, n):
        dc[j] = dc[j] - ac[j]*dc[j-1]
    dc[n-1] = dc[n-1]/bc[n-1]
    for j in range(n-2, -1, -1):
        dc[j] = (dc[j] - cc[j]*dc[j+1])/bc[j]
    return dc

#test case
#
a = [-1/3,-2/3,-1]
b = [1,1,1]
c = [-1,-2/3,-1/3,0]
d = [1,1,1,1]
print(TDM(a,b,c,d))


#let n be the number of dimensions
for n in range(1,15):
    a = np.zeros(n)
    b = np.ones(n)
    c = np.zeros(n+1)
    d = np.ones(n+1)
    d[n]=0
    for i in range(0,n):
        a[i] = - i/n
        c[i] = -(n-i)/n
        
    print(TDM(a,b,c,d))    













