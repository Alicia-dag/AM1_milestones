from numpy import array, zeros, linspace, concatenate
import matplotlib.pyplot as plt
from numpy.linalg import norm
from scipy.optimize import newton
from Modules import CauchyProblem
from Modules import Euler, RK4, CrankNicholson, Euler_Inverso
from Modules import Physics

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
def LeapFrog(f, x0, y0, vx0, vy0, tf, N):
    dt = tf / N
    t = linspace(0, tf, N+1)
    x = zeros(N+1)
    y = zeros(N+1)
    vx = zeros(N+1)
    vy = zeros(N+1)
    
    x[0] = x0
    y[0] = y0
    vx[0] = vx0
    vy[0] = vy0
    
    # First step using Euler method to start Leap-Frog
    x[1] = x[0] + vx[0] * dt
    y[1] = y[0] + vy[0] * dt
    ax, ay = f(x[0], y[0], vx[0], vy[0])
    vx[1] = vx[0] + ax * dt
    vy[1] = vy[0] + ay * dt
    
    for n in range(1, N):
        ax, ay = f(x[n], y[n], vx[n], vy[n])
        x[n+1] = x[n-1] + 2 * vx[n] * dt
        y[n+1] = y[n-1] + 2 * vy[n] * dt
        vx[n+1] = vx[n-1] + 2 * ax * dt
        vy[n+1] = vy[n-1] + 2 * ay * dt
    
    return t, x, y, vx, vy

################################################### CÓDIGO ########################################################


################################################# GRÁFICAS #########################################################
