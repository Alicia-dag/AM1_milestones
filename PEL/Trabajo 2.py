from sympy import symbols, solve, Min, Eq, N
from scipy.optimize import fsolve
from numpy import sqrt
import numpy as arange
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


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
Empuje_SL = 50000 # [kg]
Empuje_SL = Empuje_SL * 9.81 # [N]
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
OF_CC_st = 0.5 * (M_O2 / M_H2) # Relación estequiométrica [adim]


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

Función_1 = eta_mec * m_t * tau_t - m_f * tau_B1_f - m_ox * tau_B2_ox


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
# PASO 6: ECUACIÓN DEL EMPUJE A NIVEL DEL MAR                                 #
###############################################################################

# Valores para los próximos cálculos
p_SL = 101325 # Presión al nivel del mar [Pa]

# Velocidad característica
c_PC = sqrt(Rg_PC * Tc_PC) / Gamma_gamma_PC
c_CC = sqrt(Rg_CC * Tc_CC) / Gamma_gamma_CC

# Relación de áreas de la tobera
epsilon_PC = Gamma_gamma_PC / ((p_PC_s / pc_PC) ** (1 / gamma_PC) * sqrt(2 * gamma_PC / (gamma_PC - 1) * (1 - (p_PC_s / pc_PC) ** ((gamma_PC - 1) / gamma_PC))))
epsilon_CC = Gamma_gamma_CC / ((p_CC_s / pc_CC) ** (1 / gamma_CC) * sqrt(2 * gamma_CC / (gamma_CC - 1) * (1 - (p_CC_s / pc_CC) ** ((gamma_CC - 1) / gamma_CC))))

# Coeficiente de empuje
Ce_PC = Gamma_gamma_PC * sqrt(2 * gamma_PC / (gamma_PC - 1) * (1 - (p_PC_s / pc_PC) ** ((gamma_PC - 1) / gamma_PC))) + epsilon_PC * ((p_PC_s / pc_PC) - (p_SL / pc_PC))
Ce_CC = Gamma_gamma_CC * sqrt(2 * gamma_CC / (gamma_CC - 1) * (1 - (p_CC_s / pc_CC) ** ((gamma_CC - 1) / gamma_CC))) + epsilon_CC * ((p_CC_s / pc_CC) - (p_SL / pc_CC)) 

# Empuje específico
Isp_PC = c_PC * Ce_PC
Isp_CC = c_CC * Ce_CC


# Ecuación del empuje
Empuje_SL = Isp_PC * (m_PC_f + m_PC_ox) * g_0 + Isp_CC * (m_CC_f + m_CC_ox) * g_0

Funcion_2 = Empuje_SL  - Isp_PC * (m_PC_f + m_PC_ox) * g_0 - Isp_CC * (m_CC_f + m_CC_ox) * g_0

# Empuje total
# E = E_CC + E_PC


###############################################################################
# PASO 8: OPTIMIZACIÓN                                                        #
###############################################################################

# Función de optimización

def Optimización (OF_CC_st, OF_CC, OF_ini, paso_OF, OF_fin, x_CC, M_H2, M_O2, a, b, c, Pc_CC, pc_ini, paso_pc, pc_fin, Funcion_1, Funcion_2, M_CC_f, Ce_CC):
    
    for OF_CC in arange(OF_ini, OF_fin + paso_OF, paso_OF):
        x_CC = OF_CC * M_H2 / M_O2
        
        if OF_CC >= OF_CC_st: # Mezcla rica
            a = 2 * x_CC
            b = 1 - 2 * x_CC
            c = 0
            Mezcla = 'Rica'
        else: # Mezcla pobre
            a = 1
            b = 0
            c = x_CC - 1 / 2
            Mezcla = 'Pobre'
        
        # Iteración en Pc_CC
        for Pc_CC in arange(pc_ini, pc_fin + paso_pc, paso_pc):
            # Definición simbólica
            m_CC_f, m_PC_f = symbols('m_CC_f m_PC_f')
            Funciones = [Funcion_1, Funcion_2]
            
            # Resolver el sistema de ecuaciones
            Soluciones = solve(Funciones, (m_CC_f, m_PC_f))
            mf_CC_sol = N(Soluciones[m_CC_f])
            pc_sol = N(Soluciones[m_PC_f])
            
            # Sustitución de las soluciones en cada una de las ecuaciones
            Isp = N(((m_CC_f + m_CC_ox) * Isp_CC + m_t * Isp_PC) / (m_f + m_ox))
            Km = N((k_ox * m_ox / m_f + k_f) / (m_ox / m_f + 1))
            rho_p = N((m_ox / m_f + 1) / ((m_ox / m_f) / rho_O2 + 1 / rho_H2))
            c_cc = N(c_CC)
            Ce = N(Ce_CC)
            MO = N(m_CC_ox + m_PC_ox)
            MO_principal = N(m_CC_ox)
            MO_sangrado = N(m_PC_ox)
            MF = N(m_CC_f + m_PC_f)
            MF_principal = N(m_CC_f)
            MF_sangrado = N(m_PC_f)
            
            
            # Resultados almacenados en una lista
            resultados = []
            
            resultados.append({
                'OF_CC': OF_CC,
                'pc_CC': pc_CC,
                'Isp': Isp,
                'Km': Km,
                'rho_p': rho_p,
                'c_cc': c_CC,
                'Ce': Ce,
                'MO': MO,
                'MO_principal': MO_principal,
                'MO_sangrado': MO_sangrado,
                'MF': MF,
                'MF_principal': MF_principal,
                'MF_sangrado': MF_sangrado
                })
    
    # Retornar resultados
    return Isp, Km, rho_p, c_CC, Ce, MO, MO_principal, MO_sangrado, MF, MF_principal, MF_sangrado


###############################################################################
# PASO 9: GRÁFICAS                                                            #
###############################################################################

# # Figura 1: Isp
# fig1 = plt.figure(1)
# ax1 = fig1.add_subplot(111, projection='3d')
# ax1.plot_surface(vx, vy, Isp, cmap='viridis')
# ax1.set_title('Isp')
# ax1.set_xlabel('Pc [MPa]')
# ax1.set_ylabel('O/F')
# ax1.set_zlabel('Isp [m/s]')
# plt.colorbar(ax1.plot_surface(vx, vy, Isp, cmap='viridis'), ax=ax1, shrink=0.5)

# # Figura 2: Isp / (1 + Km)
# fig2 = plt.figure(2)
# ax2 = fig2.add_subplot(111, projection='3d')
# ax2.plot_surface(vx, vy, Isp / (1 + Km), cmap='viridis')
# ax2.set_title('Isp/(1+Km)')
# ax2.set_xlabel('Pc [MPa]')
# ax2.set_ylabel('O/F')
# ax2.set_zlabel('Isp/(1+Km) [m/s]')
# plt.colorbar(ax2.plot_surface(vx, vy, Isp / (1 + Km), cmap='viridis'), ax=ax2, shrink=0.5)

# # Figura 3: Isp * rho_p
# fig3 = plt.figure(3)
# ax3 = fig3.add_subplot(111, projection='3d')
# ax3.plot_surface(vx, vy, Isp * rho_p, cmap='viridis')
# ax3.set_title('Isp*rho_m')
# ax3.set_xlabel('Pc [MPa]')
# ax3.set_ylabel('O/F')
# ax3.set_zlabel('Isp*Densidad [Kg/(m^2*s)]')
# plt.colorbar(ax3.plot_surface(vx, vy, Isp * rho_p, cmap='viridis'), ax=ax3, shrink=0.5)

# # Figura 5: c*
# fig5 = plt.figure(5)
# ax5 = fig5.add_subplot(111, projection='3d')
# ax5.plot_surface(vx, vy, c_estrella, cmap='viridis')
# ax5.set_title('c*')
# ax5.set_xlabel('Pc [MPa]')
# ax5.set_ylabel('O/F')
# ax5.set_zlabel('c* [m/s]')
# plt.colorbar(ax5.plot_surface(vx, vy, c_estrella, cmap='viridis'), ax=ax5, shrink=0.5)

# # Figura 6: C_empuje
# fig6 = plt.figure(6)
# ax6 = fig6.add_subplot(111, projection='3d')
# ax6.plot_surface(vx, vy, C_empuje, cmap='viridis')
# ax6.set_title('C_E')
# ax6.set_xlabel('Pc [MPa]')
# ax6.set_ylabel('O/F')
# ax6.set_zlabel('C_E')
# plt.colorbar(ax6.plot_surface(vx, vy, C_empuje, cmap='viridis'), ax=ax6, shrink=0.5)

# # Figura 7: MO_principal
# fig7 = plt.figure(7)
# ax7 = fig7.add_subplot(111, projection='3d')
# ax7.plot_surface(vx, vy, MO_principal, cmap='viridis')
# ax7.set_title('Gasto Oxidante linea principal')
# ax7.set_xlabel('Pc [MPa]')
# ax7.set_ylabel('O/F')
# ax7.set_zlabel('MO principal [kg/s]')
# plt.colorbar(ax7.plot_surface(vx, vy, MO_principal, cmap='viridis'), ax=ax7, shrink=0.5)

# # Figura 8: MO_sangrado
# fig8 = plt.figure(8)
# ax8 = fig8.add_subplot(111, projection='3d')
# ax8.plot_surface(vx, vy, MO_sangrado, cmap='viridis')
# ax8.set_title('Gasto Oxidante sangrado')
# ax8.set_xlabel('Pc [MPa]')
# ax8.set_ylabel('O/F')
# ax8.set_zlabel('MO sangrado [kg/s]')
# plt.colorbar(ax8.plot_surface(vx, vy, MO_sangrado, cmap='viridis'), ax=ax8, shrink=0.5)

# # Figura 9: MF_sangrado
# fig9 = plt.figure(9)
# ax9 = fig9.add_subplot(111, projection='3d')
# ax9.plot_surface(vx, vy, MF_sangrado, cmap='viridis')
# ax9.set_title('Gasto Fuel sangrado')
# ax9.set_xlabel('Pc [MPa]')
# ax9.set_ylabel('O/F')
# ax9.set_zlabel('MF sangrado [kg/s]')
# plt.colorbar(ax9.plot_surface(vx, vy, MF_sangrado, cmap='viridis'), ax=ax9, shrink=0.5)

# # Figura 10: MF_principal
# fig10 = plt.figure(10)
# ax10 = fig10.add_subplot(111, projection='3d')
# ax10.plot_surface(vx, vy, MF_principal, cmap='viridis')
# ax10.set_title('Gasto Fuel linea principal')
# ax10.set_xlabel('Pc [MPa]')
# ax10.set_ylabel('O/F')
# ax10.set_zlabel('MF principal [kg/s]')
# plt.colorbar(ax10.plot_surface(vx, vy, MF_principal, cmap='viridis'), ax=ax10, shrink=0.5)

# # Mostrar todas las figuras
# plt.show()