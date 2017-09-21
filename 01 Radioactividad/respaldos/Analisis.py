# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 23:16:46 2017

@author: Javier Alejandro Acevedo Barroso
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

rFondo = 0.416 #Conteos por segundo

a1 = np.loadtxt("lab1.txt", skiprows = 1)
a11 = np.loadtxt("lab11.txt", skiprows = 0)
a12 = np.loadtxt("lab12.txt")-rFondo*10 #Se le resta la radiación de fondo

print "Las medidas con un tiempo de 60 segundos y sin fuente: (n prom desv)"
print len(a1[:,0]), a1[:,0].mean(), a1[:,0].std()
print "\n"

print "Las medidas con un tiempo de 60 segundos y sin fuente para dir 1:"
print len(a1[:,1]), a1[:,1].mean(), a1[:,1].std()
print "\n"

print "Las medidas con un tiempo de 60 segundos y sin fuente para dir 2:"
print len(a1[:,2]), a1[:,2].mean(), a1[:,2].std()
print "\n"

print "Las medidas de radiación de fondo con 1s:"
print len(a1[:,3]), a1[:,3].mean(), a1[:,3].std()
print "\n"

print "Las medidas de radiación de fondo con 10s:"
print len(a11), a11.mean(), a11.std()
print "\n"

print "Las medidas para la camisa incandescente: n prom desv sqrt(prom)"
print len(a12), a12.mean(), a12.std(), np.sqrt(a12.mean())
print "\n"

a12m = a12.mean()
a12 = a12-a12m
a121 = 0.0
a122 = 0.0
for i in range(len(a12)):
    if(abs(a12[i])< a12.std()):
        a121 +=1
    if(abs(a12[i])< 2*a12.std()):
        a122 +=1
        

a121 = a121*100/len(a12)
a122 = a122*100/len(a12)

print "El porcentaje de datos que se encuentra entre 1 desviación es %.2f" %(a121)
print "El valor esperado era 68.3, la diferencia fue de %.2f porciento" %(a121 - 68.3)
print "\n"

print "El porcentaje de datos que se encuentra entre 2 desviaciones es %.2f" %(a122)
print "El valor esperado era 95.45, la diferencia fue de %.2f porciento" %(a122 - 95.45)
print "\n"

a12 = a12+a12m
h = plt.figure()
h12 = plt.hist(a12, bins = 15)
plt.xlabel("Conteos/10s")
plt.ylabel("Frecuencia")
plt.title("Histograma de conteos/10 para la camisa incandecente")
plt.savefig("histograma actividad 1.png")



#Actividad 2

def f(a,columna):
    return a[:,columna]

a2 = np.loadtxt("lab2.txt", skiprows = 1)
a2c = a2
print "\nActividad 2"
print "\nPara la actividad dos se posicionó las muestras a 8.6cm con 10s de medición. \n"
print "Para la muestra de Columbita: (alpha, beta, gamma, fondo)"
pFondo0 = 10*rFondo*100/f(a2, 0).mean()
pFondo1 = 10*rFondo*100/f(a2, 3).mean()
pFondo2 = 10*rFondo*100/f(a2, 6).mean()
a2 = a2-rFondo*10
g0 = 100*(a2[:,2].mean()/f(a2, 0).mean()) #Porcentaje de gamma de la radiación que NO ES RADIACIÓN DE FONDO
g0 = (100-pFondo0)*g0/100 #Porcentaje de gamma de la radiación medida por el GM.
b0 = 100*(f(a2, 1).mean()-f(a2,2).mean())/f(a2,0).mean()
b0 = (100-pFondo0)*b0/100   
al0 = 100*(f(a2,0).mean() - f(a2,1 ).mean())/f(a2,0).mean()
al0 = (100-pFondo2)*al0/100
print "%.2f %.2f %.2f %.2f   suma = %.2f\n" % (al0,b0,g0,pFondo0, al0+b0+g0+pFondo0)



g1 = 100*(a2[:,2+3].mean()/f(a2, 0+3).mean()) #Porcentaje de gamma de la radiación que NO ES RADIACIÓN DE FONDO
g1 = (100-pFondo1)*g1/100 #Porcentaje de gamma de la radiación medida por el GM.
b1 = 100*(f(a2, 1+3).mean()-f(a2,2+3).mean())/f(a2,0+3).mean()
b1 = (100-pFondo1)*b1/100   
al1 = 100*(f(a2,0+3).mean() - f(a2,1+3 ).mean())/f(a2,0+3).mean()
al1 = (100-pFondo2)*al1/100

print "Para la muestra de Cd-109: (alpha, beta, gamma, fondo)"
print "%.2f %.2f %.2f %.2f   suma = %.2f\n" % (al1,b1,g1,pFondo1, al1+b1+g1+pFondo1)


g2 = 100*(a2[:,2+6].mean()/f(a2, 0+6).mean()) #Porcentaje de gamma de la radiación que NO ES RADIACIÓN DE FONDO
g2 = (100-pFondo2)*g2/100 #Porcentaje de gamma de la radiación medida por el GM.
b2 = 100*(f(a2, 1+6).mean()-f(a2,2+6).mean())/f(a2,0+6).mean()
b2 = (100-pFondo2)*b2/100   
al2 = 100*(f(a2,0+6).mean() - f(a2,1+6 ).mean())/f(a2,0+6).mean()
al2 = (100-pFondo2)*al2/100
print "Para la muestra de Co-109: (alpha, beta, gamma, fondo)"
print "%.2f %.2f %.2f %.2f   suma = %.2f\n\n" % (al2,b2,g2,pFondo2, al2+b2+g2+pFondo2)
##
##


#Actividad 3

def prom1(distancia):
    distancia = (distancia - 3)*5
    return a3[distancia:distancia+5].mean()

def func(x, alpha,beta):
    return alpha*x+beta

a3 = np.loadtxt("lab3.txt", skiprows = 1)

for i in range(3,12):
    print "El promedio conteos para la distancia %d fue de %.1f" %(i,prom1(i))

dist = np.array([3,3,3,3,3,4,4,4,4,4,5,5,5,5,5,6,6,6,6,6,7,7,7,7,7,8,8,8,8,8,9,9,9,9,9,10,10,10,10,10,11,11,11,11,11])
rDist = 1.0/dist
#rDist = rDist*rDist

h1 = plt.figure()
reg = np.polyfit(rDist[10::], a3[10::],1)
plt.scatter(rDist[10::],a3[10::], color = 'r', label = "datos")
plt.plot(rDist[10::],func(rDist[10::], reg[0], reg[1]), label = "Regresion")
plt.xlabel("1/r^2 [cm^-2]")
plt.ylabel("Conteos")
plt.title("Conteo contra 1/r^2")
l1= plt.legend(loc='center left', bbox_to_anchor=(0.8, 0.5))
plt.savefig("regresion actividad 3.png",bbox_inches='tight')


def distAtenuacion(porcAtenuacion):
    return np.power( (porcAtenuacion*np.max(a3[10::]/100)-reg[1])/reg[0] ,-1/2 )

print "\n Al realizar la regresión lineal entre el conteo y 1/r^2 se obtuvo:"
print "Conteo = (%.2f) (1/r^2) + (%.2f)\n" % (reg[0],reg[1])

print "La distancia para una atenuación del 50%% es de %.2fcm." %(distAtenuacion(50))
print "La distancia para una atenuación del 10%% es de %.2fcm." %(distAtenuacion(10))

aPa10 = np.loadtxt("lab31.txt", skiprows =1)[:,0]
aPl10 = np.loadtxt("lab31.txt", skiprows =1)[:,1]

vGamma10 = aPl10.mean()
vBeta10 = (aPa10 - aPl10).mean()
vAlpha10 = prom1(10)-aPa10.mean()
vtotal10 = vGamma10 + vAlpha10+ vBeta10


plomo5 = np.loadtxt("lab5.txt", skiprows =1 )[:,1]
papel5 = np.loadtxt("lab5.txt",skiprows =1 )[:,6]
pNada5 = np.loadtxt("lab5.txt",skiprows =1 )[:,5]

porGamma5 = (plomo5.mean())/pNada5.mean()
porBeta5 = (papel5.mean() - plomo5.mean())/pNada5.mean()
porAlpha5 = (pNada5.mean()-papel5.mean())/pNada5.mean()

vGamma5 = porGamma5*func(1.0/5, reg[0],reg[1])
vBeta5 = porBeta5*func(1.0/5, reg[0],reg[1])
vAlpha5 = porAlpha5*func(1.0/5, reg[0],reg[1])
vtotal5 = vGamma5 + vAlpha5+ vBeta5

regAlpha = np.polyfit(np.array([1./5,1./10]), np.array([vAlpha5, vAlpha10]),1)
regBeta = np.polyfit(np.array([1./5,1./10]), np.array([vBeta5, vBeta10]),1)
regGamma = np.polyfit(np.array([1./5,1./10]), np.array([vGamma5, vGamma10]),1)

h2 = plt.figure()
plt.plot(rDist[10::],func(rDist[10::], regAlpha[0], regAlpha[1]), label = "Regresion para Alpha")
plt.scatter([1.0/5,1./10],[vAlpha5, vAlpha10], label ="Conteos de radiacion Alpha a 5cm y 10cm")
plt.plot(rDist[10::],func(rDist[10::], regBeta[0], regBeta[1]),label = "Regresion para Beta")
plt.scatter([1.0/5,1./10],[vBeta5, vBeta10], label = "Conteos de radiacion Beta a 5cm y 10cm")
plt.plot(rDist[10::],func(rDist[10::], regGamma[0], regGamma[1]),label = "Regresion para Gamma")
plt.scatter([1.0/5,1./10],[vGamma5, vGamma10], label = "Conteos de radiacion Gamma a 5cm y 10cm")
plt.xlabel("1/r^2 [cm^-2]")
plt.ylabel("Conteos")
plt.title("Conteos por 1/r^2 para distintos tipos de radiacion")
#plt.legend(loc=1)
l2= plt.legend(loc='center left', bbox_to_anchor=(0.5, 0.5))
plt.savefig("Atenuacion_aby",bbox_inches='tight')

print "\n Al realizar la regresión lineal con los datos para los distintos tipos de radiación, se obtuvo:"
print "Para radiación alpha: Conteo = (%.2f) (1/r^2) + (%.2f)\n" % (regAlpha[0],regAlpha[1])
print "Para radiación beta: Conteo = (%.2f) (1/r^2) + (%.2f)\n" % (regBeta[0],regBeta[1])
print "Para radiación gamma: Conteo = (%.2f) (1/r^2) + (%.2f)\n" % (regGamma[0],regGamma[1])



#Actividad 4.

a4 = np.loadtxt("lab4.txt", skiprows = 1)
theta = np.array([[-90.0,-90,-90,-90,-90],[-60,-60,-60,-60,-60],[-30,-30,-30,-30,-30],[0,0,0,0,0],[30,30,30,30,30],[60,60,60,60,60],[90,90,90,90,90]])*np.pi/180
a41 = a4[:,0:7] - 10*rFondo
a42 = a4[:,7:7+7] - 10*rFondo


h4 = plt.figure()
plt.scatter(a41[:,0].mean() *np.sin(theta[0,:]),a41[:,0].mean() *np.cos(theta[0,:] ), color = 'b', label = "Imanes paralelos")
plt.scatter(a42[:,0].mean() *np.sin(theta[0,:] ),a42[:,0].mean() *np.cos(theta[0,:] ), color = 'r', label = "Imanes antiparalelos")
for i in range(1,7):
    plt.scatter(a41[:,i].mean() *np.sin(theta[i,:] ),a41[:,i].mean() *np.cos(theta[i,:] ), color = 'b')
    plt.scatter(a42[:,i].mean() *np.sin(theta[i,:] ),a42[:,i].mean() *np.cos(theta[i,:] ), color = 'r')
plt.xlabel("Tasa de conteos/ 10s")
plt.ylabel("Tasa de conteos/ 10s")
plt.title("Conteos de acuerdo al angulo.")
l4= plt.legend(loc='center left', bbox_to_anchor=(0.8, 0.5))
plt.savefig("polarImanes.png",bbox_inches='tight')


aNoPlomoImanes = a4[:,14:16]-10*rFondo
aPlomoImanes = a4[:,16:18]-10*rFondo
aPlomoNoImanes = a4[:, 18:19]-10*rFondo
 
print "\n Actividad 4"
print "Con imanes se tuvo %.2f \pm %.2f conteos" %(aPlomoImanes.mean(), aPlomoImanes.std())
print "Sin imanes se tuvo %.2f \pm %.2f conteos" %(aPlomoNoImanes.mean(), aPlomoNoImanes.std())
#






#Actividad 5

a5= np.loadtxt("lab5.txt", skiprows = 1)-10*rFondo

al = a5[:,0] -10*rFondo
pl = a5[:,1]-10*rFondo
poly = a5[:,2]-10*rFondo
al2 = a5[:,3]-10*rFondo
plas = a5[:,4]-10*rFondo
sin =  a5[:,5]-10*rFondo
         
print"\n Actividad 5" 
print "Sin material de por medio se tuvieron %.2f \pm %.2f conteos\n" %(sin.mean(), sin.std())
print "Para el papel aluminio (A) se obtuvo %.2f \pm %.2f conteos, es decir una atenuacion del %.2f%%\n" %(al.mean(), al.std(), 100* ( (sin.mean() - al.mean() )/ sin.mean()))
print "Para el Plomo (S) se obtuvo %.2f \pm %.2f conteos, es decir una atenuacion del %.2f%%\n" %(pl.mean(), pl.std(), 100* ( (sin.mean() - pl.mean() )/ sin.mean()))
print "Para el Poliestireno (C) se obtuvo %.2f \pm %.2f conteos, es decir una atenuacion del %.2f%%\n" %(poly.mean(), poly.std(), 100* ( (sin.mean() - poly.mean() )/ sin.mean()))
print "Para el Plastico (E) se obtuvo %.2f \pm %.2f conteos, es decir una atenuacion del %.2f%%\n" %(plas.mean(), plas.std(), 100* ( (sin.mean() - plas.mean() )/ sin.mean()))
print "Para el Aluminio (P) se obtuvo %.2f \pm %.2f conteos, es decir una atenuacion del %.2f%%\n" %(al2.mean(), al2.std(), 100* ( (sin.mean() - al2.mean() )/ sin.mean()))


grosores = np.array([1,2,3,4,5,6,12,24])
papel= a5[:,6:6+8]
h6= plt.figure()
pMeans = np.array([1,1,1,1,1,1,1,1])
pStd = np.array([1,1,1,1,1,1,1,1])
pMeans[0] = papel[:,0].mean()
pStd[0] = papel[:,0].std()
plt.scatter(grosores[0], np.log(papel[:,0].mean()), color = 'r', label = "datos")
for i in range(1,8):
    pMeans[i] = papel[:,i].mean()
    pStd[i] = papel[:,i].std()
    plt.scatter(grosores[i], np.log(papel[:,i].mean()), color = 'r')
    

def aten(x,mu, I0):
    return I0*np.exp(-mu*x)




regPapel, std = curve_fit(aten, grosores,pMeans )
plt.plot(grosores, np.log(aten(grosores, regPapel[0], regPapel[1])), label ="Ajuste al modelo")
plt.xlabel("Numero de hojas")
plt.ylabel("Ln de conteos/10s")
plt.title("Atenuacion para el papel")
l8= plt.legend(loc='center left', bbox_to_anchor=(0.8, 0.5))
plt.savefig("atenuacionPapel.png",bbox_inches='tight')

print "Para la regresión del papel vs numero de hojas de obtuvo: (mu, I0):"
print "%.2f  %.2f" %(regPapel[0], regPapel[1])
print "Sin el papel se espera un promedio de " + str(regPapel[1])+ " conteos/10s"
print "Debe haber %.2f hojas para lograr una reducción del 50%%" %(   np.log((pMeans[0]/(regPapel[1]*2)))/(-regPapel[0]))



























