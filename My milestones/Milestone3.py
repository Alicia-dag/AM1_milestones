from numpy import array, zeros, linspace, concatenate, float64
import matplotlib.pyplot as plt
from scipy.optimize import newton # Import Newton Method



#################################################### DATOS ########################################################



################################################# FUNCIONES #######################################################
# KEPLER
def Kepler(U, t): 

    x = U[0]; y = U[1]; dxdt = U[2]; dydt = U[3]
    d = ( x**2  +y**2 )**1.5

    return  array( [ dxdt, dydt, -x/d, -y/d ] ) 


# Problema CAUCHY
def Cauchy_problem(F, t, U0, Esquema):  
    N =  len(t)-1
    Nv = len(U0)
    U = zeros( (N+1, Nv), dtype=float64 ) 
    U[0,:] = U0
    
    for n in range(N): 
        U[n+1,:] = Esquema( U[n, :], t[n+1] - t[n], t[n],  F ) 
    return U


# Esquema EULER EXPLÍCITO
def Euler (U, dt, t, F):
    
    return U + dt * F(U, t)


# Esquema RUNGE-KUTTA órden 4
def RK4 (U, dt, t, F):
    k1 = F (U, t)
    k2 = F ( U + k1 * dt/2, t + dt/2)
    k3 = F ( U + k2 * dt/2, t + dt/2)
    k4 = F ( U + k3 * dt , t + dt/2)
    return U + (dt/6) * (k1 + 2*k2 + 2*k3 + k4)


# Esquema implícito CRANK-NICKOLSON
def Crank_Nickolson(U, dt, t, F): 
    def G(X):
        return X - U - dt/2 * (F(X, t) + F(U, t))
    return newton(G, U)


# Esquema implícito EULER IMPLÍCITO
def Euler_Inverso(U, dt, t, F): 
    def G(X):
        return X - U - dt * F(X, t)
    return newton(G, U)


def Richardson(U, dt, t, F): #Extrapolación de Richardson
    U1 = Euler(U, dt/2, t, F)
    U2 = Euler(U1, dt/2, t, F)
    return U2 + (U2 - U1)/15



################################################### CÓDIGO ########################################################



################################################# GRÁFICAS #########################################################
# Gráficas de las soluciones