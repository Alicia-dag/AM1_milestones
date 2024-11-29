from numpy import sqrt, cos, pi, linspace, log, max, zeros, arctan, sin, cos
import matplotlib.pyplot as plt

################################################################## DATA ##############################################################
# Number of satellites in the constellation
ns = 9

# Constants
Rt = 6378000              # [m]
muT = 3.986 * 10**14      # [m^3/s^2]
J2 = 1.0827 * 10**(-3)    # [-]

# Semi-major axis of each orbit
a = 7222000               # [m]
ai = linspace(0, 100000, ns)
af = a + ai               # [m]
e = 1 - a / af            # [-]
T = 2* pi / sqrt(a**3 / muT) # Period of the orbit

# Mean motion of each satellite
n = sqrt(muT / af**7)     # [rad/s]
i = 85 / 180 * pi   # [rad]

# Gravitational acceleration
g0 = 9.81 # [m/s^2]

# Change in the RAAN
delta_omega = 22 * pi / 180  # Change in the RAAN [rad]

# Satellite mass
Ms = 25 # [kg] SOBRE_ESTIMATED

# Datos del Kick-Stage
M_KS = 40 # [kg]
Isp_KS = 325 # [s]
PL_KS = 3.633 # [kg]
# P_L debe ser mayor a 3.6330 kg para que el cohete pueda llevar a cabo las maniobras para los 9 satélites



############################################################## CALCULATIONS ###########################################################
# Days for each satellite to place in the correct RAAN
print(f"Satélite {1}: 0 días")
for idx, ai_val in enumerate(ai):
    denom = -((3/2) * J2 * Rt**2) / ((1 - e[idx]**2)**2) * n[idx] * cos(i)
    if denom != 0: 
        t = -(delta_omega / denom)
        t_days = t / 86400
        print(f"Satélite {idx+2}: {t_days:.2f} días")
    else:
        print(f"Satélite {idx+1}: División por cero en el cálculo")


# Impulses needed to place each satellite on the orbit that will correct its RAAN
def calculate_velocity_differences(a, af, muT):
    v_initial = sqrt(muT * (2 / a - 1 / a))  # Initial velocity for r = a
    v_final = sqrt(muT * (2 / a - 1 / af))   # Final velocities for each orbit
    delta_v = v_final - v_initial  # Differences in velocities
    return delta_v

# Calculate the velocity differences
delta_v_RAAN = calculate_velocity_differences(a, af, muT)
for idx, dv in enumerate(delta_v_RAAN):
    print(f"Velocity difference for maneouver {idx+1}: {dv:.2f} m/s")


# Isp calculations with a PL_KS given
mo_KS = M_KS + Ms * ns + PL_KS # [kg]
mf_KS = mo_KS - PL_KS  # [kg]

Isp_per_case = delta_v_RAAN / (g0 * log (mo_KS / mf_KS)) # [s]
Isp_needed = max (Isp_per_case)
print (f"Isp: {Isp_needed}")
if Isp_needed < Isp_KS:
    print ("The mission is possible using the Electron Launcher")
else:
    print ("The mission is NOT possible using the Electron Launcher")


#  Delta_Vs calculation to recircularize the orbit
delta_v = calculate_velocity_differences(a, af, muT) # Same ones as before


# Change in the AoP
delta_AoP = zeros(ns) 
for idx in range(ns):
    delta_AoP[idx] = -((3/4) * J2 * Rt**2) / ((1 - e[idx]**2)**2) * n[idx] * (5 * (cos(i))**2 - 1)

for idx in range(ns):
    print(f"Satellite {idx+1}: Delta AoP = {delta_AoP[idx]:.3e} rad/s")

# Impusles needed to change back the AoP
def calculate_velocity_differences_AoP (delta_AoP, e, af, muT):
    theta = delta_AoP / 2 # Half of the angle to change the AoP
    gamma = arctan (e * sin(theta)) / (1 ++ e * cos(theta))  # Angle between the velocity vector and the radial vector
    v_perp = muT / sqrt (muT * af * (1 - e**2)) * (1 + e * cos(theta))
    v_par = muT / sqrt (muT * af * (1 - e**2)) * e * sin(theta)
    v = sqrt(v_perp**2 + v_par**2)
    delta_v_AoP = 2 * v * sin(gamma)
    return delta_v_AoP

delta_v_AoP = calculate_velocity_differences_AoP (delta_AoP, e, af, muT)
print(delta_v_AoP)
for idx, dv_AoP in enumerate(delta_v_AoP):
    print(f"Delta V for AoP correction of maneouver {idx+1}: {dv_AoP:.6e} m/s")

# Total delta_v
delta_v_total = delta_v_RAAN + delta_v_AoP
for idx, dv_total in enumerate(delta_v_total):
    print(f"Total delta V for maneouver {idx+1}: {dv_total:.2f} m/s")

# Sum all terms of delta_v_total
total_delta_v = sum(delta_v_total)
print(f"Total delta V for all maneuvers: {total_delta_v:.2f} m/s")


# Change of the thruth anomaly (theta) after recircularization
t_delta_AoP = T / 360 * delta_AoP # Time to situate in delta_AoP
T_PO = T + t_delta_AoP # Total period of the phasing orbit
a_PO = muT * (T_PO / (2 * pi))**(3 / 2) # Semi-major axis of the phasing orbit
delta_v_PO = calculate_velocity_differences(a, af, muT) # Same ones as before
delta_v_PO_final = delta_v_PO + delta_v_PO

for idx, dv_PO in enumerate(delta_v_PO_final):
    print(f"Delta V for phasing orbit of maneouver {idx+1}: {dv_PO:.6e} m/s")

############################################################## PLOTS ################################################################
# Propulsion paylod vs af