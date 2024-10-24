from numpy import array, zeros
from scipy.optimize import newton

# KEPLER
def Kepler(U, t): 

    x = U[0]; y = U[1]; dxdt = U[2]; dydt = U[3]
    d = ( x**2  +y**2 )**1.5

    return  array( [ dxdt, dydt, -x/d, -y/d ] ) 


# OSCILADOR
def Oscilador(U, t): 
    x = U[0]; 
    xdot = U[1]
    F = array([xdot, -x])
    return F