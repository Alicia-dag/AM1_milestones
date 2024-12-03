# -----------------------------------------------------------------------
#                            IMPORT
# -----------------------------------------------------------------------
import numpy as np
import matplotlib.pyplot as plt


# -----------------------------------------------------------------------
#                           FUNCTIONS
# -----------------------------------------------------------------------


def Newton(F, x_0, Fp, tol = 1e-4, maxiter=50):

    xn = x_0
    Error = tol + 1
    iter = 0

    while Error > tol:

        xn1 = xn - F(xn)/Fp(xn)
        Error = abs(xn-xn1)
        xn = xn1

        iter += 1
        if iter >= maxiter:
            print(f'Max number of iterations reached ({maxiter}). Returning...')
            return

    return xn


def jorge(x):
    return np.exp(x)-2*x-2 # Al usar la exp de numpy, se aceptan inputs tanto como escalar o vectorial (lista)


def dif_jorge(x):
    return np.exp(x)-2


def plot(x, y, method):

    # Define points (x, y) where vectors start
    x = np.array(x)
    y = np.array(y)

    # Create the scatter plot for points only
    plt.scatter(x, y, color='b', marker='o', s=1)  # 's' controls the size of the markers

    # Add labels and a title
    plt.xlabel('x (Position)')
    plt.ylabel('y (Position)')
    plt.title(f'Kepler solutions to {method} method')

    # Show the plot with a grid
    plt.grid()
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()


# -----------------------------------------------------------------------
#                    MAIN
# -----------------------------------------------------------------------
x = np.linspace(-2, 2, 1000)
y = jorge(x)

# plot(x, y, jorge.__name__)

Sol = Newton(jorge, -10, dif_jorge)
print("La solución es:", Sol)
print ("Residual = ", jorge(Sol))