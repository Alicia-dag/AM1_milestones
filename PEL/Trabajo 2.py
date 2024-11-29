from sympy import symbols, solve, Min, Eq


#############################################################################################################################################
############################################################# DATOS DEL TRABAJO #############################################################
#############################################################################################################################################
# Propiedades de las sustancias
M_H2 = 2.016  # Masa molar del hidrógeno [kg/kmol]
M_H2 = M_H2 / 1000  # Masa molar del hidrógeno [kg/mol]
M_O2 = 31.998  # Masa molar del oxígeno [kg/mol]
M_O2 = M_O2 / 1000  # Masa molar del oxígeno [kg/mol]
M_H2O = 18.015  # Masa molar del agua [kg/mol]
M_H2O = M_H2O / 1000  # Masa molar del agua [kg/mol]

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
R_u = 8314.4598 # [J/(kmol*K)]
R_u = R_u / 1000 # [J/(mol*K)]
g_0 = 9.80665 # [m/s^2]
T_ref = 298.15 # [K]




#############################################################################################################################################
################################################################# TRABAJO 2 #################################################################
#############################################################################################################################################

###### ECUACIÓN DE COMBUSTIÓN DEL HIDRÓGENO ######
x = symbols('x')

# Mezcla rica
n_r_H2 =1
n_r_O2 = x
a_r = 2 * x
b_r = 1 - 2 * x
c_r = 0

OF_r = (n_r_O2 * M_O2) / (n_r_H2 * M_H2)

# Mezcla pobre
n_p_H2 = 1
n_p_O2 = x
a_p = 1
b_p = 0
c_p = x - 1 / 2

OF_p = (n_p_O2 * M_O2) / (n_p_H2 * M_H2)

# Mezcla estequiométrica
n_e_H2 = 2
n_e_O2 = 1
a_e = 2
b_e = 0
c_e = 0

OF_e = (n_e_O2 * M_O2) / (n_e_H2 * M_H2)



###### CÁLCULOS EN LA PRECÁMARA ######
# Seleccionamos el tipo de mezcla
tipo_mezcla_PC_valores = ["Rica", "Pobre"]
tipo_mezcla_PC = None

while tipo_mezcla_PC not in tipo_mezcla_PC_valores:
    print("Seleccione el tipo de mezcla en la prescámara:")
    print("1. Rica")
    print("2. Pobre")

    # Capturar la elección del usuario
    eleccion = input("Ingrese el número correspondiente (1 para Rica, 2 para Pobre): ")

    # Validar la entrada
    if eleccion == "1":
        tipo_mezcla_PC = "Rica"
    elif eleccion == "2":
        tipo_mezcla_PC = "Pobre"
    else:
        print("Entrada no válida. Por favor, intente de nuevo.")


if tipo_mezcla_PC == tipo_mezcla_PC_valores[0]:
    n_r_H2 =1
    n_r_O2 = x
    a = a_r
    b = b_r
    c = c_r
    OF = OF_r
elif tipo_mezcla_PC == tipo_mezcla_PC_valores[1]:
    n_p_H2 = 1
    n_p_O2 = x
    a = a_p
    b = b_p
    c = c_p
    OF = OF_p
print("La mezcla seleccionada es: ", tipo_mezcla_PC)


# Cálculos de las propiedades de los productos
Cp_prod = (a * Cp_H2O + b * Cp_O2 - c * Cp_H2) / (a + b + c) # Capacidad calorífica de los productos [J/(mol*K)]
Mp_prod = (a * M_H2O + b * M_O2 - c * M_H2) / (a + b + c) # Masa molar de los productos [kg/mol]
delta_f_prod = a * delta_f_H2O + b * delta_f_O2 - c * delta_f_H2 # Entalpía de formación de los productos [J/mol]
Q_comb_PC = - delta_f_prod * (1 + 1 / OF_e) # Calor de reacción [J/mol]


# Ecuación de la energía y cálculo de "x" y OF_opt en cada siutación
Tc_PC = T_t_in_max
if tipo_mezcla_PC == tipo_mezcla_PC_valores[0]:
    (1 + OF) / OF_e * Cp_prod * (Tc_PC - T_ref) - Q_comb_PC == 0
    residual = Eq ((1 + OF) / OF_e * Cp_prod * (Tc_PC - T_ref) - Q_comb_PC, 0)
    x_solution = solve(residual, x)
elif tipo_mezcla_PC == tipo_mezcla_PC_valores[1]:
    (1 + OF) / OF * Cp_prod * (Tc_PC - T_ref) - Q_comb_PC == 0
    residual = Eq ((1 + OF) / OF * Cp_prod * (Tc_PC - T_ref) - Q_comb_PC, 0)
    x_solution = solve(residual, x)
print(x_solution)
OF_opt = (x_solution[1] * M_O2) / M_H2
print("El valor de x es: ", x_solution[1]) 
print("El valor de OF_opt es: ", OF_opt)