
# DATOS DEL ENUNCIADO DEL TRABAJO 2 DE PEL

# Propiedades de las sustancias
M_H2 = 2.016  # Masa molar del hidrógeno [g/kmol]
M_H2 = M_H2 / 1000  # Masa molar del hidrógeno [kg/mol]
M_O2 = 31.998  # Masa molar del oxígeno [gk/mol]
M_O2 = M_O2 / 1000  # Masa molar del oxígeno [kg/mol]
M_H2O = 18.015  # Masa molar del agua [g/kmol]
M_H2O = M_H2O / 1000  # Masa molar del agua [kg/mol]

Cp_H2 = 36.11 # Capacidad calorífica del hidrógeno [J/(mol*K)]
Cp_O2 = 39.07 # Capacidad calorífica del oxígeno [J/(mol*K)]
Cp_H2O = 54.32 # Capacidad calorífica del agua [J/(mol*K)]

delta_f_H2 = 0 # Entalpía de formación del hidrógeno [J/mol]
delta_f_O2 = 0 # Entalpía de formación del oxígeno [J/mol]
delta_f_H2O = -241818 # Entalpía de formación del agua [J/mol]

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