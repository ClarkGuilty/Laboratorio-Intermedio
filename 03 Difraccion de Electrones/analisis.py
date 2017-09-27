# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 20:54:24 2017

@author: Javier Alejandro Acevedo Barroso
"""

import numpy as np
import matplotlib.pyplot as plt

data0 = np.loadtxt("m-c1.txt")
data = np.loadtxt("m-c2.txt")

L = 13.5/100
h = 6.62607004e-34
m = 9.10938291e-31
e = 1.60217656e-19
d1 = 213e-12
d2 = 123e-12

def lbrag1 (D, d):
    at = np.arctan(D/(2.0*L))
    return 2.0*d*np.sin(at/2.0)

def lbrag2 (D, d):
    at = np.arctan(D/(2.0*L))
    return 2*d*np.sin(at/2.0)

def lbrog(U):
    return h/np.sqrt(2*m*e*U)

def di(pend):
    return 2*h*L/(pend*np.sqrt(2*m*e))


print "Voltaje [kV] & \lambda_{deBroglie} [pm]&\lambda_{Bragg}_1 [pm] & Error \% & \lambda_{Bragg}_2 [pm] & Error \% \\\\ \\hline"
for i in range(7):
    lb1 = lbrag1((data[i,3])/100.0,d1)*1e12
    lbo = lbrog(data[i,0]*1000)*1e12
    lb2 = lbrag2((data[i,4])/100, d2)*1e12
    print "%.1f &%.3f & $%.3f & %.3f  & %.3f & %.3f \\\\ \\hline" %(data[i,0],lbo,lb1, 100*np.abs(lbo-lb1)/lbo, lb2, np.abs(lbo-lb2)/lbo*100)






reg1 = np.polyfit((np.power(data[:,0]*1000,-0.5)), data[:,3]/100,1)
reg2 = np.polyfit((np.power(data[:,0]*1000,-0.5)), data[:,4]/100,1)


print reg1
print reg2

print di(reg1[0])*1e12
print di(reg2[0])*1e12

        
#        
#fig0 = plt.figure()
#plt.scatter(np.power(data[:,0]*1000,-0.5), data[:,3]/100)
#plt.scatter(np.power(data[:,0]*1000,-0.5), data[:,4]/100, color = 'r')
#plt.scatter([0],[0], color = 'black')
#nuevo = np.array(np.append([0],np.power(data[:,0]*1000,-0.5)))
#plt.plot(nuevo, reg1[0]*nuevo+reg1[1])
#plt.plot(nuevo, reg2[0]*nuevo+reg2[1])
#
