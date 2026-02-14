"""
Author: Juan Felipe Rubiano Santacruz
Description: Método de la regla falsa para encontrar raices de funciones
Constraints: La función debe ser continua en el intervalo [a, b] con f(a)*f(b) < 0
"""

import sympy as sp
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
        raiz = regla_falsa(f_in, a_in, b_in, m_in, epsilon_in)
        print(Salida.MSJ_EXITO.value, raiz)
    except ValueError as e:
        print(Salida.MSJ_FRACASO.value, e)


def regla_falsa(f_in, a, b, m=10, epsilon=1e-3):
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

        if abs(fx_n) < epsilon:
            return x_n

        if fx_n * fa < 0:
            b = x_n
            fb = fx_n
        else:
            a = x_n
            fa = fx_n

        if x_n_1 is not None:
            error = calculo_error(x_n, x_n_1)
            if error < epsilon:
                return x_n

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


if __name__ == "__main__":
    main()
