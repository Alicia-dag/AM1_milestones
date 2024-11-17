from numpy import array, reshape, zeros, linspace
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from Modules.CauchyProblem import Cauchy_problem
from Modules.NumericalSchemes import RK4


################################################# FUNCIONES #######################################################
# Funcion para definir y guardar las condiciones iniciales en el vector U0
def Initial_conditions(Nb, Nc):
    '''''''''''
    INPUTS:
        - Nb: número de cuerpos
        - Nc: número de coordenadas
    '''''''''''
    U0 = zeros(2*Nc*Nb)
    U1 = reshape(U0, (Nb, Nc, 2))  
    r0 = reshape(U1[:, :, 0], (Nb, Nc))
    v0 = reshape(U1[:, :, 1], (Nb, Nc))

    # Cuerpo 1
    r0[0,:] = [1, 0, 0]
    v0[0,:] = [0, 0.5, 0]

    # Cuerpo 2
    v0[1,:] = [0, -1, 0]
    r0[1,:] = [-0.5, 0, 0]

    # Cuerpo 3
    r0[2,:] = [0, -1, 0]
    v0[2,:] = [0.5, 0, 0]

    # Cuerpo 4
    r0[3,:] = [0, 1, 0]
    v0[3,:] = [-0.5, 0, 0]

    # Cuerpo 5
    r0[4,:] = [-1, 0, 0] 
    v0[4,:] = [0, -0.5, 0]
    return U0 


# Función para el "N body problem"
def N_Body_Problem(U, t, Nb, Nc):
    '''''''''''
    INPUTS:
        - U: vector de condiciones iniciales
        - t: tiempo
        - Nb: número de cuerpos
        - Nc: número de coordenadas
    '''''''''''
    
    pu = reshape (U, (Nb, Nc, 2))
    r = reshape (U[:, :, 0], (Nb, Nc)) # Posiciones en pu
    v = reshape (U[:, :, 1], (Nb, Nc)) # Velocidades en pu
    
    Fs = zeros(len(U))
    pFs = reshape (Fs, (Nb, Nc, 2)) 
    
    drdt = reshape (pFs[:, :, 0], (Nb, Nc)) # Derivadas de r en pFs
    dvdt = reshape (pFs[:, :, 1], (Nb, Nc)) # Derivadas de v en pFs
    
    dvdt[:,:] = 0
    
    for i in range (1, Nb):
        drdt[i,:] = v[i,:]
        for j in range (1, Nc):
            for j in range(Nb): 
                if j != i:  
                    d = r[j,:] - r[i,:]
                    dvdt[i,:] = dvdt[i,:] +  d[:] / norm(d)**3 
    return Fs


def F_N_Body_Problem(t, U):
    return N_Body_Problem(t, U, Nb, Nc)



################################################### CÓDIGO ########################################################
# Definicion de los parametros de integracion
N = 10000
t0 = 0
tf = 5
t = linspace(t0, tf, N+1)

# Definicion del numero de cuerpos y del numero de coordenadas por cuerpo
Nb = 5
Nc = 3

# Resolucion del prolema de Cauchy
U0 = Initial_conditions(Nb, Nc)
U = Cauchy_problem(F_N_Body_Problem, t, U0, RK4)


################################################# GRÁFICAS #########################################################
# Representacion de resultados (en 3 dimensiones)
Us = reshape(U, (Nb, Nc, 2, N+1))
r = reshape(Us[:, :, 0, :], (Nb, Nc, N+1))
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
for i in range(Nb):
    ax.plot3D(r[i, 0, :], r[i, 1, :], r[i, 2, :], label=f'Cuerpo {i+1}')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.legend()
plt.show()