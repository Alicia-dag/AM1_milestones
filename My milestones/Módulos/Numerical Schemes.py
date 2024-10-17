from numpy import array, zeros, linspace, concatenate
from numpy.linalg import norm


# EULER EXPLÍCITO
def Euler (F, U, dt, t):
    
    return U + dt * F(U,t)


# RUNGE-KUTTA órden 4
def RK4 (F, U, dt, t):
    k1 = F(U, t)
    k2 = F ( U + k1 * dt/2, t + dt/2)
    k3 = F ( U + k2 * dt/2, t + dt/2)
    k4 = F ( U + k3 * dt , t + dt/2)
    return