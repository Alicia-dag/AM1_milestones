from sympy import symbols, solve, Min, Eq
from scipy.optimize import fsolve
from numpy import sqrt


#############################################################################################################################################
############################################################# DATOS DEL TRABAJO #############################################################
#############################################################################################################################################
# Propiedades de las sustancias
M_H2 = 2.016  # Masa molar del hidrógeno [kg/kmol]
M_H2 = M_H2 / 1000  # Masa molar del hidrógeno [kg/mol]
M_O2 = 31.998  # Masa molar del oxígeno [kg/Kmol]
M_O2 = M_O2 / 1000  # Masa molar del oxígeno [kg/mol]
M_H2O = 18.015  # Masa molar del agua [kg/Kmol]
M_H2O = M_H2O / 1000  # Masa molar del agua [kg/mol]

Cp_H2 = 36.11 # Capacidad calorífica del hidrógeno [J/(mol*K)]
Cp_O2 = 39.07 # Capacidad calorífica del oxígeno [J/(mol*K)]
Cp_H2O = 54.32 # Capacidad calorífica del agua [J/(mol*K)]

delta_f_H2 = 0 # Entalpía de formación del hidrógeno [J/mol]
delta_f_O2 = 0 # Entalpía de formación del oxígeno [J/mol]
delta_f_H2O = - 241818 # Entalpía de formación del agua [J/mol]

rho_H2 = 1140 # Densidad del hidrógeno [kg/m3]
rho_O2 = 71 # Densidad del oxígeno [kg/m3]
rho_H2O = 1000 # Densidad del agua [kg/m3]


# Datos generales
Empuje = 50000 # [kg]
Empuje = E * 9.81 # [N]
p_adapt = 40000 # [Pa]

# Datos línea LH2
pd_B1 = 3 * 10**5 # [Pa]
pd_f = pd_B1
eta_B1 = 0.62 # Eficiencia de la bomba 1
eta_f = eta_B1
pi_inyCC_f = 0.82 # Caída de presión de inyección de combustible
pi_refr = 0.88 # Caída de presión en la parte de refrigeración
k_LH2 = 0.2 
k_f = k_LH2

# Datos línea LO2
pd_B2 = 6 * 10**5 # [Pa]
pd_ox = pd_B2
eta_B2 = 0.64 # Eficiencia de la bomba 2
eta_ox = eta_B2
pi_inyCC_ox = 0.78 # Caída de presión de inyección de combustible en cámara de combustión
pi_inyPC_ox = 0.88 # Caída de presión de inyección de combustible en precombustión
k_LO2 = 0.02
k_ox = k_LO2

# Datos línea conjunta
T_t_in_max = 900 # [K]
pi_t_max = 12 # Caída de presión máxima en turbina
eta_t = 0.72 # Eficiencia de la turbina
eta_mec = 0.94 # Caída de presión mecánica
pi_PC = 0.92 # Caída de presión la precombustión
eta_q = 1 # Eficiencia de combustión
Ru = 8314.4598 # [J/(kmol*K)]
Ru = Ru / 1000 # [J/(mol*K)]
g_0 = 9.80665 # [m/s^2]
T_ref = 298.15 # [K]




#############################################################################################################################################
################################################################# TRABAJO 2 #################################################################
#############################################################################################################################################

###############################################################################
# PASO 1: ECUACIÓN DE COMBUSTIÓN DEL HIDRÓGENO                                #
###############################################################################

x = symbols('x')

# Relación estequiométrica
OF_PC_st = 0.5 * (M_O2 / M_H2) # Relación estequiométrica [adim]


# Cálculos de las popiedades químicas según el tipo de mezcla: H2 + x * O2 -> a * H2O + b * H2 + c * O2 + Q
def Propiedades_químicas(Tipo_mezcla, Tipo_mezcla_valores):
    if Tipo_mezcla == Tipo_mezcla_valores[0]: # Mezcla rica
        n_H2 = 1
        n_O2 = x
        a = 2 * x
        b = 1 - 2 * x
        c = 0
        
        OF = (n_O2 * M_O2) / (n_H2 * M_H2) # Relación de mezcla [adim]
        Cp_prod = (a * Cp_H2O + b * Cp_H2 + c * Cp_O2) / (a + b + c) # Capacidad calorífica de los productos [J/(mol*K)]
        Mp_prod = (a * M_H2O + b * M_H2 + c * M_O2) / (a + b + c) # Masa molar de los productos [kg/mol]
        Cp_prod_kg = Cp_prod / Mp_prod # Capacidad calorífica de los productos [J/(kg*K)]
        delta_f_prod = a * delta_f_H2O + b * delta_f_H2 + c * delta_f_O2 # Entalpía de formación de los productos [J/mol]
        # delta_f_prod = delta_f_H2O # Entalpía de formación de los productos [J/mol]
        Q_comb_PC = - delta_f_prod * (1 + 1 / OF_PC_st) # Calor de reacción [J/mol]
        Rg = Ru / Mp_prod # Constante de los gases
        gamma = Cp_prod_kg / (Cp_prod_kg - Rg) # Coeficiente adiabático
        Gamma_gamma = sqrt(gamma) * (2 / (gamma + 1)) ** ((gamma + 1) / (2 * (gamma - 1))) # Parámetro Gamma(gamma)
        
        Tc = T_ref - (a * delta_f_H2O) / (a * Cp_H2O + b * Cp_H2 + c * Cp_O2) # Temperatura de combustión [K]
        
        
    elif Tipo_mezcla == Tipo_mezcla_valores[1]: # Mezcla pobre
        n_H2 = 1
        n_O2 = x
        a = 1
        b = 0
        c = x - 1 / 2
        
        OF = (n_O2 * M_O2) / (n_H2 * M_H2) # Relación de mezcla [adim]
        Cp_prod = (1 * Cp_H2O + b * Cp_H2 + c * Cp_O2) / (a + b + c) # Capacidad calorífica de los productos [J/(mol*K)]
        Mp_prod = (a * M_H2O + b * M_H2 + c * M_O2) / (a + b + c) # Masa molar de los productos [kg/mol]
        Cp_prod_kg = Cp_prod / Mp_prod # Capacidad calorífica de los productos [J/(kg*K)]
        delta_f_prod = a * delta_f_H2O + b * delta_f_H2 + c * delta_f_O2 # Entalpía de formación de los productos [J/mol]
        # delta_f_prod = delta_f_H2O # Entalpía de formación de los productos [J/mol]
        Q_comb_PC = - delta_f_prod * (1 + 1 / OF_PC_st) # Calor de reacción [J/mol]
        Rg = Ru / Mp_prod # Constante de los gases
        gamma = Cp_prod_kg / (Cp_prod_kg - Rg) # Coeficiente adiabático
        Gamma_gamma = sqrt(gamma) * (2 / (gamma + 1)) ** ((gamma + 1) / (2 * (gamma - 1))) # Parámetro Gamma(gamma)
        
        Tc = T_ref - (a * delta_f_H2O) / (a * Cp_H2O + b * Cp_H2 + c * Cp_O2) # Temperatura de combustión [K]
        
        
    elif Tipo_mezcla == Tipo_mezcla_valores[2]: # Mezcla estequiométrica
        n_H2 = 2
        n_O2 = 1
        a = 2
        b = 0
        c = 0
        
        OF = (n_O2 * M_O2) / (n_H2 * M_H2) # Relación de mezcla [adim]
        Cp_prod = (a * Cp_H2O + b * Cp_O2 + c * Cp_H2) / (a + b + c) # Capacidad calorífica de los productos [J/(mol*K)]
        Mp_prod = (a * M_H2O + b * M_O2 + c * M_H2) / (a + b + c) # Masa molar de los productos [kg/mol]
        Cp_prod_kg = Cp_prod / Mp_prod # Capacidad calorífica de los productos [J/(kg*K)]
        delta_f_prod = a * delta_f_H2O + b * delta_f_O2 + c * delta_f_H2 # Entalpía de formación de los productos [J/mol]
        Q_comb_PC = - delta_f_prod * (1 + 1 / OF_PC_st) # Calor de reacción [J/mol]
        Rg = Ru / Mp_prod # Constante de los gases
        gamma = Cp_prod_kg / (Cp_prod_kg - Rg) # Coeficiente adiabático
        Gamma_gamma = sqrt(gamma) * (2 / (gamma + 1)) ** ((gamma + 1) / (2 * (gamma - 1))) # Parámetro Gamma(gamma)

        Tc = T_ref - (a * delta_f_H2O) / (a * Cp_H2O + b * Cp_H2 + c * Cp_O2) # Temperatura de combustión [K]
        
    return OF, Cp_prod, Mp_prod, Cp_prod_kg, delta_f_prod, Q_comb_PC, Rg, gamma, Gamma_gamma, Tc



###############################################################################
# PASO 2: CÁLCULOS EN LA PRECÁMARA (RELACIÓN DE MEZCLA)                       #
###############################################################################

# Seleccionamos el tipo de mezcla para la ecuación de combustión del hidrógeno
Tipo_mezcla_PC_valores = ["Rica", "Pobre", "Estequiométrica"]
Tipo_mezcla_PC = None

while Tipo_mezcla_PC not in Tipo_mezcla_PC_valores:
    print("Seleccione el tipo de mezcla en la pre-cámara:")
    print("1. Rica")
    print("2. Pobre")

    # Capturar la elección del usuario
    eleccion = input("Ingrese el número correspondiente (1 para Rica, 2 para Pobre, 3 para Estequiométrica): ")

    # Validar la entrada
    if eleccion == "1":
        Tipo_mezcla_PC = "Rica"
    elif eleccion == "2":
        Tipo_mezcla_PC = "Pobre"
    elif eleccion == "3":
        Tipo_mezcla_PC = "Estequiométrica"
    else:
        print("Entrada no válida. Por favor, intente de nuevo.")


# Asignación de las propiedades químicas según el tipo de mezcla seleccionado para la pre-cámara
OF_PC, Cp_prod_PC, Mp_prod_PC, Cp_prod_PC_kg, delta_f_prod_PC, Q_comb_PC, Rg_PC, gamma_PC, Gamma_gamma_PC, Tc_PC = Propiedades_químicas(Tipo_mezcla_PC, Tipo_mezcla_PC_valores)

print("La mezcla seleccionada en la pre-cámara es: ", Tipo_mezcla_PC)


# Ecuación de la energía en la precámara
Tc_PC = T_t_in_max

def Ec_Energia(OF, OF_st, Cp_prod, Tc, T_ref, Q_comb, eta_q, Tipo_mezcla, Tipo_mezcla_valores):
    
    if Tipo_mezcla == Tipo_mezcla_valores[0]: # Mezcla rica
        residual =  (1 + OF) / (OF) * Cp_prod * (Tc - T_ref) - Q_comb * eta_q
        eq = Eq(residual, 0)
        x_solution = solve(eq, x)

    elif Tipo_mezcla == Tipo_mezcla_valores[1]: # Mezcla pobre
        residual =  (1 + OF) / (OF_st) * Cp_prod * (Tc - T_ref) - Q_comb * eta_q
        eq = Eq(residual, 0)
        x_solution = solve(eq, x)
        
    elif Tipo_mezcla == Tipo_mezcla_valores[2]: # Mezcla estequiométrica
        residual =  (1 + OF) / (OF_st) * Cp_prod * (Tc - T_ref) - Q_comb * eta_q
        x_solution = 1
        
    return x_solution


# Cálculo de OF_PC_opt en cada siutación
if Tipo_mezcla_PC == Tipo_mezcla_PC_valores[0]: # Mezcla rica
    soluciones = Ec_Energia(OF_PC, OF_PC_st, Cp_prod_PC, Tc_PC, T_ref, Q_comb_PC, eta_q, Tipo_mezcla_PC, Tipo_mezcla_PC_valores)
    print(soluciones)
    OF_PC_opt = (soluciones[1] * M_O2) / M_H2 
    phi_PC_opt = OF_PC_st / OF_PC_opt

elif Tipo_mezcla_PC == Tipo_mezcla_PC_valores[1]: # Mezcla pobre
    soluciones = Ec_Energia(OF_PC, OF_PC_st, Cp_prod_PC, Tc_PC, T_ref, Q_comb_PC, eta_q, Tipo_mezcla_PC, Tipo_mezcla_PC_valores)
    print(soluciones)
    OF_PC_opt = (soluciones[1] * M_O2) / M_H2 
    phi_PC_opt = OF_PC_st / OF_PC_opt

elif Tipo_mezcla_PC == Tipo_mezcla_PC_valores[2]: # Mezcla estequiométrica
    x_solution = 1
    OF_PC_opt = OF_PC_st
    phi_PC_opt = OF_PC_st / OF_PC_opt


print("El valor de OF_PC_opt es: ", OF_PC_opt)
print("El valor de phi_PC_opt es", phi_PC_opt)



###############################################################################
# PASO 3: CÁLCULO DE LAS PRESIONES                                            #
###############################################################################
pc_CC = symbols('pc_CC')

# LH2, B1 y f: línea del hidrógeno (LH2)
# LO2, B2 y ox: línea del oxígeno (LO2)

# Presión en las bombas
delta_B1_f = pc_CC / (pi_refr * pi_inyCC_f) - pd_B1
delta_B2_ox = pc_CC / (pi_inyCC_ox) - pd_B2

# Presión de inyección en la precámara
p_iny_PC_f = delta_B1_f + pd_f
p_iny_PC_ox = delta_B2_ox + pd_ox

# Presión de inyección en la cámara de combustión
p_iny_CC_f = p_iny_PC_f * pi_refr
p_iny_CC_ox = p_iny_PC_ox

# Presión en la precámara
pc_PC = p_iny_PC_ox * pi_inyPC_ox

# Salida de la pre-cámara y comienzo de la turbina
p_et = pc_PC * pi_PC

# Salida de la turbina
p_st = p_et * pi_t_max


###############################################################################
# PASO 4: CÁLCULO DE LOS GASTOS MÁSICOS                                       #
###############################################################################
OF_CC_opt = symbols('OF_CC_opt')
m_PC_f = symbols('m_PC_f')
m_CC_f = symbols('m_CC_f')

# Relaciones de mezcla en la PC y CC
m_PC_ox = m_PC_f * OF_PC_opt
m_CC_ox = m_CC_f * OF_CC_opt

# Gastos másicos totales
m_f = m_PC_f + m_CC_f
m_ox = m_PC_ox + m_CC_ox

# Gasto másico en la turbina
m_t = m_PC_f + m_PC_ox


###############################################################################
# PASO 5: ECUACIÓN DE ACOPLAMIENTO                                            #
###############################################################################

# Ecuación de acoplamiento mecánico
tau_t = eta_t * Cp_prod_PC_kg * T_t_in_max * (1 - (pi_t_max)^((gamma_PC-1)/gamma_PC))
tau_B1_f = delta_B1_f / (eta_B1 * rho_H2)
tau_B2_ox = delta_B2_ox / (eta_B2 * rho_O2) 
eta_mec * m_t * tau_t = m_f * tau_B1_f + m_ox * tau_B2_ox




###############################################################################
# PASO 7: RELACIÓN DE MEZCLA EN LA LÍNEA PRINCIPAL                            #
###############################################################################
# POR AHORA DEJO QUE SE ELIJA EL TIPO DE MEZCLA EN LA CC, LUEGO SE OPTIMIZARÁ
# Seleccionamos el tipo de mezcla para la ecuación de combustión del hidrógeno en la CC
Tipo_mezcla_CC_valores = ["Rica", "Pobre", "Estequiométrica"]
Tipo_mezcla_CC = None

while Tipo_mezcla_CC not in Tipo_mezcla_CC_valores:
    print("Seleccione el tipo de mezcla en la pre-cámara:")
    print("1. Rica")
    print("2. Pobre")

    # Capturar la elección del usuario
    eleccion = input("Ingrese el número correspondiente (1 para Rica, 2 para Pobre, 3 para Estequiométrica): ")

    # Validar la entrada
    if eleccion == "1":
        Tipo_mezcla_CC = "Rica"
    elif eleccion == "2":
        Tipo_mezcla_CC = "Pobre"
    elif eleccion == "3":
        Tipo_mezcla_CC = "Estequiométrica"
    else:
        print("Entrada no válida. Por favor, intente de nuevo.")


# Asignación de las propiedades químicas según el tipo de mezcla seleccionado para la cámara de combustión
OF_CC, Cp_prod_CC, Mp_prod_CC, Cp_prod_CC_kg, delta_f_prod_CC, Q_comb_CC, Rg_CC, gamma_CC, Gamma_gamma_CC, Tc_CC = Propiedades_químicas(Tipo_mezcla_CC, Tipo_mezcla_CC_valores)

print("La mezcla seleccionada en la pre-cámara es: ", Tipo_mezcla_CC)



###############################################################################
# PASO 6: ECUACIÓN DEL EMPUJE                                                 #
###############################################################################
# FALTA TODA ESTA PARTE
# Valores para los próximos cálculos
Ps_Pc_pc = P_s / pc_PC;
Ps_Pc_cc = P_s / pc_CC;
Pamb_Pc_pc = 101325/pc_PC; % Pa/Pa
Pamb_Pc_cc = 101325/pc_CC;

# Velocidad característica
c_PC = sqrt(Rg_PC * Tc_PC) / Gamma_gamma_PC
c_CC = sqrt(Rg_CC * Tc_CC) / Gamma_gamma_CC

# Relación de áreas de la tobera
epsilon_PC = Gamma_gamma_PC / ((p_PC_s / pc_PC) ** (1 / gamma_PC) * sqrt(2 * gamma_PC / (gamma_PC - 1) * (1 - (p_PC_s / pc_PC) ** ((gamma_PC - 1) / gamma_PC))))
epsilon_CC = Gamma_gamma_CC / ((p_CC_s / pc_CC) ** (1 / gamma_CC) * sqrt(2 * gamma_CC / (gamma_CC - 1) * (1 - (p_CC_s / pc_CC) ** ((gamma_CC - 1) / gamma_CC))))

# Coeficiente de empuje
Ce_PC = Gamma_gamma_PC * sqrt(2 * gamma_PC / (gamma_PC - 1) * (1 - (p_PC_s / pc_PC) ** ((gamma_PC - 1) / gamma_PC))) + epsilon_PC * ((p_PC_s / pc_PC) - (p_adapt / pc_PC))
Ce_CC = Gamma_gamma_CC * sqrt(2 * gamma_CC / (gamma_CC - 1) * (1 - (p_CC_s / pc_CC) ** ((gamma_CC - 1) / gamma_CC))) + epsilon_CC * ((p_CC_s / pc_CC) - (p_adapt / pc_CC)) 

# Empuje específico
Isp_PC = c_PC * Ce_PC
Isp_CC = c_CC * Ce_CC


# Ecuación del empuje
Empuje = Isp_PC * (m_PC_f + m_PC_ox) * g_0 + Isp_CC * (m_CC_f + m_CC_ox) * g_0

# Empuje total
# E = E_CC + E_PC


###############################################################################
# PASO 8: OPTIMIZACIÓN                                                        #
###############################################################################



###############################################################################
# PASO 9: GRÁFICAS                                                            #
###############################################################################