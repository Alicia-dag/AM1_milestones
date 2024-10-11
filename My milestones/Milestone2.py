from numpy import array, zeros, linspace, concatenate
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


# Simplifica las dos líneas anteriores en una
U_Euler[n+1,:] = Euler (Kepler, U_Euler[n,:], dt, t[n]) 
#U_Euler[n+1,:] = Euler (F = Kepler, U = U_Euler[n,:], dt, t[n]) 

# Aplicando el CAUCHY
U_Euler = Cauchy (Euler, Kepler, U0, t)

# Aplicando el RK4
U_Euler = Cauchy (Euler, Kepler, U0, t)



################################################# GRÁFICAS #########################################################
# Gráficas de las soluciones
plt.figure(figsize=(10, 6))
plt.plot(U_Euler[:, 0], U_Euler[:, 1], label="Euler Explícito", alpha=0.6)
plt.plot(U_RK4[:, 0], U_RK4[:, 1], label="Runge-Kutta 4 etapas", alpha=0.6)
plt.plot(U_CN[:, 0], U_CN[:, 1], label="Crank-Nickolson", alpha=0.6)
plt.legend()
plt.xlabel("x")
plt.ylabel("y")
plt.title("Solución de la EDO usando diferentes métodos numéricos")
plt.grid()
plt.show()