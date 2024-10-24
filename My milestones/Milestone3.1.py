from numpy import array, zeros, linspace, concatenate, float64, log
import matplotlib.pyplot as plt
from scipy.optimize import fsolve


################################################# FUNCIONES #######################################################
# KEPLER
def Kepler(U, t): 
    x = U[0]; y = U[1]; dxdt = U[2]; dydt = U[3]
    d = ( x**2  +y**2 )**1.5
    return array([dxdt, dydt, -x/d, -y/d])

# Problema CAUCHY
def Cauchy_problem(F, t, U0, Esquema):  
    N = len(t) - 1
    Nv = len(U0)
    U = zeros((N+1, Nv), dtype=float64) 
    U[0, :] = U0
    for n in range(N): 
        U[n+1, :] = Esquema(U[n, :], t[n+1] - t[n], t[n], F) 
    return U

# Esquema EULER EXPLÍCITO
def Euler(U, dt, t, F):
    return U + dt * F(U, t)

# Esquema RUNGE-KUTTA órden 4
def RK4(U, dt, t, F):
    k1 = F(U, t)
    k2 = F(U + k1 * dt/2, t + dt/2)
    k3 = F(U + k2 * dt/2, t + dt/2)
    k4 = F(U + k3 * dt, t + dt/2)
    return U + (dt/6) * (k1 + 2*k2 + 2*k3 + k4)



# Esquema implícito CRANK-NICKOLSON
def Crank_Nickolson(U, dt, t, F): 
    def G(X):
        return X - U - dt/2 * (F(X, t) + F(U, t))
    return fsolve(G, U)

# Esquema implícito EULER IMPLÍCITO
def Euler_Inverso(U, dt, t, F): 
    def G(X):
        return X - U - dt * F(X, t)
    return fsolve(G, U)

def Richardson(U, dt, t, F): #Extrapolación de Richardson
    U1 = Euler(U, dt/2, t, F)
    U2 = Euler(U1, dt/2, t, F)
    return U2 + (U2 - U1)/15

# Function to evaluate errors using Richardson extrapolation
def evaluate_errors(F, t, U0, Esquema):
    U = Cauchy_problem(F, t, U0, Esquema)
    U_richardson = Cauchy_problem(F, t, U0, Richardson)
    errors = abs(U - U_richardson)
    return errors

# Function to evaluate numerical error for different schemes
def evaluate_numerical_error(F, t, U0):
    schemes = [Euler, Euler_Inverso, Crank_Nickolson, RK4]
    errors = {}
    for scheme in schemes:
        errors[scheme.__name__] = evaluate_errors(F, t, U0, scheme)
    return errors

# Function to evaluate convergence rate
def evaluate_convergence_rate(F, t, U0):
    schemes = [Euler, Euler_Inverso, Crank_Nickolson, RK4]
    rates = {}
    for scheme in schemes:
        errors = evaluate_errors(F, t, U0, scheme)
        dt = t[1] - t[0]
        rate = log(errors[1:] / errors[:-1]) / log(dt)
        rates[scheme.__name__] = rate
    return rates


################################################### CÓDIGO ########################################################
# Example usage
t = linspace(0, 1000, 10)
U0 = array([1, 0, 0, 1], dtype=float64)
errors = evaluate_numerical_error(Kepler, t, U0)
rates = evaluate_convergence_rate(Kepler, t, U0)


################################################# GRÁFICAS #########################################################
# Gráfica de errores
plt.figure(figsize=(10, 6))
for scheme, error in errors.items():
    plt.plot(t, error[:, 0], label=f'{scheme} (x)')
    plt.plot(t, error[:, 1], label=f'{scheme} (y)')
plt.yscale('log')
plt.xlabel('t')
#plt.xlim([0, 10])
plt.ylabel('Error')
plt.title('Numerical Errors for Different Schemes')
plt.legend()
plt.grid(True)
plt.show()

# Gráfica de convergence rates
plt.figure(figsize=(10, 6))
for scheme, rate in rates.items():
    plt.plot(t[1:], rate[:, 0], label=f'{scheme} (x)')
    plt.plot(t[1:], rate[:, 1], label=f'{scheme} (y)')
plt.xlabel('t')
plt.ylabel('Convergence Rate')
plt.title('Convergence Rates for Different Schemes')
plt.legend()
plt.grid(True)
plt.show()