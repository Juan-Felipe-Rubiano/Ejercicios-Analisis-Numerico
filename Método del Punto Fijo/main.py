"""
Author: Juan Felipe Rubiano Santacruz
Description: Método del punto fijo para encontrar raíces de funciones
Constraints: La función g(x) debe cumplir |g'(p_0)| < 1 cerca del punto inicial para garantizar convergencia
"""

import sympy as sp
from Salida import Salida


def main():
    f_in = None
    p_0 = None

    print("Para encontrar raices de una función mediante el método del punto fijo, digite los siguientes parámetros:\n")

    tipo_entrada = None
    while tipo_entrada not in ['1', '2']:
        print("Qué desea ingresar?\n")
        print("1. f(x)")
        print("2. g(x)")
        tipo_entrada = input("Seleccione una opción (1 o 2): ").strip()
        if tipo_entrada not in ['1', '2']:
            print("Opción inválida. Por favor ingrese 1 o 2.")

    while not f_in or not f_in.strip():
        if tipo_entrada == '1':
            f_in = input(
                "\nDigite la función f(x) [FORMATO: utilice la notación de python. ej: x^2 es x**2 y 2x es 2*x]:\n")
        else:
            f_in = input(
                "\nDigite la función g(x) [FORMATO: utilice la notación de python. ej: x^2 es x**2 y 2x es 2*x]:\n")

    while p_0 is None:
        try:
            p_0 = float(input(
                "Digite el valor incial P_0:\n"))
        except ValueError:
            print("Por favor ingrese un número")

    m_in = int(
        input("Digite el numero de iteraciones máximas para utilizar el método del punto fijo en su función (10 por defecto):\n")
        or 10)
    epsilon_in = float(
        input(
            "Digite la tolerancia para la solución que reciba [FORMATO: 1e-x, con x el número de decimales que desea] (1e-3 por defecto):\n")
        or 1e-3)

    try:
        es_f = (tipo_entrada == '1')
        raiz = punto_fijo(f_in, p_0, m_in, epsilon_in, es_f)
        print(Salida.MSJ_EXITO.value, raiz)
    except ValueError as e:
        print(Salida.MSJ_FRACASO.value, e)


def punto_fijo(f_in, p_0, m = 10, epsilon=1e-3, es_funcion_f=True):
    x = sp.symbols('x')
    try:
        expr_ingresada = sp.sympify(f_in)
    except sp.SympifyError:
        raise ValueError("La función ingresada por consola no es válida. Revise e intente de nuevo.\n")
    if es_funcion_f:
        expr_g = x - expr_ingresada
    else:
        expr_g = expr_ingresada

    g_prima = sp.diff(expr_g, x)

    g_prima_eval = abs(g_prima.subs(x, p_0))
    g_prima_eval = float(g_prima_eval)

    if g_prima_eval >= 1:
        print("La función no cumple con el criterio de convergencia, por lo que podría no converger el método\n")
        continuar = input("Continuar? (si/no):\t")
        if continuar.lower() != "si":
            raise ValueError("Programa terminado por el usuario debido a posible no convergencia\n")

    g = sp.lambdify(x, expr_g, "math")

    i = 0
    p_n = p_0
    while i < m:
        p_n_1 = g(p_n)
        err = abs(p_n_1 - p_n)

        if err <= epsilon:
            return p_n_1
        p_n = p_n_1
        print(f"i={i+1}; p: {p_n_1}; error: {err}")

        i += 1
    raise ValueError("No se ha podido llegar a la tolerancia deseada en el número de iteraciones digitado")


if __name__ == "__main__":
    main()