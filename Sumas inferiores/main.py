"""
Author: Juan Felipe Rubiano Santacruz
Description: Método de las sumas inferiores para calcular areas bajo la curva de una función dada.
El método consiste en dividir el intervalo de integración en n subintervalos, calcular el valor de la función en el
extremo izquierdo de cada subintervalo, y luego multiplicar ese valor por el ancho del subintervalo para obtener la suma inferior.
Constraints: La función debe ser continua en el intervalo de integración. El número de subintervalos n debe ser un entero positivo.
"""
import sympy as sp


def main():
    f_in = None
    a_in = None
    b_in = None
    n_in = None
    print("Para calcular el área bajo la curva de una función utilizando el método de las sumas inferiores, digite los siguientes parámetros:\n")
    while not f_in:
        f_in = input("Digite la función a integrar [FORMATO: utilice la notación de python. ej: x^2 es x**2 y 2x es 2*x]:\n")
    while a_in is None:
        a_in = float(input("Digite el límite inferior del intervalo de integración:\n"))
    while b_in is None:
        b_in = float(input("Digite el límite superior del intervalo de integración:\n"))
    while n_in is None:
        try:
            n_in = int(input("Digite el número de subintervalos para aplicar el método de las sumas inferiores (10 por defecto):\n") or 10)
            if n_in <= 0:
                print("El número de subintervalos debe ser un entero positivo. Intente de nuevo.")
                n_in = None
        except ValueError:
            print("Ingrese un número entero válido.")
    try:
        area = sumas_inferiores(f_in, a_in, b_in, n_in)
        print("El área bajo la curva de la función es:", area)
    except ValueError as e:
        print("Error:", e)


def sumas_inferiores(f_in, a, b, n):
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

    delta_x = (b - a) / n
    s = 0.0

    for i in range(n):
        x_i = a + i * delta_x
        x_i_m_1 = x_i + delta_x
        try:
            f_x_i = f(x_i)
            f_x_i_m_1 = f(x_i_m_1)
        except Exception as e:
            raise ValueError(f"Error al evaluar la función en x={x_i} o x={x_i_m_1}. Asegúrese de que la función sea continua"
                             f" en el intervalo de integración. Detalles del error: {e}")
        f_min = min(f_x_i, f_x_i_m_1)
        s += f_min * delta_x

    return s


if __name__ == "__main__":
    main()
