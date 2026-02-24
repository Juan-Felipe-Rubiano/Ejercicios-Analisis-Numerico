"""
Author: Juan Felipe Rubiano Santacruz
Description: Método de Newton-Raphson para encontrar raices de funciones
Constraints: La función debe ser diferenciable en el intervalo considerado
 y la derivada no debe ser cero en el punto inicial para garantizar convergencia
"""

import matplotlib
matplotlib.use("TkAgg")

import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from Salida import Salida


def main():
    f_in = None
    x_0 = None

    while not f_in:
        f_in = input("Digite la funcion a la que requiere encontrar raices [FORMATO: utilice la notación de python. ej: x^2 es x**2 y 2x es 2*x]:\n")

    while x_0 is None:
        try:
            x_0 = float(input(
                "Digite el valor incial x_0:\n"))
        except ValueError:
            print("Por favor ingrese un número")

    m_in = int(
        input(
            "Digite el numero de iteraciones máximas para utilizar el método de Newton-Raphson en su función (10 por defecto):\n")
        or 10)
    epsilon_in = float(
        input(
            "Digite la tolerancia para la solución que reciba [FORMATO: 1e-x, con x el número de decimales que desea] (1e-3 por defecto):\n")
        or 1e-3)
    try:
        raiz, historial, expr = newton_raphson(f_in, x_0, m_in, epsilon_in)
        print(Salida.MSJ_EXITO.value, raiz)
        graficar(expr, historial, raiz)
    except ValueError as e:
        print(Salida.MSJ_FRACASO.value, e)


def newton_raphson(f_in, x_0, m=10, epsilon=1e-3):
    historial = []
    i = 0
    x = sp.symbols('x')
    try:
        expr = sp.sympify(f_in)
    except sp.SympifyError:
        raise ValueError("La funcion ingresada por consola no es válida. Revise e intente de nuevo.\n")
    f = sp.lambdify(x, expr, "numpy")

    f_prima = sp.diff(expr, x)
    f_prima_fun = sp.lambdify(x, f_prima, "numpy")

    while i < m:
        f_x_0 = f(x_0)
        f_prima_x_0 = f_prima_fun(x_0)

        if f_prima_x_0 == 0:
            raise ValueError("La derivada es cero en x_0. Intente con otro valor inicial.")

        historial.append((x_0, f_x_0, f_prima_x_0))

        x_n_1 = x_0 - f_x_0 / f_prima_x_0

        if abs(x_n_1 - x_0) < epsilon:
            historial.append((x_n_1, f(x_n_1), f_prima_fun(x_n_1)))
            return x_n_1, historial, expr

        if abs(f(x_n_1)) < epsilon:
            historial.append((x_n_1, f(x_n_1), f_prima_fun(x_n_1)))
            return x_n_1, historial, expr

        x_0 = x_n_1
        i += 1
    raise ValueError("No se ha podido llegar a la tolerancia deseada en el número de iteraciones digitado")


def graficar(expr, historial, raiz):
    x = sp.symbols('x')
    f = sp.lambdify(x, expr, "numpy")

    xs = [p[0] for p in historial]

    xmin = min(xs) - abs(min(xs)) * 0.5 - 1
    xmax = max(xs) + abs(max(xs)) * 0.5 + 1

    X = np.linspace(xmin, xmax, 400)
    Y = f(X)

    plt.figure(figsize=(11, 7))

    # Curva de la función
    plt.plot(X, Y, label="f(x)", linewidth=2)

    # Eje X
    plt.axhline(0)

    colors = plt.cm.plasma(np.linspace(0, 1, len(historial)))

    for i, ((x_n, f_n, pendiente), c) in enumerate(zip(historial, colors)):

        # Tangente
        tangente = f_n + pendiente * (X - x_n)
        plt.plot(X, tangente, linestyle="--", color=c, alpha=0.7)

        # Punto sobre la curva
        plt.scatter(x_n, f_n, color=c, zorder=3)

        # Etiqueta iteración
        plt.text(x_n, f_n, f"x{i}", fontsize=10, color=c)

        # Intersección con eje X
        x_inter = x_n - f_n / pendiente
        plt.scatter(x_inter, 0, marker="x", s=70, color=c)


        plt.arrow(
            x_n, f_n,
            x_inter - x_n, -f_n,
            head_width=0.05,
            length_includes_head=True,
            color=c,
            alpha=0.6
        )


    plt.scatter(raiz, 0, marker="o", s=120, color="pink", label="Raíz aproximada")

    plt.title("Método de Newton-Raphson", fontsize=14)
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.legend()
    plt.grid(True)

    plt.show()
#curva azul: f, tangentes de colores, puntos numerados de iteracion, X intersecciones con eje x, flechas indicando el paso de cada iteración, punto rosa indicando la raíz aproximada

if __name__ == "__main__":
    main()
