from numpy import array, zeros, linspace, concatenate
from numpy.linalg import norm
from Physics import Kepler

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