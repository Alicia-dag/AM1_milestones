from numpy import array, zeros, linspace, float64
import matplotlib.pyplot as plt
from scipy.optimize import newton # Import Newton Method


################################################## FUNCIONES #######################################################

def Cauchy_problem( F, t, U0, Temporal_scheme, q=None, Tolerance=None ):  # Lo del None significa que están inicializados pero no tienen orden, se llaman argumentos opcionales
    """
  

    Inputs:  
            F(U,t) : Function dU/dt = F(U,t) 
          t : time partition t (vector of length N+1)
          U0 : initial condition at t=0
          Temporal_schem 
          q : order o scheme (optional) 
          Tolerance: Error tolerance (optional)

    Return: 
          U: matrix[N+1, Nv], Nv state values at N+1 time steps     
    """

    N =  len(t)-1
    Nv = len(U0)
    #U = zeros( (N+1, Nv), dtype=type(U0) )
    U = zeros( (N+1, Nv), dtype=float64 ) 

    U[0,:] = U0

    for n in range(N): # Estudio de lo que pasa con y sin el argumento opcional none

        if q != None: 
          U[n+1,:] = Temporal_scheme( U[n, :], t[n+1] - t[n], t[n],  F, q, Tolerance ) 

        else: 
          U[n+1,:] = Temporal_scheme( U[n, :], t[n+1] - t[n], t[n],  F ) 

    return U



def Euler(U, dt, t, F): 

    return U + dt * F(U, t)



def Kepler(U, t): 

    x = U[0]; y = U[1]; dxdt = U[2]; dydt = U[3]
    d = ( x**2  +y**2 )**1.5

    return  array( [ dxdt, dydt, -x/d, -y/d ] ) 


# El Euler inverso es un método implícito
def Euler_Inverso(U, dt, t, F): 
  
  def G(X): # Siendo X = U(n-1)
    return X - U - dt * F(X, t)
  
  return newton(G, U) # En el milestone 4 habrá que calcularse este Newton pero, por ahora, los importamos
# U no se modifica al "pasar" por la función, la U que sale es la que devuelve Newton


# El Crank-Nickolson es otro método implícito
def Crank_Nickolson(U, dt, t, F): # Es un método mejor para converger
  
  def G(X): # Siendo X = U(n-1)
    return X - U - dt/2 * (F(X, t) + F(U, t))
  
  return newton(G, U)




################################################### CÓDIGO #########################################################

tf = 7 # Si no converge rec¡ducimos este tiempo y la N
N = 2000
t = linspace(0, tf, N)

U = Cauchy_problem (Kepler, t, array ([1., 0., 0., 1.]), Euler)

plt.plot(U[:,0], U[:,1])
plt.show()


U = Cauchy_problem (Kepler, t, array ([1., 0., 0., 1.]), Euler_Inverso)

plt.plot(U[:,0], U[:,1])
plt.show()


U = Cauchy_problem (Kepler, t, array ([1., 0., 0., 1.]), Crank_Nickolson)

plt.plot(U[:,0], U[:,1])
plt.show()

################################################# GRÁFICAS #########################################################
# plt.plot(U[:,0], U[:,1])
# plt.plot(t, U[:,0])
# plt.show()