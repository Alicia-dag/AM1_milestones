from numpy import array, zeros, linspace, concatenate
from numpy.linalg import norm
import matplotlib.pyplot as plt

# KEPLER
def Kepler(U): #U = vector
    r = U[0:2]
    rdot = U[2:4]
    F = concatenate ( (rdot, -r/norm(r)**3), axis =0)
    
    return F


# Esquema EULER EXPLÍCITO
def Euler (F, U, dt, t):
    
    return U + dt * F(U,t)


# Problema CAUCHY: consiste en obtener la solución de un problema de CI dada una CI y un esquema temporal
# Imputs:
#           Esquema temporal
#           Función F(U,t)
#           Condición inicial
#           Partición temporal
# Output:
#           Solución para todo instante temporal y para todo componente

def Cauchy(Esquema, F, U0, t): 
    N = len(t)-1  # Por como se empieza a contar en Python
    U = zeros((N+1,len(U0)))
    
    U[0,:] = U0
    for n in range(0,N):
        U[n+1,:] = Esquema ( Kepler, U[n,:], t[n+1]-t[n], t[n] )
    return

# Esquema RUNGE-KUTTA órden 4
def RK4 (F, U, dt, t):
    k1 = F(U, t)
    k2 = F ( U + k1 * dt/2, t + dt/2)
    k3 = F ( U + k2 * dt/2, t + dt/2)
    k4 = F ( U + k3 * dt , t + dt/2)
    return



###### CÓDIGO ######

F_Euler[n,:] = Kepler(U_Euler[n,:])

U_Euler[n+1,:] = U_Euler[n,:] + (t[n+1]-t[n]) * F_Euler[n,:]


# Simplifica las dos líneas anteriores en una
U_Euler[n+1,:] = Euler (Kepler, U_Euler[n,:], dt, t[n]) 
#U_Euler[n+1,:] = Euler (F = Kepler, U = U_Euler[n,:], dt, t[n]) 

# Aplicando el CAUCHY
U_Euler = Cauchy (Euler, Kepler, U0, t)

# Aplicando el RK4
U_Euler = Cauchy (Euler, Kepler, U0, t)