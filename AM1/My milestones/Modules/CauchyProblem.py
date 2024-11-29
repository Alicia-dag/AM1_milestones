from numpy import zeros, float64



# CAUCHY PROBLEM
def Cauchy_problem(F, t, U0, Esquema):  
    '''''''''''
    Problema CAUCHY: consiste en obtener la solución de un problema de CI dada una CI y un esquema temporal
    INPUTS:
        - Esquema(U, F, t): función que representa el esquema numérico a utilizar
        - F(U,t): función a resolver
        - U0: vector de condiciones iniciales
        - t: partición temporal
    
    OUTPUT:
        - U: Solución para todo instante temporal y para todo componente
    '''''''''''
    
    N =  len(t)-1
    Nv = len(U0)
    U = zeros( (N+1, Nv), dtype=float64 ) 
    U[0,:] = U0
    
    for n in range(N): 
        U[n+1,:] = Esquema( U[n, :], t[n+1] - t[n], t[n],  F ) 
    return U