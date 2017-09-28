# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 20:54:24 2017

@author: Javier Alejandro Acevedo Barroso
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

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

def hi(pend,d):
    return d*np.sqrt(2*m*e)*pend/(2*L)

print "Voltaje [kV] & \lambda_{deBroglie} [pm]&\lambda_{Bragg}_1 [pm] & Error \% & \lambda_{Bragg}_2 [pm] & Error \% \\\\ \\hline"
for i in range(7):
    lb1 = lbrag1((data[i,3])/100.0,d1)*1e12
    lbo = lbrog(data[i,0]*1000)*1e12
    lb2 = lbrag2((data[i,4])/100, d2)*1e12
    print "%.1f &%.3f & $%.3f & %.3f  & %.3f & %.3f \\\\ \\hline" %(data[i,0],lbo,lb1, 100*np.abs(lbo-lb1)/lbo, lb2, np.abs(lbo-lb2)/lbo*100)






#reg1 = np.polyfit((np.power(data[:,0]*1000,-0.5)), data[:,3]/100,1)
#reg2 = np.polyfit((np.power(data[:,0]*1000,-0.5)), data[:,4]/100,1)

qw1,qw2,qw3,qw4,qw5 = stats.linregress((np.power(data[:,0]*1000,-0.5)), data[:,3]/100)
ew1,ew2,ew3,ew4,ew5 = stats.linregress((np.power(data[:,0]*1000,-0.5)), data[:,4]/100)

#print qw1,qw2,qw3,qw4,qw5
#print ew1,ew2,ew3,ew4,ew5

print "%.4f, %.5f, %.5f" % (qw1,qw2,qw3)
print "%.4f, %.5f, %.5f" % (ew1,ew2,ew3)

print di(qw1)*1e12
print di(ew1)*1e12

print ""
print hi(qw1,d1)
print hi(ew1,d2)
print str(hi(qw1,d1)/2.0+hi(ew1,d2)/2.0)

#        
fig0 = plt.figure()
plt.scatter(np.power(data[:,0]*1000,-0.5), data[:,3]/100, color = 'g', label = "Datos D Interior ")
plt.scatter(np.power(data[:,0]*1000,-0.5), data[:,4]/100, color = 'r', label = "Datos D exterior")
plt.scatter([0],[0], color = 'black')
nuevo = np.array(np.append([0],np.power(data[:,0]*1000,-0.5)))
plt.plot(nuevo, qw1*nuevo+qw2, label = "Regresion D interno")
plt.plot(nuevo, ew1*nuevo+ew2)

l1= plt.legend(loc='center left', bbox_to_anchor=(0.8, 0.5))
plt.savefig("rvsU.png",bbox_inches='tight')














