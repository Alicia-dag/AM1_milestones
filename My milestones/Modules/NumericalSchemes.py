from scipy.optimize import newton



# Esquema EULER EXPLÍCITO
def Euler (U, dt, t, F):
    '''''''''''
    INPUTS:
        - U: vector de estado (posición, velocidad)
        - F(U,t): función a resolver
        - t: partición temporal 
    '''''''''''
    
    return U + dt * F(U, t)




# Esquema RUNGE-KUTTA órden 4
def RK4 (U, dt, t, F):
    '''''''''''
    INPUTS:
        - U: vector de estado (posición, velocidad)
        - F(U,t): función a resolver
        - t: partición temporal 
    '''''''''''
    
    k1 = F (U, t)
    k2 = F ( U + k1 * dt/2, t + dt/2)
    k3 = F ( U + k2 * dt/2, t + dt/2)
    k4 = F ( U + k3 * dt , t + dt/2)
    return U + (dt/6) * (k1 + 2*k2 + 2*k3 + k4)




# Esquema implícito EULER IMPLÍCITO
def Euler_Inverso(U, dt, t, F): 
    '''''''''''
    INPUTS:
        - U: vector de estado (posición, velocidad)
        - F(U,t): función a resolver
        - t: partición temporal 
    '''''''''''
    
    def G(X):
        return X - U - dt * F(X, t)
    return newton(G, U)




# Esquema implícito CRANK-NICKOLSON
def Crank_Nickolson(U, dt, t, F): 
    '''''''''''
    INPUTS:
        - U: vector de estado (posición, velocidad)
        - F(U,t): función a resolver
        - t: partición temporal
    '''''''''''
    
    def G(X):
        return X - U - dt/2 * (F(X, t) + F(U, t))
    return newton(G, U)
