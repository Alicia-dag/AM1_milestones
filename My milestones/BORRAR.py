from numpy import zeros, linspace, reshape, array
from numpy.linalg import norm
import matplotlib.pyplot as plt

# Definicion de una funcion adicional, ya que la funcion de Cauchy solo da como inputs t y U, y la funcion
# necesita tambien Nb y Nc.
def F_NBody(t, U):
    return N_body(t, U, Nb, Nc)


# Esquema temporal Runge Kutta 4
def RK4(U0, t0, tf, f):
    dt = tf - t0
    k1 = f(t0, U0)
    k2 = f(t0 + dt/2, U0 + k1*dt/2)
    k3 = f(t0 + dt/2, U0 + k2*dt/2)
    k4 = f(t0 + dt, U0 + k3*dt)
    return U0 + dt/6 * (k1 + 2*k2 + 2*k3 + k4)

# Función para integrar ecuaciones (problema de Cauchy)
def Cauchy(t, temporal_scheme, f, U0):
    U = array (zeros((len(U0),len(t))))
    U[:,0] = U0
    for ii in range(0, len(t) - 1):
        U[:,ii+1] = temporal_scheme(U[:,ii], t[ii], t[ii+1], f)
    return U

# Funcion para definir y guardar las condiciones iniciales en el vector U0
def Init_cond(Nb, Nc):
    U0 = zeros(2*Nc*Nb)
    U1 = reshape(U0, (Nb, Nc, 2))  
    r0 = reshape(U1[:, :, 0], (Nb, Nc))
    v0 = reshape(U1[:, :, 1], (Nb, Nc))

    r0[0,:] = [1, 0, 0]
    v0[0,:] = [0, 0.5, 0]

    v0[1,:] = [0, -1, 0]
    r0[1,:] = [-0.5, 0, 0]

    r0[2,:] = [0, 0, 1]
    v0[2,:] = [0, 0, 0.5]

    r0[3,:] = [0, 1, 0]
    v0[3,:] = [0, 0, -0.5]

    r0[4,:] = [-1, 0, 0] 
    v0[4,:] = [0, -0.5, 0]
    return U0 

# Problema de los N cuerpos
def N_body(t, U, Nb, Nc):      
    Us = reshape(U, (Nb, Nc, 2))   
    r = reshape(Us[:, :, 0], (Nb, Nc))
    v = reshape(Us[:, :, 1], (Nb, Nc))

    F = zeros(len(U))   
    dUs = reshape(F, (Nb, Nc, 2))  
    drdt = reshape(dUs[:, :, 0], (Nb, Nc))
    dvdt = reshape(dUs[:, :, 1], (Nb, Nc))
    
    dvdt[:,:] = 0

    for i in range(Nb):   
        drdt[i,:] = v[i,:]
        for j in range(Nb): 
            if j != i:  
                d = r[j,:] - r[i,:]
                dvdt[i,:] = dvdt[i,:] +  d[:] / norm(d)**3 
    
    return F

# Definicion de los parametros de integracion
N = 10000
t0 = 0
tf = 5
t = linspace(t0, tf, N+1)

# Definicion del numero de cuerpos y del numero de coordenadas por cuerpo
Nb = 5
Nc = 3

# Resolucion del prolema de Cauchy
U0 = Init_cond(Nb, Nc)
U = Cauchy(t, RK4, F_NBody, U0)

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