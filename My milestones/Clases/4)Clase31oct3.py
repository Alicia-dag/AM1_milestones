from numpy import array, zeros, linspace,log10, concatenate
from numpy.linalg import norm
from scipy.optimize import newton
import matplotlib.pyplot as plt


############################################################################
######################## CONDICIONES INICIALES #############################
############################################################################
#         ->->->->-> Lo único que hay que cambiar <-<-<-<-

T = 0.5 # Periodo
N = 10 # Nº de particiones de U1



x0 = 1 # x Inicial
y0 = 0 # y Inicial
dx0 = 0 # Vx inicial
dy0 = 1 # Vy inicial
U0 = array([x0, y0, dx0, dy0]) # Vector de estado inicial euler
#U0 = array([x0, dx0])




############################################################################
############################# FUNCIONES ###################################
############################################################################
def Euler(U, dt, F, t): # U(n+1) = U(n) + dt * F

    return U + dt * F(U, t)

def RK2(U, dt, F, t): # U(n+1) = U(n) + dt/2 * (K1 + K2)
    K1_RK2 = F(U, t)
    K2_RK2 = F(U + K1_RK2*dt, t + dt)
    return U + dt/2 * (K1_RK2 + K2_RK2)

def RK4(U, dt, F, t): # U(n+1) = U(n) + dt/6 * (K1 + 2*K2 + 2*K3 + K4)
    K1_RK4 = F(U, t)
    K2_RK4 = F(U + K1_RK4*dt/2, t + dt/2)
    K3_RK4 = F(U + K2_RK4*dt/2, t + dt/2)
    K4_RK4 = F(U + K3_RK4*dt, t + dt)
    return U + dt/6 * (K1_RK4 + 2 * K2_RK4 + 2 * K3_RK4 + K4_RK4)

def EulerI(U, dt, F, t):
    def G(X):
        return X-U-dt*F(X, t)
    return newton(G, U, maxiter=500)

def CrankNicholson(U, dt, F, t):
    def G(X):
        return X-U-dt/2*(F(X, t)+F(U,t))
    return newton(G, U, maxiter=500)

def Cauchy(F, t, N, U0, Esquema):
    U = array(zeros((N, len(U0)))) # Definición de U
    U[0,:] = U0 # Asignación del vector de estado inicial
    for i in range(1, N):
        U[i, :] = Esquema(U[i-1,:], t/N, F, t) # Llamada al esquema numérico, e integración por cada paso temporal
    return U


















def Conv(F, U0, t, N, Esquema):
    E = ErrorCauchy(F, U0, t, N, Esquema)
    q = array(zeros((N, len(U0))))
    logN = array(zeros((N, 1)))
    for i in range(4, N):
        q[i,:] = (log10(E[i,:])-log10(E[i-1,:]))/(log10(i)-log10(i-1))
        logN[i,0] = log10(i)
        print(q[i,:])
    
    return q, logN

def Cauchy(F, t, N, U0, Esquema):
    U = array(zeros((N, len(U0)))) # Definición de U
    U[0,:] = U0 # Asignación del vector de estado inicial
    for i in range(1, N):
        U[i, :] = Esquema(U[i-1,:], t/N, F, t) # Llamada al esquema numérico, e integración por cada paso temporal
    return U

def Error(U1, U2, U0, N, Esquema):
    Error = array(zeros((N, len(U0))))
    if Esquema == Euler:
        q = 1
    elif Esquema == RK2:
        q = 2
    elif Esquema == RK4:
        q = 4
    elif Esquema == CrankNicholson: 
        q = 2

    for i in range(0,N):
        Error[i,:] = (U2[2*i,:]-U1[i,:])/(1-1/(2**q)) # E = (U2(dt/2)-U1(dt))/(1-1/2**q)

    return Error

def ErrorCauchy(F, U0, t, N, Esquema): # (Funcion, U, U0, t, N, Esquema)
    
    U1 = Cauchy(F, t, N, U0, Esquema)
    U2 = Cauchy(F, t, 2*N, U0, Esquema)
    
    Error = array(zeros((N, len(U0))))
    if Esquema == Euler:
        q = 1
    elif Esquema == RK2:
        q = 2
    elif Esquema == RK4:
        q = 4
    elif Esquema == CrankNicholson: 
        q = 2

    for i in range(0,N):
        Error[i,:] = (U2[2*i,:]-U1[i,:])/(1-1/(2**q)) # E = (U2(dt/2)-U1(dt))/(1-1/2**q)

    return Error # Cuando saco dos variables, luego como lo hago para tratar esos datos? Como funciona tuple?


def Funcion(U, t):
    F = concatenate((U[2:4], -U[0:2]/norm(U[0:2])**3)) # Función F de Euler
    return F


# ARMÓNICO
#def Funcion(U, t):
#    F = array([U[1],-U[0]])
#    return F


############################################################################
############################# SOLUCIONES ###################################
############################################################################

E_Euler = ErrorCauchy(Funcion, U0, T, N, Euler)
E_RK2 = ErrorCauchy(Funcion, U0, T, N, RK2)
E_RK4 = ErrorCauchy(Funcion, U0, T, N, RK4)
E_CN = ErrorCauchy(Funcion, U0, T, N, CrankNicholson)

print(E_Euler)
############################################################################
############################ CONVERGENCIA ##################################
############################################################################

q_Euler, logNEuler = Conv(Funcion, U0, T, N, Euler)
#q_RK2 = Conv(Funcion, U0, T, N, RK2)
#q_RK4 = Conv(Funcion, U0, T, N, RK4)
#q_CN = Conv(Funcion, U0, T, N, CrankNicholson)

############################################################################
############################## GRÁFICAS ####################################
############################################################################

# Gráfica comparación de posiciones
plt.plot(linspace(0, T, N), E_RK2[:,0], label = 'RK2')
plt.plot(linspace(0, T, N), E_RK4[:,0], label = 'RK4')
plt.plot(linspace(0, T, N), E_CN[:, 0], label = 'Crank-Nicholson')
plt.title('Comparación error de métodos numéricos')
plt.xlabel('N')
plt.ylabel('Error')
plt.legend(loc='upper right')
plt.grid() #############
#plt.axis('equal') ###################
plt.ylim(-0.003,0.003)
plt.show()
