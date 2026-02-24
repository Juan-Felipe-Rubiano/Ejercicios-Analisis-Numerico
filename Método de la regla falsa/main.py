"""
Author: Juan Felipe Rubiano Santacruz
Description: Método de la regla falsa para encontrar raices de funciones
Constraints: La función debe ser continua en el intervalo [a, b] con f(a)*f(b) < 0
"""

import matplotlib
matplotlib.use("TkAgg")

import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from Salida import Salida


def main():
    f_in = None
    a_in = None
    b_in = None

    print("Para encontrar raices de una función digite los siguientes parámetros:\n")

    while not f_in:
        f_in = input("Digite la funcion a la que requiere encontrar raices [FORMATO: utilice la notación de python. ej: x^2 es x**2 y 2x es 2*x]:\n")
    while a_in is None:
        a_in = float(input("Digite el limite inferior del intervalo donde se encuentra definida la función:\n"))
    while b_in is None:
        b_in = float(input("Digite el limite superior del intervalo donde se encuentra definida la función:\n"))

    m_in = int(
        input("Digite el numero de iteraciones máximas a para aplicar la regla falsa en su función (10 por defecto):\n")
        or 10)
    epsilon_in = float(
        input("Digite la tolerancia para la solución que reciba [FORMATO: 1e-x, con x el número de decimales que desea] (1e-3 por defecto):\n")
        or 1e-3)

    try:
        raiz, historial, expr = regla_falsa(f_in, a_in, b_in, m_in, epsilon_in)
        print(Salida.MSJ_EXITO.value, raiz)
        graficar(expr, historial, raiz)
    except ValueError as e:
        print(Salida.MSJ_FRACASO.value, e)


def regla_falsa(f_in, a, b, m=10, epsilon=1e-3):
    historial = []
    i = 0
    x = sp.symbols('x')
    try:
        expr = sp.sympify(f_in)
    except sp.SympifyError:
        raise ValueError("La funcion ingresada por consola no es válida. Revise e intente de nuevo.\n")

    f = sp.lambdify(x, expr, "math")

    # Verificación de aplicabilidad del teorema
    if a >= b:
        raise ValueError("El intervalo no es correcto. Intente con un intervalo tal que a < b.")

    fa = f(a)
    fb = f(b)
    if fa * fb > 0:
        raise ValueError("La función no cambia de signo en [a,b]. Intente con otra función o ajuste el intervalo.")

    x_n_1 = None

    while i < m:

        if fb == fa:
            raise ValueError("Division entre cero. Intente con otra función o ajuste el intervalo.")

        x_n = calculo_xn(a, b, fa, fb)
        fx_n = f(x_n)

        historial.append((a,b,x_n,fa,fb,fx_n))

        if abs(fx_n) < epsilon:
            return x_n, historial, expr

        if fx_n * fa < 0:
            b = x_n
            fb = fx_n
        else:
            a = x_n
            fa = fx_n

        if x_n_1 is not None:
            error = calculo_error(x_n, x_n_1)
            if error < epsilon:
                return x_n, historial, expr

        x_n_1 = x_n
        i += 1
    raise ValueError("No se ha podido llegar a la tolerancia deseada en el número de iteraciones digitado")


def calculo_xn(a_n, b_n, fa_n, fb_n):
    return (a_n * fb_n - b_n * fa_n) / (fb_n - fa_n)


def calculo_error(x_n, x_n_1):
    if x_n != 0:
        return abs((x_n - x_n_1) / x_n)
    else:
        return abs(x_n - x_n_1)

def graficar(expr, historial, raiz):
    x = sp.symbols('x')
    f = sp.lambdify(x, expr, "numpy")

    puntos = [h[0] for h in historial] + [h[1] for h in historial]
    xmin, xmax = min(puntos) - 1, max(puntos) + 1

    X = np.linspace(xmin, xmax, 600)
    Y = f(X)

    plt.figure(figsize=(11, 7))

    # Curva
    plt.plot(X, Y, linewidth=2, label="f(x)")

    # Eje X
    plt.axhline(0)

    # iteraciones
    for i, (a, b, xn, fa, fb, fxn) in enumerate(historial):

        # Secante
        secante = fa + (fb - fa) * (X - a) / (b - a)
        plt.plot(X, secante, linestyle="--", alpha=0.5)

        # Puntos
        plt.scatter(a, fa, marker="o")
        plt.scatter(b, fb, marker="o")
        plt.scatter(xn, fxn, marker="x")

        # Líneas verticales del intervalo
        plt.axvline(a, linestyle=":", alpha=0.3)
        plt.axvline(b, linestyle=":", alpha=0.3)

    # Raíz
    plt.scatter(raiz, 0, s=120, label="Raíz aproximada")

    plt.title("Método de Regla Falsa")
    plt.legend()
    plt.grid()
    plt.show()
    #azul f, eje x, puntos azules extremos intervalo, linea es recta secante que los une y= f*an..., x punto donde secante intersecta curva nueva aproximacion, raiz final, vertical limites intervalo

if __name__ == "__main__":
    main()
