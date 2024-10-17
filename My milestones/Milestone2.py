from numpy import array, zeros, linspace, concatenate, float64
from numpy.linalg import norm
import matplotlib.pyplot as plt


#################################################### DATOS ########################################################
# Condiciones iniciales
x0 = 1.0
y0 = 0.0
vx0 = 0.0
vy0 = 1.0

# Instantes inicial, final y paso del tiempo
t0 = 0.0
tf = 10.0
dt = 0.01

# Número de intervalos (= nº de instantes de tiempo - 1)
N = int((tf - t0) / dt)


################################################# FUNCIONES #######################################################
# KEPLER
def Kepler(U): #U = vector
    r = U[0:2]
    rdot = U[2:4]
    F = concatenate ( (rdot, -r/norm(r)**3), axis =0)
    
    return F

# def Kepler(U, t): 

#     x = U[0]; y = U[1]; dxdt = U[2]; dydt = U[3]
#     d = ( x**2  +y**2 )**1.5

#     return  array( [ dxdt, dydt, -x/d, -y/d ] ) 


# Esquema EULER EXPLÍCITO
def Euler (F, U, dt, t):
    
    return U + dt * F(U,t)


# Problema CAUCHY: consiste en obtener la solución de un problema de CI dada una CI y un esquema temporal
def Cauchy_problem(F, t, U0, Esquema):  
    N =  len(t)-1
    Nv = len(U0)
    #U = zeros( (N+1, Nv), dtype=type(U0) )
    U = zeros( (N+1, Nv), dtype=float64 ) 
    U[0,:] = U0
    
    for n in range(N): 
        U[n+1,:] = Esquema( U[n, :], t[n+1] - t[n], t[n],  F ) 
    return U



# Esquema RUNGE-KUTTA órden 4
def RK4 (F, U, dt, t):
    k1 = F(U, t)
    k2 = F ( U + k1 * dt/2, t + dt/2)
    k3 = F ( U + k2 * dt/2, t + dt/2)
    k4 = F ( U + k3 * dt , t + dt/2)
    U[n+1, :] = k1 + k2 + k3 + k4
    return U

################################################### CÓDIGO ########################################################
# Inicializamos el vector de intantes temporales en los que se calcula la solución
t_values = linspace(t0, tf, N)
n = len(t_values)

# Vector de condiciones iniciales
U0 = array ([x0, y0, vx0, vy0])

# Matrices de soluciones
U_Euler = zeros((n,4))
U_Euler[0] = U0 
F_Euler = zeros(4)

# Llamadas
F_Euler[n,:] = Kepler(U_Euler[n,:])
U_Euler[n+1,:] = U_Euler[n,:] + dt * F_Euler[n,:]


