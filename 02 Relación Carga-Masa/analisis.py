# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 18:34:46 2017

@author: Javier
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

data = np.loadtxt("a1.txt")
v = np.array(np.arange(100,275,25))
v1 = np.array(np.arange(125,300,25))



def vol(B2, alpha):
    return alpha*B2

def cm(alpha,r):
    return alpha*2.0/(r*r)

def heh(a,b,c):
    return a*a+b*b+c*c


def camB(I, Re):
    return np.power(4.0/5.0, 3.0/2.0)* 4*np.pi*154*I/(10000*Re)

#La conversión a Teslas
def camBReal(I, Re):
    return np.power(4.0/5.0, 3.0/2.0)* 4*np.pi*154*I/(10000000*Re)




regI = np.polyfit(data[:,5], data[:,4],1)

regR,b = curve_fit(camB, data[:,5], data[:,4])
R = 0.2

def em(I, r, V):
    return 2*V/(np.power(camBReal(I, R)*r,2))

def em2(I, r, V):
    return 2*V/np.power((regI[0]*I+regI[1])*r/1000,2)
#plt.scatter(data[:,5], data[:,4])
#plt.plot(data[:,5], camB(data[:,5], a[0]))
#plt.plot(data[:,5], regI[0]*data[:,5] + regI[1])

print "De la regresión lineal B = m I + b, se obtuvo %.2f, %.2f" %(regI[0], regI[1])
print "De la regresión entre B e I se obtuvo que el radio era de %.2f cm" %(regR[0]*100)

rta = np.array([])
for i in range(3):
    for j in range(7):
        rta = np.append(rta,em(data[j,i], (i+2.0)/100.0,25.0*j+100.0))


for i in range(3):
    for j in range(7):
        if(rta[3*i+j] > 200000000000):
            print rta[3*i+j],j,i
        #print data[j,i], rta[i*3+j], i,j
        
print rta[0:7].mean()/100000000000













