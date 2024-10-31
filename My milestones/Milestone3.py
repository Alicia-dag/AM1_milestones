from numpy import array, zeros, linspace, concatenate, float64, pi
import matplotlib.pyplot as plt
from numpy.linalg import norm
from scipy.optimize import newton # Import Newton Method



#################################################### DATOS ########################################################
# Condiciones iniciales
x0 = 1.
y0 = 0.
vx0 = 0.
vy0 = 1.

# Variables de tiempo y número de intervalos 
tf = 7
N = 2000


################################################# FUNCIONES #######################################################
# KEPLER
def Kepler(U, t): 
    x = U[0]; y = U[1]; dxdt = U[2]; dydt = U[3]
    d = ( x**2  +y**2 )**1.5
    F =  array( [ dxdt, dydt, -x/d, -y/d ] ) 
    return  F


# OSCILADOR
def Oscilador(U, t): 
    x = U[0]; 
    xdot = U[1]
    F = array([xdot, -x])
    return F


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


# Refinación de malla: dada la partición t1 (con N+1 puntos), obtiene la partición t2 (que tiene 2N+1 puntos)
# Los nodos pares de t2 seguirán siendo los mismos que los de t1, y los nodos impares serán los puntos medios de los intervalos de t1
def mesh_refinement(t1): # Cada función define las cosas como quiera, se puede repetir nomenclatura
    N = len(t1) - 1
    t2 = zeros(2*N + 1)
    for i in range(N + 1): # Recordar que el range es [), por eso va hasta N+1]
        t2[2*i] = t1[i] # Nodos pares
        t2[2*i+1] = (t1[i+1] -  t1[i]) / 2 # Nodos impares
    t2[2*N] = t1[N] # Se añade el último nodo, hay que añadirlo a mano. IMPORTANTE
    return t2


# Defición de la función partición para un caso genérico
def partition(a, b, N):
    t = zeros(N + 1) 
    for i in range (0, N+1):
        t[i] = a + i * (b - a) / N # Esto es lo que hace el comando linspace
    return (t)

# Extrapolación de Richardson
def Cauchy_error(F, t, U0, Esquema):
    N = len(t) - 1
    a = t[0]
    b = t[N]
    
    Error = zeros((N+1, len(U0)))
    
    t1 = t
    t2 = partition (a, b, 2*N)
    
    U_1 = Cauchy_problem (F, t1, U0, Esquema) # Solución del problema de Cauchy_problem con la malla original
    U_2 = Cauchy_problem (F, t2, U0, Esquema) # Solución del problema de Cauchy_problem con la malla modificada (más fina), es decir, con una malla refinada
    
    # Para calcular el error se hace la resta, pero un vector no se puede restar de otro si uno mide N+1 y el otro N, por eso se hace la resta en los nodos pares
    for i in range (0, N+1): 
        Error[i, :] = U_2[2*i, :] - U_1[i, :] # en este caso los dos puntitos significan: para todas las variables
        
    return U_1, Error


################################################### CÓDIGO ########################################################
# Separación equiespaciada de instantes de tiempo en los que calcular la solución
t1 = partition(a = 0, b = 20*pi, N = 1000) # a es el tiempo inicial, b es el tiempo final, N es el número de intervalos

# Llamadas
U0 = array([1, 0])
U_E, Error_E = Cauchy_error(Oscilador, t1, array([1, 0]), Euler)
U_RK4, Error_RK4 = Cauchy_error(Oscilador, t1, array([1, 0]), RK4)
U_CN, Error_CN = Cauchy_error(Oscilador, t1, array([1, 0]), Crank_Nickolson)
U_EI, Error_EI = Cauchy_error(Oscilador, t1, array([1, 0]), Euler_Inverso)

# # Verificación de que linspace y partition NO es lo mismo, lo mismo sería con linspace(a, b, N+1)
# a, b = 0, 1
# N = 100
# t = linspace(a, b, N)
# print ("t1 = ", t)
# t = partition(a, b, N)
# print ("t2 = ", t)

# t1 = partition (a, b, N)
# print ("t1 = ", t1)
# t2 = partition (a, b, N)
# print ("t2 = ", t2)

################################################# GRÁFICAS #########################################################
# Gráfica de las todas soluciones
plt.plot(t1, U_E[:, 0], label="Euler")
plt.plot(t1, U_RK4[:, 0], label="RK4")
plt.plot(t1, U_CN[:, 0], label="Crank-Nickolson")
plt.plot(t1, U_EI[:, 0], label="Euler Inverso")
plt.plot(t1, Error_E[:, 0],  label="Error Euler")
plt.plot(t1, Error_RK4[:, 0],  label="Error RK4")
plt.plot(t1, Error_CN[:, 0],  label="Error CN")
plt.plot(t1, Error_EI[:, 0],  label="Error EI")
plt.legend()
plt.xlabel("t")
plt.show()

# Gráfica de Euler y su error
plt.plot(t1, U_E[:, 0], label="Euler")
plt.plot(t1, Error_E[:, 0],  label="Error Euler")
plt.legend()
plt.xlabel("t")
plt.show()

# Gráfica de RK4 y su error
plt.plot(t1, U_RK4[:, 0], label="RK4")
plt.plot(t1, Error_RK4[:, 0],  label="Error RK4")
plt.legend()
plt.xlabel("t")
plt.show()

# Gráfica de Crank-Nickolson y su error
plt.plot(t1, U_CN[:, 0], label="Crank-Nickolson")
plt.plot(t1, Error_CN[:, 0],  label="Error CN")
plt.legend()
plt.xlabel("t")
plt.show()

# Gráfica de Euler Inverso y su error
plt.plot(t1, U_EI[:, 0], label="Euler Inverso")
plt.plot(t1, Error_EI[:, 0],  label="Error EI")
plt.legend()
plt.xlabel("t")
plt.show()