from numpy import array, zeros, exp, abs
from numpy.linalg import norm
import matplotlib.pyplot as plt


################################################## FUNCIONES #######################################################
# Función con el punto y la derivada
def Newton(F, x_0, Fp, tolerancia=1e-4, ):
    xn = x_0
    Error = tolerancia + 1 # Valor incial del error, grande
    
    
    if Fp == None:
        def FP():
            return
    
    
    while Error > tolerancia:
        xn1 = xn - F(xn)/Fp(xn)
        Error = abs(xn1 - xn)
        # print("xn =", xn, "xn1 - xn =", xn1 - xn)
        xn = xn1
        
    return xn


# Función que Newton aproximará
def jorge(x):
    return exp(x)  - 2 * x - 2

def jorgep(x):
    return exp(x)  - 2 * x

# Defición de la función partición
def partition(a, b, N):
    t = zeros(N + 1) 
    for i in range (0, N+1):
        t[i] = a + i * (b - a) / N # Esto es lo que hace el comando linspace
    return (t)


################################################### CÓDIGO #########################################################
# Llamadas
# solution = Newton(F=jorge, x_0=10, Fp=jorge, tolerancia=1e-8)
# print("La solución es:", solution)

# x = partition(a=0, b=10, N=100)
# y = jorge(x) # Esto se puede hacer porque hemos extraido la función de numpy, si se hubiera extraido de .mat no se podría hacer así, habría que ir punto a punto (pues no es vectorial)
# plt.plot(x, y)
# plt.show()

Sol = Newton(F=jorge, x_0=10, Fp=jorgep, tolerancia=1e-8)
print("La solución es:", Sol)
print ("Residual = ", jorge(Sol))