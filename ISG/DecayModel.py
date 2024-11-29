from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt

def decay_model(r, t, Cd, A, rho, m, mu):
    v = np.sqrt(mu / r)
    drdt = -0.5 * Cd * A * rho * v**2 / m
    return drdt

# Parámetros
Cd = 2.2
A = 0.2  # m^2 (área frontal)
rho = 4.8e-11 # kg/m^3 (densidad a 850 km)
m = 25  # kg
mu = 3.986e14  # m^3/s^2 (constante gravitacional)
r0 = 6371e3 + 850e3  # Radio inicial
t = np.linspace(0, 6000*86400, 6000)  # 5000 días en segundos

# Integrar
r = odeint(decay_model, r0, t, args=(Cd, A, rho, m, mu))

# Graficar
plt.figure(figsize=(10, 6))
# Convertir tiempo de días a años (1 año = 365.25 días)
plt.plot(t / (86400 * 365.25), (r - 6371e3) / 1000)  # Tiempo en años, Altitud en km
plt.title("Orbital decay of a 6U cubesat of 25kg")
plt.xlabel("Time [years]")
plt.ylabel("Altitude [km]")
plt.xlim(0, 16) # Limitar el eje X de 0 a 15 años
# plt.ylim(0, 900)
plt.xticks(np.arange(0, 16, 3))  # Eje X de 5 en 5 (0, 5, 10, 15)
plt.yticks(np.arange(0, 1000 + 50, 200))  # Eje Y de 5 en 5
plt.grid()
plt.show()


plt.figure(figsize=(10, 6))
# Convertir tiempo de días a años (1 año = 365.25 días)
plt.plot(t / (86400 * 365.25), (r - 6371e3) / 1000)  # Tiempo en años, Altitud en km
plt.title("Orbital decay of a 6U cubesat of 25kg")
plt.xlabel("Time [years]")
plt.ylabel("Altitude [km]")
plt.xlim(0, 16) # Limitar el eje X de 0 a 15 años
# plt.ylim(0, 900)
plt.grid()
plt.show()