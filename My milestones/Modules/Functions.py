from numpy import zeros, linspace, log10, polyfit, float64
from numpy.linalg import norm


#MESH REFINEMENT
def Mesh_Refinement(t1): # Cada función define las cosas como quiera, se puede repetir nomenclatura
    '''''''''''
    Refinación de malla: dada la partición t1 (con N+1 puntos), obtiene la partición t2 (que tiene 2N+1 puntos)
    Los nodos pares de t2 seguirán siendo los mismos que los de t1, y los nodos impares serán los puntos medios de los intervalos de t1
    
    INPUTS:
        - t1: partición temporal con N+1 puntos
    '''''''''''
    
    N = len(t1) - 1
    t2 = zeros(2*N + 1)
    for i in range(N + 1): # Recordar que el range es [), por eso va hasta N+1]
        t2[2*i] = t1[i] # Nodos pares
        t2[2*i+1] = (t1[i+1] -  t1[i]) / 2 # Nodos impares
    t2[2*N] = t1[N] # Se añade el último nodo, hay que añadirlo a mano. IMPORTANTE
    return t2




# Defición de la función PARTICIÓN para un caso genérico
def Partition(a, b, N):
    '''''''''''
    INPUTS:
        - a: tiempo incial
        - b: tiempo final
        - N: número de intervalos (particiones)
    '''''''''''
    
    t = zeros(N + 1) 
    for i in range (0, N+1):
        t[i] = a + i * (b - a) / N # Esto es lo que hace el comando linspace
    return (t)




# ERROR DE CONVERGENCIA DE LOS ESQUEMAS NUMÉRICOS: Extrapolación de Richardson
def Schemes_error(U0, F, Problema, Esquema, t):
    '''''''''''
    INPUTS:
        - U0: vector de condiciones iniciales
        - F(U,t): función a resolver
        - Esquema(U, F, t): función que representa el esquema numérico a utilizar
        - Problema(Esquema, F, U0, t): Función que representa el problema a resolver (Cauchy hasta el momento)
        - t: partición temporal 
    '''''''''''
    
    N = len(t) - 1
    a = t[0]
    b = t[N]
    
    Error = zeros((N+1, len(U0)))
    
    t1 = t
    t2 = Partition (a, b, 2*N)
    
    U_1 = Problema (F, t1, U0, Esquema) # Solución del problema (hasta ahora de Cauchy) con la malla original
    U_2 = Problema (F, t2, U0, Esquema) # Solución del problema (hasta ahora de Cauchy) con la malla modificada (más fina), es decir, con una malla refinada
    
    # Para calcular el error se hace la resta, pero un vector no se puede restar de otro si uno mide N+1 y el otro N, por eso se hace la resta en los nodos pares
    for i in range (0, N+1): 
        Error[i, :] = U_2[2*i, :] - U_1[i, :] # en este caso los dos puntitos significan: para todas las variables
        
    return U_1, Error




# CONVERGENCIA DE LOS ESQUEMAS NUMÉRICOS
def Convergence(U0, F, Error, Problema, Esquema, t):
    '''''''''''
    INPUTS:
        - U0: Vector del estado inicial
        - F: Función a resolver
        - Error(U0, F, Problema, Esquema, t): Función que devuelve un vector con el error de un esquema en cada paso temporal
        - Esquema: Esquema temporal a resolver
        - t: partición temporal
    OUTPUTS:
        - logN:  vector for the different number of time partitions 
        - logE:  error for each time partition      
        - Order:  order of Error of the temporal scheme 
    '''''''''''
    
    np = 6  # Número de puntos de la regresión, si se sube más tarda MUCHO en converger
    logE = zeros(np)
    logN = zeros(np)
    N = len(t) - 1
    t1 = t
    
    for i in range(np):
        U, Er = Error(U0, F, Problema, Esquema, t1)  # Asumiendo que Error devuelve U_1 y Error
        logE[i] = log10(norm(Er[N, :])) 
        logN[i] = log10(float(N))
        N = 2*N
        t1 = linspace(t[0], t[-1], N+1)  
        
    y = logE[ logE > -12 ]
    x = logN[ 0:len(y) ]
    Order, b = polyfit(x, y, 1) # Regresión lineal para encontrar la pendiente de la recta que mejor se ajusta a los datos
    # print("Order =", Order, "b =", b)
    return logN, logE, Order



# REGIÓN DE ESTABILIDAD
def Region_Estabilidad(Scheme, N, x0, xf, y0, yf): 
    '''''''''''
    INPUTS:
        - Scheme: esquema numérico a utilizar
        - N: número de puntos en la malla
        - x0, xf: intervalo en x
        - y0, yf: intervalo en y
    '''''''''''
    
    x = linspace(x0, xf, N) # Malla en x
    y = linspace(y0, yf, N) # Malla en y
    rho =  zeros( (N, N),  dtype=float64) # Matriz de estabilidad
    F = lambda u, t: w*u # Función anónima que representa la ecuación diferencial a resolver
    
    for i in range(N): 
        for j in range(N):
            w = complex(x[i], y[j]) # Número complejo
            r = Scheme(1., 1., 0., F) # 1. = paso temporal inicial, 1. = valor inicial solución, 0. = tiempo inicial, F = función a resolver
            rho[i, j] = abs(r)
    return rho, x, y  