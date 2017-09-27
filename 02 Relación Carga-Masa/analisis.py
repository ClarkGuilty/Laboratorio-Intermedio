# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 18:34:46 2017

@author: Javier
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy import stats

data = np.loadtxt("a1.txt")
v = np.array(np.arange(100,275,25))
v1 = np.array(np.arange(150,300,25))



def vol(B2, alpha):
    return alpha*B2

def cm(alpha,r):
    return alpha*2.0/(r*r)



def camB(I, Re):
    return np.power(4.0/5.0, 3.0/2.0)* 4*np.pi*154*I/(10000*Re)

#La conversión a Teslas
def camBReal(I, Re):
    return np.power(4.0/5.0, 3.0/2.0)* 4*np.pi*154*I/(10000000*Re)




regI = np.polyfit(data[:,5], data[:,4],1)

regR,b = curve_fit(camB, data[:,5], data[:,4])
#R = 0.2
R = 0.2

slope, inter, r_val, sobra0,sobra1 = stats.linregress(np.power(camBReal(data[:,0], R),2), v)



def em(I, r, V):
    return 2*V/(np.power(camBReal(I, R)*r,2))

def em2(I, r, V):
    return 2*V/np.power((regI[0]*I+regI[1])*r/1000,2)

def err(I,r,V):
    return np.sqrt(np.power(4*V/(camBReal(I,R)*np.power(camBReal(I, R)*r,2))*(0.1)*np.power(4.0/5.0, 3.0/2.0)* 4*np.pi*154*I/(10000000*R),2)+ np.power(0.001*em(I,r,V)*2/r ,2)+ np.power(em(I,r,V)/V,2))


print "De la regresión lineal B = m I + b, se obtuvo %.2f, %.2f" %(regI[0], regI[1])
print "De la regresión entre B e I se obtuvo que el radio era de %.2f cm" %(regR[0]*100)

rta = np.array([], dtype = float)
for i in range(3):
    for j in range(7):
        rta = np.append(rta,em(data[j,i], (i+2.0)/100.0,25.0*j+100.0))

#for j in range(7):
#    rta = np.append(rta,em(data[j,3], 0.05,25.0*j+125.0))
    
rta2 = np.array([])
#rta2 = np.append(rta2,em(data[0,3], 0.05,25.0*0+125.0))
#print em(data[0,3], 0.05,25.0*0*+125.0)
rta2 = np.append(rta2,em(data[1,3], 0.05,25.0*1+125.0))
rta2 = np.append(rta2,em(data[2,3], 0.05,25.0*2+125.0))
rta2 = np.append(rta2,em(data[3,3], 0.05,25.0*3+125.0))
rta2 = np.append(rta2,em(data[4,3], 0.05,25.0*4+125.0))
rta2 = np.append(rta2,em(data[5,3], 0.05,25.0*5+125.0))
#print em(data[5,3], 0.05,25.0*5+125.0)
rta = np.append(rta,em(data[6,3], 0.05,25.0*6+125.0))
rta = np.concatenate((rta,rta2))
rta[14] = em(data[5,3], 0.05,25.0*5+125.0)
#for i in range(4):
#    for j in range(7):
#        if(rta[3*i+j] > 200000000000):
#            print rta[3*i+j],j,i
        #print data[j,i], rta[i*3+j], i,j
def suma(arr, i):
    rt = 0
    for i in range(i,i+7):
        rt = rt + arr[i]
    return rt
        
print rta.mean()/100000000000
radio = np.array([2,2,2,2,2,2,2,3,3,3,3,3,3,3,4,4,4,4,4,4,4,5,5,5,5,5,5])
rReal = radio/100.0
print "Radio (cm)& $e/m$  ($\\frac{C 10^{11}}{kg}) $  \\\\ \hline"
des = err(rta,rReal , np.array([100,125,150,175,200,225,250,100,125,150,175,200,225,250,100,125,150,175,200,225,250,150,175,200,225,250,275]))
for i in range(4):
#    print "%d & %.4f \\pm %.4f " %(radio[i*7], rta[i*7:7*i+7].mean()/100000000000, suma(des,i))
    print "%d & $%.4f \\pm %.4f$ \\\\ \\hline" %(radio[i*7], rta[i*7:7*i+7].mean()/100000000000, rta[i*7:7*i+7].std()/100000000000)


#h1 = plt.figure()    
#plt.scatter(data[:,5], data[:,4], label = "Teslametro")
#plt.plot(data[:,5], camB(data[:,5], regR[0]), color = 'r', label = "Modelo")
##plt.plot(data[:,5], camB(data[:,5], 0.2), color = 'g')
#plt.plot(data[:,5], regI[0]*data[:,5] + regI[1],color = 'g', label = "Regresion Lineal")    
#plt.xlabel("Corriente [A]")
#plt.ylabel("Campo Magnetico [mT]")
#plt.title("Campo Magnetico contra Corriente")
#l1= plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
#plt.savefig("B vs I",bbox_inches='tight')
    


a2,b2,c2,d2,f2 = stats.linregress(np.power(camBReal(data[:,0], R),2), v)
a3,b3,c3,d3,f3 = stats.linregress(np.power(camBReal(data[:,1], R),2), v)
a4,b4,c4,d4,f4 = stats.linregress(np.power(camBReal(data[:,2], R),2), v)
a5,b5,c5,d5,f5 = stats.linregress(np.power(camBReal(data[1:,3], R),2), v1)
#a2, b2 = np.polyfit(np.power(camBReal(data[:,0], R),2), v,1)
#a3, b3 = np.polyfit(np.power(camBReal(data[:,1], R),2), v,1)
#a4, b4 = np.polyfit(np.power(camBReal(data[:,2], R),2), v,1)
#a5, b5 = np.polyfit(np.power(camBReal(data[1:,3], R),2), v1,1)

g2, h2 = curve_fit(vol, np.power(camBReal(data[:,0],R),2), v)
g3, h3 = curve_fit(vol, np.power(camBReal(data[:,1],R),2), v)
g4, h4 = curve_fit(vol, np.power(camBReal(data[:,2],R),2), v)
g5, h5 = curve_fit(vol, np.power(camBReal(data[1:,3],R),2), v1)

#h = plt.figure()
#plt.scatter(np.power(camBReal(data[:,0]*1000, R),2), v, label = "r = 2cm")
#plt.plot(np.power(camBReal(data[:,0]*1000, R),2), a2*np.power(camBReal(data[:,0], R),2)+b2, label = "r = 2cm")
#plt.scatter(np.power(camBReal(data[:,1]*1000, R),2), v, label = "r = 3cm")
#plt.plot(np.power(camBReal(data[:,1]*1000, R),2), a3*np.power(camBReal(data[:,1], R),2)+b3, label = "r = 3cm")
#plt.scatter(np.power(camBReal(data[:,2]*1000, R),2), v, label = "r = 4cm")
#plt.plot(np.power(camBReal(data[:,2]*1000, R),2), a4*np.power(camBReal(data[:,2], R),2)+b4, label = "r = 4cm")
#plt.scatter(np.power(camBReal(data[1:,3]*1000, R),2), v1, label = "r = 5cm")
#plt.plot(np.power(camBReal(data[1:,3]*1000, R),2), a5*np.power(camBReal(data[1:,3], R),2)+b5, label = "r = 5cm")
#plt.xlabel("B^2 [(mT)^2]")
#plt.ylabel("Voltaje [V]")
#plt.title("V vs B^2 junto con su regresion lineal")
#l2= plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
#plt.savefig("VvsB2",bbox_inches='tight')
#    
caM1 = np.array([cm(a2,0.02)/100000000000,cm(a3,0.03)/100000000000,cm(a4,0.04)/100000000000,cm(a5,0.05)/100000000000])
caM2 = np.array([cm(g2[0],0.02)/100000000000,cm(g3[0],0.03)/100000000000,cm(g4[0],0.04)/100000000000,cm(g5[0],0.05)/100000000000])
caM2d = np.array([cm(np.sqrt(h2[0]),0.02)/100000000000,cm(np.sqrt(h3[0]),0.03)/100000000000,cm(np.sqrt(h4[0]),0.04)/100000000000,cm(2*np.sqrt(h5[0]),0.05)/100000000000])
print cm(a2,0.02)/100000000000,cm(a3,0.03)/100000000000,cm(a4,0.04)/100000000000,cm(a5,0.05)/100000000000
print c2,c3,c4,c5
print cm(g2[0],0.02)/100000000000,cm(g3[0],0.03)/100000000000,cm(g4[0],0.04)/100000000000,cm(g5[0],0.05)/100000000000
print caM1.mean(), caM2.mean(), caM2d.mean()
    


residuals2= v - vol(np.power(camBReal(data[:,0],R),2), h2)
ss_res2 = np.sum(residuals2**2)
ss_tot2 = np.sum((v-np.mean(v))**2)

print "Mean R :",  1-ss_res2/ss_tot2
    
#for i in range(7):
#    print "%.2f & %.2f \\\\ \\hline" % (data[i,4], data[i,5])
#    
#print "V = (%.0f)B^2 + %.0f" %(a2,b2 )
#print "V = (%.0f)B^2 + %.0f" %(a3,b3 )
#print "V = (%.0f)B^2 + %.0f" %(a4,b4 )
#print "V = (%.0f)B^2 + %.0f" %(a5,b5 )
    
    
    
    


