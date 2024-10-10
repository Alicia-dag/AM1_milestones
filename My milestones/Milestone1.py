from numpy import array, zeros, linspace  #array--vectores, linspace--partición equiespaciada
import matplotlib.pyplot as plt

#################################################### DATOS ########################################################

# Condiciones iniciales
x0 = 1
y0 = 0
vx0 = 0
vy0 = 1

# Instantes inicial y final
t0 = 0
tf = 20

# Número de intervalos (= nº de instantes de tiempo - 1)
N = 200



################################################### CÓDIGO ########################################################
# Vector de conidicones iniciales
U0 = array([1, 0, 0, 1])
F0 = array ([vx0, vy0, -x0/(x0**2+y0**2)**3/2, -y0/(x0**2+y0**2)**3/2])
x = array( zeros(N) )
y = array( zeros(N) )
vx = array( zeros(N) )
vy = array( zeros(N) )

# Matrices de soluciones
F_Euler = array( zeros([4,1]) )
U_Euler = array( zeros([4,1]) )

# Inicializamos lado derecho de EDO para Euler 
# Inicializamos el vector de intantes temporales en los que se calcula la solución
# Vector instantes temporales
dt = 0.1

# EULER EXPLÍCITO (desarrollar las dos)
F = array ([vx, vy, -x/(x**2+y**2)**3/2, -y/(x**2+y**2)**3/2])
U = array ([x, y, vx, vy])

U[0] = U0 + dt * F0
U[1] = U[0] + dt * F[0]
U[2] = U[1] + dt * F[1]
U[3] = U[2] + dt * F[2]


print (U[:])
#F_Euler[n,1] =

 
#F_Euler[n,:] = Kepler(U_Euler[n,:])

#U_Euler[n+1,:] = U_Euler[n,:] + (t[n+1]-t[n]) * F_Euler[n,:]

# RUNGE-KUTTA DE 2 ETAPAS

# RUNGE-KUTTA DE 4 ETAPAS

# ADAMS-BASHFORTH DE 2 ETAPAS
