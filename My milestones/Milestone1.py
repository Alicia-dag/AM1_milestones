from numpy import array, zeros, linspace  #array--vectores, linspace--partición equiespaciada
import matplotlib.pyplot as plt

## DATOS ##

# Condiciones iniciales
x0 = 1
y0 = 0
vx0 = 0
vy0 = 1

# Instantes inicial y final
t0 = 0
tf = 20

# Número de intervalos (=nº de instantes de tiempo-1)
N = 200





## CÓDIGO ##
# Vector de conidic ones iniciales
# Matrices de soluciones
# Inicializamos lado derecho de EDO para Euler y 
# Inicializamos el vector de intantes temporales en los que se calcula la solución
# Vector instantes temporales
# EULER EXPLÍCITO (desarrollar las dos)

F_Euler[n,:] = Kepler(U_Euler[n,:])

U_Euler[n+1,:] = U_Euler[n,:] + (t[n+1]-t[n]) * F_Euler[n,:]

# RUNGE-KUTTA DE 2 ETAPAS
# RUNGE-KUTTA DE 4 ETAPAS
# ADAMS-BASHFORTH DE 2 ETAPAS
