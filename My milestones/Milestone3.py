from numpy import array, zeros, pi
import matplotlib.pyplot as plt
from Modules.Physics import Kepler, Oscilador
from Modules.NumericalSchemes import Euler, RK4, Crank_Nickolson, Euler_Inverso
from Modules.Functions import Mesh_Refinement, Partition, Schemes_error, Convergence
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



################################################### CÓDIGO ########################################################
# Separación equiespaciada de instantes de tiempo en los que calcular la solución
t1 = Partition(a = 0, b = 20*pi, N = 1000)

# Error
U0 = array([1, 0])
U_E, Error_E = Schemes_error(U0, Oscilador, Cauchy_problem, Euler, t1)
U_RK4, Error_RK4 = Schemes_error(U0, Oscilador, Cauchy_problem, RK4, t1)
U_CN, Error_CN = Schemes_error(U0, Oscilador, Cauchy_problem, Crank_Nickolson, t1)
U_EI, Error_EI = Schemes_error(U0, Oscilador, Cauchy_problem, Euler_Inverso, t1)

# Convergencia
logN_E, logE_E = Convergence(U0, Oscilador, Schemes_error, Cauchy_problem, Euler, t1)
logN_RK4, logE_RK4 = Convergence(U0, Oscilador, Schemes_error, Cauchy_problem, RK4, t1)
logN_CN, logE_CN = Convergence(U0, Oscilador, Schemes_error, Cauchy_problem, Crank_Nickolson, t1)
logN_EI, logE_EI = Convergence(U0, Oscilador, Schemes_error, Cauchy_problem, Euler_Inverso, t1)

plt.axis('equal') 
plt.xlabel('logN')
plt.ylabel('logE')
plt.plot(logN_E, logE_E, '-b')
plt.show()

################################################# GRÁFICAS #########################################################
# # Gráfica de las todas soluciones
# plt.plot(t1, U_E[:, 0], label="Euler")
# plt.plot(t1, U_RK4[:, 0], label="RK4")
# plt.plot(t1, U_CN[:, 0], label="Crank-Nickolson")
# plt.plot(t1, U_EI[:, 0], label="Euler Inverso")
# plt.plot(t1, Error_E[:, 0],  label="Error Euler")
# plt.plot(t1, Error_RK4[:, 0],  label="Error RK4")
# plt.plot(t1, Error_CN[:, 0],  label="Error CN")
# plt.plot(t1, Error_EI[:, 0],  label="Error EI")
# plt.legend()
# plt.xlabel("t")
# plt.show()

# # Gráfica de Euler y su error
# plt.plot(t1, U_E[:, 0], label="Euler")
# plt.plot(t1, Error_E[:, 0],  label="Error Euler")
# plt.legend()
# plt.xlabel("t")
# plt.show()

# # Gráfica de RK4 y su error
# plt.plot(t1, U_RK4[:, 0], label="RK4")
# plt.plot(t1, Error_RK4[:, 0],  label="Error RK4")
# plt.legend()
# plt.xlabel("t")
# plt.show()

# # Gráfica de Crank-Nickolson y su error
# plt.plot(t1, U_CN[:, 0], label="Crank-Nickolson")
# plt.plot(t1, Error_CN[:, 0],  label="Error CN")
# plt.legend()
# plt.xlabel("t")
# plt.show()

# # Gráfica de Euler Inverso y su error
# plt.plot(t1, U_EI[:, 0], label="Euler Inverso")
# plt.plot(t1, Error_EI[:, 0],  label="Error EI")
# plt.legend()
# plt.xlabel("t")
# plt.show()

# # Gráfica de convergencia de Euler
#     plt.plot(logN_E, logE_E, '-b')
#     plt.axis('equal') 
#     plt.xlabel('logN_E')
#     plt.ylabel('logE_E')
#     plt.show()

# # Gráfica de convergencia de RK4
#     plt.plot(logN_RK4, logE_RK4, '-b')
#     plt.axis('equal') 
#     plt.xlabel('logN_RK4')
#     plt.ylabel('logE_RK4')
#     plt.show()
    
# # Gráfica de convergencia de Cranck-Nickolson
#     plt.plot(logN_CN, logE_CN, '-b')
#     plt.axis('equal') 
#     plt.xlabel('logN_CN')
#     plt.ylabel('logE_CN')
#     plt.show()

# # Gráfica de convergencia de Euler Inverso
#     plt.plot(logN_E, logE_E, '-b')
#     plt.axis('equal') 
#     plt.xlabel('logN_EI')
#     plt.ylabel('logE_EI')
#     plt.show()