from numpy import array, zeros, linspace, pi, log10, polyfit 
from numpy.linalg import norm
import matplotlib.pyplot as plt
from Modules.Physics import Kepler, Oscilador
from Modules.NumericalSchemes import Euler, RK4, Crank_Nickolson, Euler_Inverso
from Modules.Functions import Mesh_Refinement, Partition
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
# ERROR DE CONVERGENCIA DE LOS ESQUEMAS NUMÉRICOS: Extrapolación de Richardson
def Schemes_error(U0, F, Problema, Esquema, t):
    '''''''''''
    INPUTS:
        - U0: vector de condiciones iniciales
        - F(U,t): función a resolver
        - Esquema(U, F, t): función que representa el esquema numérico a utilizar
        - Problema(Esquema, F, U0, t): Función que representa el problema a resolver (Cauchy hasta el momento)
        - t: partición temporal 
    '''''''''''
    
    N = len(t) - 1
    a = t[0]
    b = t[N]
    
    Error = zeros((N+1, len(U0)))
    
    t1 = t
    t2 = Partition (a, b, 2*N)
    
    U_1 = Problema (F, t1, U0, Esquema) # Solución del problema (hasta ahora de Cauchy) con la malla original
    U_2 = Problema (F, t2, U0, Esquema) # Solución del problema (hasta ahora de Cauchy) con la malla modificada (más fina), es decir, con una malla refinada
    
    # Para calcular el error se hace la resta, pero un vector no se puede restar de otro si uno mide N+1 y el otro N, por eso se hace la resta en los nodos pares
    for i in range (0, N+1): 
        Error[i, :] = U_2[2*i, :] - U_1[i, :] # en este caso los dos puntitos significan: para todas las variables
        
    return U_1, Error




# CONVERGENCIA DE LOS ESQUEMAS NUMÉRICOS
def Convergence(U0, F, Error, Problema, Esquema, t):
    '''''''''''
    INPUTS:
        - U0: Vector del estado inicial
        - F: Función a resolver
        - Error(U0, F, Problema, Esquema, t): Función que devuelve un vector con el error de un esquema en cada paso temporal
        - Esquema: Esquema temporal a resolver
        - t: partición temporal
    OUTPUTS:
        - logN:  vector for the different number of time partitions 
        - logE:  error for each time partition      
        - Order:  order of Error of the temporal scheme 
    '''''''''''
    
    np = 6  # Número de puntos de la regresión, si se sube más tarda MUCHO en converger
    logE = zeros(np)
    logN = zeros(np)
    N = len(t) - 1
    t1 = t
    
    for i in range(np):
        U, Er = Error(U0, F, Problema, Esquema, t1)  # Asumiendo que Error devuelve U_1 y Error
        logE[i] = log10 ( norm( Er[N, :]  ) ) 
        logN[i] = log10( float(N) )
        N = 2*N
        t1 = linspace(t[0], t[-1], N+1)  
        
    y = logE[ logE > -12 ]
    x = logN[ 0:len(y) ]
    Order, b = polyfit(x, y, 1) # Regresión lineal para encontrar la pendiente de la recta que mejor se ajusta a los datos
    # print("Order =", Order, "b =", b)
    return logN, logE, Order


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
logN_E, logE_E, Order_E = Convergence(U0, Oscilador, Schemes_error, Cauchy_problem, Euler, t1)
logN_RK4, logE_RK4, Order_RK4 = Convergence(U0, Oscilador, Schemes_error, Cauchy_problem, RK4, t1)
logN_CN, logE_CN, Order_CN = Convergence(U0, Oscilador, Schemes_error, Cauchy_problem, Crank_Nickolson, t1)
logN_EI, logE_EI, Order_EI = Convergence(U0, Oscilador, Schemes_error, Cauchy_problem, Euler_Inverso, t1)
print ("Order Euler =", Order_E)
print ("Order RK4 =", Order_RK4)
print ("Order CN =", Order_CN)
print ("Order EI =", Order_EI)

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
plt.title("Soluciones de todos los esquemas numéricos y sus errores")
plt.legend()
plt.xlabel("t")
plt.show()

# Gráfica de Euler y su error
plt.plot(t1, U_E[:, 0], label="Euler")
plt.plot(t1, Error_E[:, 0],  label="Error Euler")
plt.title("Solución del esquema de Euler y su error")
plt.legend()
plt.xlabel("t")
plt.show()

# Gráfica de RK4 y su error
plt.plot(t1, U_RK4[:, 0], label="RK4")
plt.plot(t1, Error_RK4[:, 0],  label="Error RK4")
plt.title("Solución del esquema de RK4 y su error")
plt.legend()
plt.xlabel("t")
plt.show()

# Gráfica de Crank-Nickolson y su error
plt.plot(t1, U_CN[:, 0], label="Crank-Nickolson")
plt.plot(t1, Error_CN[:, 0],  label="Error CN")
plt.title("Solución del esquema de Crank-Nickolson y su error")
plt.legend()
plt.xlabel("t")
plt.show()

# Gráfica de Euler Inverso y su error
plt.plot(t1, U_EI[:, 0], label="Euler Inverso")
plt.plot(t1, Error_EI[:, 0],  label="Error EI")
plt.title("Solución del esquema de Euler Inverso y su error")
plt.legend()
plt.xlabel("t")
plt.show()


# Gráfica de convergencia de todos los esquemas
plt.axis('equal') # Cada unidad en el eje 𝑥 x tiene la misma escala visual que cada unidad en el eje y
plt.xlabel('logN')
plt.ylabel('logE')
plt.plot(logN_E, logE_E, '-b')
plt.plot(logN_RK4, logE_RK4, '-g')
plt.plot(logN_CN, logE_CN, '-r')
plt.plot(logN_EI, logE_EI, '-m')
plt.title("Convergencia de todos los esquemas numéricos")
plt.show()

# Gráfica de convergencia de Euler
plt.axis('equal') 
plt.xlabel('logN_E')
plt.ylabel('logE_E')
plt.plot(logN_E, logE_E, '-b')
plt.title("Convergencia del esquema de Euler")
plt.show()

# Gráfica de convergencia de RK4
plt.axis('equal') 
plt.xlabel('logN_RK4')
plt.ylabel('logE_RK4')  
plt.plot(logN_RK4, logE_RK4, '-g')
plt.title("Convergencia del esquema de RK4")
plt.show()

# Gráfica de convergencia de Cranck-Nickolson
plt.axis('equal') 
plt.xlabel('logN_CN')
plt.ylabel('logE_CN')
plt.plot(logN_CN, logE_CN, '-r')
plt.title("Convergencia del esquema de Crank-Nickolson")
plt.show()

# Gráfica de convergencia de Euler Inverso
plt.axis('equal') 
plt.xlabel('logN_EI')
plt.ylabel('logE_EI')
plt.plot(logN_E, logE_E, '-m')
plt.title("Convergencia del esquema de Euler Inverso")
plt.show()