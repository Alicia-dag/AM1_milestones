from numpy import zeros, linspace, log10
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




# ERROR DE LOS ESQUEMAS NUMÉRICOS
def Problem_Error(U0, F, Problema, Esquema, t, q):  #Este método esta escrito sólo para usarse con dt1 = dt2/2, generalizar en el futuro
    '''''''''''
    INPUTS:
        - U0: vector de condiciones iniciales
        - F(U,t): función a resolver
        - Problema(Esquema, F, U0, t): Función que representa el problema a resolver (Cauchy hasta el momento)
        - Esquema(U, F, t): función que representa el esquema numérico a utilizar
        - t: partición temporal 
    '''''''''''

    N = len(t)-1
    t1 = t
    t2 = linspace(t[0], t[-1], 2*N+1) #Refinamiento de malla

    Error = zeros([len(t1), len(U0)])           

    U1 = Problema(Esquema, F, U0, t1) #Solución al problema con la malla original
    U2 = Problema(Esquema, F, U0, t2) #Solución al problema con la malla refinada

    for i in range(len(t)):
        Error[i,:] = (U2[2*i,:] - U1[i,:]) / (1 - 1/2**q)

    return Error




# ERROR DE CONVERGENCIA DE LOS ESQUEMAS NUMÉRICOS
def Problem_Error_Convergencia(U0, F, Problema, Esquema, t):  
    '''''''''''
    INPUTS:
        -U0: vector de condiciones iniciales
        -F(U,t): función a resolver
        -Problema(Esquema, F, U0, t): Función que representa el problema a resolver (Cauchy hasta el momento)
        -Esquema(U, F, t): función que representa el esquema numérico a utilizar
        -t: partición temporal
    '''''''''''
    
    N = len(t)-1
    t1 = t
    t2 = linspace(t[0], t[-1], 2*N+1) #Refinamiento de malla

    Error = zeros([len(t1), len(U0)])           

    U1 = Problema(Esquema, F, U0, t1) #Solución al problema con la malla original
    U2 = Problema(Esquema, F, U0, t2) #Solución al problema con la malla refinada

    for i in range(len(t)):
        Error[i,:] = (U2[2*i,:] - U1[i,:])

    return Error




# CONVERGENCIA DE LOS ESQUEMAS NUMÉRICOS
def Convergencia(U0, F, Error, Problema, Esquema, t):
    '''''''''''
    INPUTS:
        - U0: Vector del estado inicial
        - F: Función a resolver
        - Error(U0, F, Problema, Esquema, t): Función que devuelve un vector con el error de un esquema en cada paso temporal
        - Esquema: Esquema temporal a resolver
        - t: partición temporal 
    '''''''''''
    
    np = 15 #Número de puntos de la regresión 
    logE = zeros(np)
    logN = zeros(np)
    N = len(t-1)
    t1 = t
    for i in range(np):
        
        E = Error(U0, F, Problema, Esquema, t1)
        logE[i] = log10(norm(E[-1,:]))
        logN[i] = log10(N)
        N = 2*N
        t1 = linspace(t[0], t[-1], N+1)    

    return logN, logE