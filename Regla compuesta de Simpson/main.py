"""
Author: Juan Felipe Rubiano Santacruz
Description: Método de la regla compuesta de simpson para calcular areas bajo la curva de una función dada.
El método consiste en dividir el intervalo de integración en n subintervalos,
 calcular el valor de la función en los extremos y en el punto medio de cada subintervalo,
Constraints: La función debe ser al menos dos veces diferenciable en el intervalo de integración. El número de subintervalos n debe ser un entero positivo par.
"""

import sympy as sp


def main():
    f_in = None
    a_in = None
    b_in = None
    n_in = None
    print(
        "Para calcular el área bajo la curva de una función utilizando la regla compuesta de simpson, digite los siguientes parámetros:\n")
    while not f_in:
        f_in = input(
            "Digite la función a integrar [FORMATO: utilice la notación de python. ej: x^2 es x**2 y 2x es 2*x]:\n")
    while a_in is None:
        try:
            a_in = float(input("Digite el límite inferior del intervalo de integración:\n"))
        except ValueError:
            print("Ingrese un número válido.")
    while b_in is None:
        try:
            b_in = float(input("Digite el límite superior del intervalo de integración:\n"))
        except ValueError:
            print("Ingrese un número válido.")
    while n_in is None:
        try:
            n_in = int(input(
                "Digite el número de subintervalos para aplicar el método de simpson (10 por defecto):\n") or 10)
            if n_in <= 0:
                print("El número de subintervalos debe ser un entero positivo. Intente de nuevo.")
                n_in = None
        except ValueError:
            print("Ingrese un número entero válido.")

    if n_in % 2 != 0:
        print(f"Numero de iteraciones es impar. Se ha aumentado a n = {n_in*2}")
        n_in *= 2

    try:
        area = regla_simpson(f_in, a_in, b_in, n_in)
        print("El área bajo la curva de la función es:", area)
    except ValueError as e:
        print("Error:", e)


def regla_simpson(f_in, a, b, n):

    x = sp.symbols('x')
    try:
        expr = sp.sympify(f_in)
    except sp.SympifyError:
        raise ValueError("La función ingresada por consola no es válida. Revise e intente de nuevo.\n")

    f = sp.lambdify(x, expr, "numpy")

    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise ValueError("Los límites de integración deben ser números. Intente de nuevo.")

    if a >= b:
        raise ValueError("El intervalo no es correcto. Intente con un intervalo tal que a < b.")

    if n <= 0:
        raise ValueError("El número de subintervalos debe ser un entero positivo. Intente de nuevo.")

    h = (b - a) / n
    try:
        s_0 = f(a) + f(b)
    except Exception as e:
        raise ValueError(f"Error al evaluar la función en los extremos del intervalo: {e}")
    s_1 = 0.0
    s_2 = 0.0

    for i in range(1, n):
        x_i = a + i*h
        try:
            f_val = f(x_i)
        except Exception as e:
            raise ValueError(f"Error en x={x_i}: {e}")
        if i % 2 == 0:
            s_2 += f_val
        else:
            s_1 += f_val

    s = (h / 3) * (s_0 + (4 * s_1) + (2 * s_2))
    return s


if __name__ == "__main__":
    main()
