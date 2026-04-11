"""
Author: Juan Felipe Rubiano Santacruz
Description: Método de la regal compuesta del trapecio para calcular areas bajo la curva de una función dada.
El método consiste en dividir el intervalo de integración en n subintervalos, calcular el valor de la función en los extremos de cada subintervalo,
y luego multiplicar la suma de esos valores por el ancho del subintervalo y dividir por 2 para obtener el área de cada trapecio,
 sumando el área de todos los trapecios para obtener el área total bajo la curva.
Constraints: La función debe ser continua en el intervalo de integración. El número de subintervalos n debe ser un entero positivo.
"""
import sympy as sp

def main():
    f_in = None
    a_in = None
    b_in = None
    n_in = None
    print("Para calcular el área bajo la curva de una función utilizando la regla compuesta del trapecio, digite los siguientes parámetros:\n")
    while not f_in:
        f_in = input("Digite la función a integrar [FORMATO: utilice la notación de python. ej: x^2 es x**2 y 2x es 2*x]:\n")
    while a_in is None:
        a_in = float(input("Digite el límite inferior del intervalo de integración:\n"))
    while b_in is None:
        b_in = float(input("Digite el límite superior del intervalo de integración:\n"))
    while n_in is None:
        try:
            n_in = int(input("Digite el número de subintervalos para aplicar el método del trapecio (10 por defecto):\n") or 10)
            if n_in <= 0:
                print("El número de subintervalos debe ser un entero positivo. Intente de nuevo.")
                n_in = None
        except ValueError:
            print("Ingrese un número entero válido.")
    try:
        area = regla_trapecio(f_in, a_in, b_in, n_in)
        print("El área bajo la curva de la función es:", area)
    except ValueError as e:
        print("Error:", e)


def regla_trapecio(f_in, a, b, n):

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
    s_0 = f(a) + f(b)
    s_1 = 0.0

    for i in range(1, n):
        x_i = a + i * h
        s_1 += f(x_i)
    s = (h / 2) * s_0 + (h * s_1)
    return s


if __name__ == "__main__":
    main()
