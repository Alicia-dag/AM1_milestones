# Como el milestone 3 pero con la parte de diferencia entre partition y linspace 
from numpy import array, zeros, linspace, concatenate, float64, pi
import matplotlib.pyplot as plt
from numpy.linalg import norm
from scipy.optimize import newton # Import Newton Method
from Modules.Physics import Kepler, Oscilador
from Modules.NumericalSchemes import Euler, RK4, Crank_Nickolson, Euler_Inverso
from Modules.Functions import Mesh_Refinement, Partition, Problem_Error, Problem_Error_Convergencia, Convergencia
from Modules.CauchyProblem import Cauchy_problem



#################################################### DATOS ########################################################
# Condiciones iniciales
x0 = 1.
y0 = 0.
vx0 = 0.
vy0 = 1.
U0 = array([x0, y0, vx0, vy0])

# Variables de tiempo y número de intervalos 
tf = 7
N = 2000


################################################# FUNCIONES #######################################################
# Extrapolación de Richardson
def Cauchy_error(F, t, U0, Esquema):
    N = len(t) - 1
    a = t[0]
    b = t[N]
    
    Error = zeros((N+1, len(U0)))
    
    t1 = t
    t2 = Partition (a, b, 2*N)
    
    U_1 = Cauchy_problem (F, t1, U0, Esquema) # Solución del problema de Cauchy_problem con la malla original
    U_2 = Cauchy_problem (F, t2, U0, Esquema) # Solución del problema de Cauchy_problem con la malla modificada (más fina), es decir, con una malla refinada
    
    # Para calcular el error se hace la resta, pero un vector no se puede restar de otro si uno mide N+1 y el otro N, por eso se hace la resta en los nodos pares
    for i in range (0, N+1): 
        Error[i, :] = U_2[2*i, :] - U_1[i, :] # en este caso los dos puntitos significan: para todas las variables
        
    return U_1, Error


################################################### CÓDIGO ########################################################
# Separación equiespaciada de instantes de tiempo en los que calcular la solución
t1 = Partition(a = 0, b = 20*pi, N = 1000) # a es el tiempo inicial, b es el tiempo final, N es el número de intervalos
# t0 = 0
# t = linspace(t0, tf, N+1)

# Llamadas
U0 = array([1, 0])
U_E, Error_E = Cauchy_error(Oscilador, t1, array([1, 0]), Euler)
U_RK4, Error_RK4 = Cauchy_error(Oscilador, t1, array([1, 0]), RK4)
U_CN, Error_CN = Cauchy_error(Oscilador, t1, array([1, 0]), Crank_Nickolson)
U_EI, Error_EI = Cauchy_error(Oscilador, t1, array([1, 0]), Euler_Inverso)

# # Verificación de que linspace y Partition NO es lo mismo, lo mismo sería con linspace(a, b, N+1)
# a, b = 0, 1
# N = 100
# t = linspace(a, b, N)
# print ("t1 = ", t)
# t = Partition(a, b, N)
# print ("t2 = ", t)

# t1 = Partition (a, b, N)
# print ("t1 = ", t1)
# t2 = Partition (a, b, N)
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