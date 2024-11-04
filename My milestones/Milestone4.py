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


################################################### CÓDIGO ########################################################


################################################# GRÁFICAS #########################################################
