"""
Author: Juan Felipe Rubiano Santacruz
Description: Método de Newton-Raphson para encontrar raices de funciones
Constraints: La función debe ser diferenciable en el intervalo considerado
 y la derivada no debe ser cero en el punto inicial para garantizar convergencia
"""

import sympy as sp
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
        raiz = newton_raphson(f_in, x_0, m_in, epsilon_in)
        print(Salida.MSJ_EXITO.value, raiz)
    except ValueError as e:
        print(Salida.MSJ_FRACASO.value, e)


def newton_raphson(f_in, x_0, m=10, epsilon=1e-3):
    i = 0
    x = sp.symbols('x')
    try:
        expr = sp.sympify(f_in)
    except sp.SympifyError:
        raise ValueError("La funcion ingresada por consola no es válida. Revise e intente de nuevo.\n")
    f = sp.lambdify(x, expr, "math")

    f_prima = sp.diff(expr, x)
    f_prima_fun = sp.lambdify(x, f_prima, "math")

    while i < m:
        f_x_0 = f(x_0)
        f_prima_x_0 = f_prima_fun(x_0)

        if f_prima_x_0 == 0:
            raise ValueError("La derivada es cero en x_0. Intente con otro valor inicial.")

        x_n_1 = x_0 - f_x_0 / f_prima_x_0

        if abs(x_n_1 - x_0) < epsilon:
            return x_n_1

        if abs(f(x_n_1)) < epsilon:
            return x_n_1

        x_0 = x_n_1
        i += 1
    raise ValueError("No se ha podido llegar a la tolerancia deseada en el número de iteraciones digitado")


if __name__ == "__main__":
    main()
