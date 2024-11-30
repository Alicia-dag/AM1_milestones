from sympy import symbols, solve, Min, Eq
from scipy.optimize import fsolve
from matplotlib import pyplot as plt
import numpy as np


#############################################################################################################################################
############################################################# DATOS DEL TRABAJO #############################################################
#############################################################################################################################################
# Propiedades de las sustancias
M_H2 = 2.016  # Masa molar del hidrógeno [kg/kmol]
# M_H2 = M_H2 / 1000  # Masa molar del hidrógeno [kg/mol]
M_O2 = 31.998  # Masa molar del oxígeno [kg/mol]
# M_O2 = M_O2 / 1000  # Masa molar del oxígeno [kg/mol]
M_H2O = 18.015  # Masa molar del agua [kg/mol]
# M_H2O = M_H2O / 1000  # Masa molar del agua [kg/mol]

Cp_H2 = 36.11 # Capacidad calorífica del hidrógeno [J/(mol*K)]
Cp_O2 = 39.07 # Capacidad calorífica del oxígeno [J/(mol*K)]
Cp_H2O = 54.32 # Capacidad calorífica del agua [J/(mol*K)]

delta_f_H2 = 0 # Entalpía de formación del hidrógeno [J/mol]
delta_f_O2 = 0 # Entalpía de formación del oxígeno [J/mol]
delta_f_H2O = 241818 # Entalpía de formación del agua [J/mol]

rho_H2 = 1140 # Densidad del hidrógeno [kg/m3]
rho_O2 = 71 # Densidad del oxígeno [kg/m3]
rho_H2O = 1000 # Densidad del agua [kg/m3]


# Datos generales
E = 50000 # [kg]
E = E * 9.81 # [N]
p_adapt = 40000 # [Pa]

# Datos línea LH2
pd_B1 = 3 * 10**5 # [Pa]
eta_B1 = 0.62 # Eficiencia de la bomba 1
pi_inyCC_red = 0.82 # Caída de presión de inyección de combustible
pi_refr = 0.88 # Caída de presión en la parte de refrigeración
k_LH2 = 0.2 

# Datos línea LO2
pd_B2 = 6 * 10**5 # [Pa]
eta_B2 = 0.64 # Eficiencia de la bomba 2
pi_inyCC_ox = 0.78 # Caída de presión de inyección de combustible en cámara de combustión
pi_inyPC_ox = 0.88 # Caída de presión de inyección de combustible en precombustión
k_LO2 = 0.02

# Datos línea conjunta
T_t_in_max = 900 # [K]
pi_t_max = 12 # Caída de presión máxima en turbina
eta_t = 0.72 # Eficiencia de la turbina
pi_mec = 0.94 # Caída de presión mecánica
pi_PC = 0.92 # Caída de presión en precombustión
eta_q = 1 # Eficiencia del quemador
Ru = 8314.4598 # [J/(kmol*K)]
Ru = Ru / 1000 # [J/(mol*K)]
g_0 = 9.80665 # [m/s^2]
T_ref = 298.15 # [K]




#############################################################################################################################################
################################################################# TRABAJO 2 #################################################################
#############################################################################################################################################

###### CÁLCULOS EN LA PRECÁMARA (ECUACIÓN DE COMBUSTIÓN DEL HIDRÓGENO) ######
x = symbols('x')

# Relación estequiométrica
OF_PC_st = 0.5 * (M_O2 / M_H2) # Relación estequiométrica [adim]


# Seleccionamos el tipo de mezcla
tipo_mezcla_PC_valores = ["Rica", "Pobre", "Estequiométrica"]
tipo_mezcla_PC = None

while tipo_mezcla_PC not in tipo_mezcla_PC_valores:
    print("Seleccione el tipo de mezcla en la prescámara:")
    print("1. Rica")
    print("2. Pobre")

    # Capturar la elección del usuario
    eleccion = input("Ingrese el número correspondiente (1 para Rica, 2 para Pobre, 3 para Estequiométrica): ")

    # Validar la entrada
    if eleccion == "1":
        tipo_mezcla_PC = "Rica"
    elif eleccion == "2":
        tipo_mezcla_PC = "Pobre"
    elif eleccion == "3":
        tipo_mezcla_PC = "Estequiométrica"
    else:
        print("Entrada no válida. Por favor, intente de nuevo.")


# Cálculos de las popiedades químicas según el tipo de mezcla: H2 + x * O2 -> a * H2O + b * H2 + c * O2 + Q
if tipo_mezcla_PC == tipo_mezcla_PC_valores[0]: # Mezcla rica
    n_H2 = 1
    n_O2 = x
    a = 2 * x
    b = 1 - 2 * x
    c = 0
    
    OF_PC = (n_O2 * M_O2) / (n_H2 * M_H2)
    
elif tipo_mezcla_PC == tipo_mezcla_PC_valores[1]: # Mezcla pobre
    n_H2 = 1
    n_O2 = x
    a = 1
    b = 0
    c = x - 1 / 2
    
    OF_PC = (n_O2 * M_O2) / (n_H2 * M_H2)
    
elif tipo_mezcla_PC == tipo_mezcla_PC_valores[2]: # Mezcla estequiométrica
    n_H2 = 2
    n_O2 = 1
    a = 2
    b = 0
    c = 0
    
    OF_PC = (n_O2 * M_O2) / (n_H2 * M_H2)
    
print("La mezcla seleccionada es: ", tipo_mezcla_PC)


# Cálculos de las propiedades de los productos
if tipo_mezcla_PC == tipo_mezcla_PC_valores[0]: # Mezcla rica
    Cp_prod = (a * Cp_H2O + b * Cp_H2 + c * Cp_O2) / (a + b + c) # Capacidad calorífica de los productos [J/(mol*K)]
    Mp_prod = (a * M_H2O + b * M_H2 + c * M_O2) / (a + b + c) # Masa molar de los productos [kg/mol]
    Cp_prod_kg = Cp_prod * 1000 / Mp_prod # Capacidad calorífica de los productos [J/(kg*K)]
    delta_f_prod = a * delta_f_H2O + b * delta_f_H2 + c * delta_f_O2 # Entalpía de formación de los productos [J/mol]
    delta_f_prod = delta_f_H2O # Entalpía de formación de los productos [J/mol]
    Q_comb_PC = - delta_f_prod * (1 + 1 / OF_PC_st) # Calor de reacción [J/mol]
    Rg = Ru / Mp_prod # Constante de los gases
    gamma = Cp_prod_kg / (Cp_prod_kg - Rg) # Coeficiente adiabático
    
elif tipo_mezcla_PC == tipo_mezcla_PC_valores[1]: # Mezcla pobre
    Cp_prod = (1 * Cp_H2O + b * Cp_H2 + c * Cp_O2) / (a + b + c) # Capacidad calorífica de los productos [J/(mol*K)]
    Mp_prod = (a * M_H2O + b * M_H2 + c * M_O2) / (a + b + c) # Masa molar de los productos [kg/mol]
    Cp_prod_kg = Cp_prod * 1000 / Mp_prod # Capacidad calorífica de los productos [J/(kg*K)]
    delta_f_prod = a * delta_f_H2O + b * delta_f_H2 + c * delta_f_O2 # Entalpía de formación de los productos [J/mol]
    delta_f_prod = delta_f_H2O # Entalpía de formación de los productos [J/mol]
    Q_comb_PC = - delta_f_prod * (1 + 1 / OF_PC_st) # Calor de reacción [J/mol]
    Rg = Ru / Mp_prod # Constante de los gases
    gamma = Cp_prod_kg / (Cp_prod_kg - Rg) # Coeficiente adiabático
    
elif tipo_mezcla_PC == tipo_mezcla_PC_valores[2]: # Mezcla estequiométrica
    Cp_prod = (a * Cp_H2O + b * Cp_O2 + c * Cp_H2) / (a + b + c) # Capacidad calorífica de los productos [J/(mol*K)]
    Mp_prod = (a * M_H2O + b * M_O2 + c * M_H2) / (a + b + c) # Masa molar de los productos [kg/mol]
    Cp_prod_kg = Cp_prod * 1000 / Mp_prod # Capacidad calorífica de los productos [J/(kg*K)]
    delta_f_prod = a * delta_f_H2O + b * delta_f_O2 + c * delta_f_H2 # Entalpía de formación de los productos [J/mol]
    Q_comb_PC = - delta_f_prod * (1 + 1 / OF_PC_st) # Calor de reacción [J/mol]
    Rg = Ru / Mp_prod # Constante de los gases
    gamma = Cp_prod_kg / (Cp_prod_kg - Rg) # Coeficiente adiabático
    


# Ecuación de la energía en la precámara
Tc_PC = T_t_in_max

def Ec_Energia(OF_PC, OF_PC_st, Cp_prod, Tc_PC, T_ref, Q_comb_PC, eta_q, tipo_mezcla_PC, tipo_mezcla_PC_valores):
    
    if tipo_mezcla_PC == tipo_mezcla_PC_valores[0]: # Mezcla rica
        print (Q_comb_PC)
        print (OF_PC)
        print (OF_PC_st)
        print (Cp_prod)
        print (Tc_PC)
        print (T_ref)
        residual =  (1 + OF_PC) / (OF_PC) * Cp_prod * (Tc_PC - T_ref) - Q_comb_PC * eta_q
        eq = Eq(residual, 0)
        x_solution = solve(eq, x)
        
        # Graficar el residual
        plt.plot(x_solution, residual, '-b')
        plt.xlabel('x')
        plt.ylabel('Residual')
        plt.title('Residual vs x')
        plt.grid(True)
        plt.show()

    elif tipo_mezcla_PC == tipo_mezcla_PC_valores[1]: # Mezcla pobre
        print (Q_comb_PC)
        print (OF_PC)
        print (OF_PC_st)
        print (Cp_prod)
        print (Tc_PC)
        print (T_ref)
        residual =  (1 + OF_PC) / (OF_PC_st) * Cp_prod * (Tc_PC - T_ref) - Q_comb_PC * eta_q
        eq = Eq(residual, 0)
        x_solution = solve(eq, x)
        
    elif tipo_mezcla_PC == tipo_mezcla_PC_valores[2]: # Mezcla estequiométrica
        residual =  (1 + OF_PC) / (OF_PC_st) * Cp_prod * (Tc_PC - T_ref) - Q_comb_PC * eta_q
        x_solution = 1
        
    return x_solution


# Cálculo de OF_PC_opt en cada siutación

if tipo_mezcla_PC == tipo_mezcla_PC_valores[0]: # Mezcla rica
    soluciones = Ec_Energia(OF_PC, OF_PC_st, Cp_prod, Tc_PC, T_ref, Q_comb_PC, eta_q, tipo_mezcla_PC, tipo_mezcla_PC_valores)
    print("Las soluciones para x son:", soluciones)
    OF_PC_opt = (soluciones[0] * M_O2) / M_H2 

elif tipo_mezcla_PC == tipo_mezcla_PC_valores[1]: # Mezcla pobre
    soluciones = Ec_Energia(OF_PC, OF_PC_st, Cp_prod, Tc_PC, T_ref, Q_comb_PC, eta_q, tipo_mezcla_PC, tipo_mezcla_PC_valores)
    print("Las soluciones para x son:", soluciones)
    OF_PC_opt = (soluciones[1] * M_O2) / M_H2 

elif tipo_mezcla_PC == tipo_mezcla_PC_valores[2]: # Mezcla estequiométrica
    x_solution = 1
    OF_PC_opt = OF_PC_st


print("El valor de OF_PC_opt es: ", OF_PC_opt)

