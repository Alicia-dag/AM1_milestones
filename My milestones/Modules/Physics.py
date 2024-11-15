from numpy import array



# KEPLER
def Kepler(U, t): 
    '''''''''''
    INPUTS:
        - U: vector de estado (posición, velocidad)
        - t: partición temporal 
    '''''''''''
    
    x = U[0]; y = U[1]; dxdt = U[2]; dydt = U[3]
    d = ( x**2  +y**2 )**1.5
    
    return  array( [ dxdt, dydt, -x/d, -y/d ] ) 




# OSCILADOR
def Oscilador(U, t): 
    '''''''''''
    INPUTS:
        - U: vector de estado (posición, velocidad)
        - t: partición temporal 
    '''''''''''
    
    x = U[0]; 
    xdot = U[1]
    F = array([xdot, -x])
    return F




# NEWTON
def Newton(F, x_0, Fprima = None, tol = 1e-8, maxiter=50):
    '''''''''''
    INPUTS:
        - F: Función escalar de la que sacar las raíces
        - x_0: Punto inicial del eje x en el que se comienza la iteración  
        - Fprima: derivada de F. (Si no se introduce se calcula dentro de la función)
        - tol: tolerancia (por defecto es 10e-8)
        - maxiter: número máximo de iteraciones
    '''''''''''
    
    def Fp(x):
        if Fprima == None:
            delta = 1e-4
            return (F(x+delta)-F(x-delta))/(2*delta)
        else:
            return Fprima(x)
    
    xn = x_0
    Error = tol + 1
    iter = 0
    
    while Error > tol and iter < maxiter:
        xn1 = xn - F(xn)/Fp(xn)
        Error = abs(xn-xn1)
        xn = xn1
        iter += 1
        print('Error:', Error)
    print('Número de iteraciones: ', iter)
    return xn