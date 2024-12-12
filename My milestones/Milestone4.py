from numpy import zeros, linspace, transpose, abs, float64, sqrt
# from sympy import symbols, Eq, lambdify
from scipy.optimize import fsolve, root
import matplotlib.pyplot as plt
from Modules import CauchyProblem
from Modules.NumericalSchemes import Euler, RK4, Crank_Nickolson, Euler_Inverso
from Modules.Physics import Oscilador



################################################# FUNCIONES #######################################################

# # Despeje y obtención de la funcion r(w) imponiendo Pi = 0
# def Funcion_despejar_r(Pi):
#     r = symbols('r')
#     eq = Eq(Pi, 0) 
#     solucion = solve(eq, r)
#     return solucion[0]


# # REGIONES DE ESTABILIDAD
# def Region_Estabilidad(N, x0, xf, y0, yf, Pi):
#     r = Funcion_despejar_r(Pi)
#     w_final = linspace(x0, xf, N) + 1j * linspace(y0, yf, N)[:, None]
#     r_func = lambdify(w, r, 'numpy')
#     r_final = r_func(w_final)
#     return abs(r_final) <= 1


# # Definición de las funciones Pi
# Pi_Euler = r - 1 - w
# Pi_RK4 = - r + 1 + w + w**2/2 + w**3/6 + w**4/24
# Pi_CN = r - 1 + w / 2 * (1 + r)
# Pi_EI = r - 1 - r * w
# Pi_LF = r ** 2 - 1 - 2 * w * r
# Pi = [Pi_Euler, Pi_RK4, Pi_CN, Pi_EI, Pi_LF]


# FUNCIONES DE ESTABILIDAD
def Funcion_Estabilidad_Euler(w):
    return 1 + w

def Funcion_Estabilidad_RK4(w):
    return 1 + w + w**2/2 + w**3/6 + w**4/24

def Funcion_Estabilidad_CN(w):
    return (1 + w / 2) / (1 - w / 2)

def Funcion_Estabilidad_EI(w):
    return 1 / (1 - w)

def Funcion_Estabilidad_LF(w):
    return w + sqrt(w**2 + 1), w - sqrt(w**2 + 1)


# REGIONES DE ESTABILIDAD
def Region_Estabilidad_Euler(N, x0, xf, y0, yf):
    wij = linspace(x0, xf, N) + 1j * linspace(y0, yf, N)[:, None]  # Crear la cuadrícula compleja
    Region_Estabilidad_Euler = zeros((N, N), dtype=bool)  # Matriz para almacenar la estabilidad
    for i in range(N):
        for j in range(N):
            w = wij[i, j]
            r = Funcion_Estabilidad_Euler(w) 
            Region_Estabilidad_Euler[i, j] = abs(r) <= 1  # Verificar si |r| <= 1 (estabilidad)
    return Region_Estabilidad_Euler

def Region_Estabilidad_RK4(N, x0, xf, y0, yf):
    wij = linspace(x0, xf, N) + 1j * linspace(y0, yf, N)[:, None]
    Region_Estabilidad_RK4 = zeros((N, N), dtype=bool)
    for i in range(N):
        for j in range(N):
            w = wij[i, j]
            r = Funcion_Estabilidad_RK4(w) 
            Region_Estabilidad_RK4[i, j] = abs(r) <= 1
    return Region_Estabilidad_RK4

def Region_Estabilidad_CN(N, x0, xf, y0, yf):
    wij = linspace(x0, xf, N) + 1j * linspace(y0, yf, N)[:, None]
    Region_Estabilidad_CN = zeros((N, N), dtype=bool)
    for i in range(N):
        for j in range(N):
            w = wij[i, j]
            r = Funcion_Estabilidad_CN(w) 
            Region_Estabilidad_CN[i, j] = abs(r) <= 1
    return Region_Estabilidad_CN

def Region_Estabilidad_EI(N, x0, xf, y0, yf):
    wij = linspace(x0, xf, N) + 1j * linspace(y0, yf, N)[:, None]
    Region_Estabilidad_EI = zeros((N, N), dtype=bool)
    for i in range(N):
        for j in range(N):
            w = wij[i, j]
            r = Funcion_Estabilidad_EI(w) 
            Region_Estabilidad_EI[i, j] = abs(r) <= 1
    return Region_Estabilidad_EI

def Region_Estabilidad_LF(N, x0, xf, y0, yf):
    wij = linspace(x0, xf, N) + 1j * linspace(y0, yf, N)[:, None]
    Region_Estabilidad_LF = zeros((N, N), dtype=bool)
    for i in range(N):
        for j in range(N):
            w = wij[i, j]
            r1, r2 = Funcion_Estabilidad_LF(w)
            Region_Estabilidad_LF[i, j] = max(abs(r1), abs(r2)) <= 1  # Verificar si el máximo de |r| <= 1 (estabilidad)
    return Region_Estabilidad_LF



################################################## CÓDIGO ####################################################

# Parámetros a representar
N = 400
x0 = -3
xf = 3
y0 = -3
yf = 3

# Llamadas a la función de estabilidad
Region_Estabilidad_Euler = Region_Estabilidad_Euler(N, x0, xf, y0, yf)
Region_Estabilidad_RK4 = Region_Estabilidad_RK4(N, x0, xf, y0, yf)
Region_Estabilidad_CN = Region_Estabilidad_CN(N, x0, xf, y0, yf)
Region_Estabilidad_EI = Region_Estabilidad_EI(N, x0, xf, y0, yf) 
Region_Estabilidad_LF = Region_Estabilidad_LF(N, x0, xf, y0, yf) 


################################################# GRÁFICAS ####################################################

# Región de estabilidad de Euler
plt.figure(figsize=(6, 6))
plt.imshow(Region_Estabilidad_Euler, extent=[x0, xf, y0, yf], origin='lower', cmap='Greys')
plt.title('Región de estabilidad de Euler')
plt.xlabel('Re(r)')
plt.ylabel('Im(r)')
plt.show()

# Región de estabilidad de RK4
plt.figure(figsize=(6, 6))
plt.imshow(Region_Estabilidad_RK4, extent=[x0, xf, y0, yf], origin='lower', cmap='Greys')
plt.title('Región de estabilidad de RK4')
plt.xlabel('Re(r)')
plt.ylabel('Im(r)')
plt.show()

# Región de estabilidad de Crank-Nicolson
plt.figure(figsize=(6, 6))
plt.imshow(Region_Estabilidad_CN, extent=[x0, xf, y0, yf], origin='lower', cmap='Greys')
plt.title('Región de estabilidad de Crank-Nicolson')
plt.xlabel('Re(r)')
plt.ylabel('Im(r)')
plt.show()

# Región de estabilidad de Euler Inverso
plt.figure(figsize=(6, 6))
plt.imshow(Region_Estabilidad_EI, extent=[x0, xf, y0, yf], origin='lower', cmap='Greys')
plt.title('Región de estabilidad de Euler Inverso')
plt.xlabel('Re(r)')
plt.ylabel('Im(r)')
plt.show()

# Región de estabilidad de Leap-Frog
plt.figure(figsize=(6, 6))
plt.imshow(Region_Estabilidad_LF, extent=[x0, xf, y0, yf], origin='lower', cmap='Greys')
plt.title('Región de estabilidad de Leap-Frog')
plt.xlabel('Re(r)')
plt.ylabel('Im(r)')
plt.show()