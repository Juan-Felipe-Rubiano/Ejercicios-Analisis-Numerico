"""
Author: Juan Felipe Rubiano Santacruz
Description: Método de bisección para encontrar raíces de funciones
Constraints La función debe ser continua en el intervalo [a, b] con f(a)*f(b) < 0
"""

from Salida import Salida
import sympy as sp
"""
@:param f: función para la cual se desea encontrar la raíz
@:param a: límite inferior del intervalo
@:param b: límite superior del intervalo
@:param epsilon: tolerancia para la aproximación de la raíz (opcional, por defecto 1e-3)
@:param M: número máximo de iteraciones para evitar bucles infinitos
@:brief Este programa implementa el método de bisección para encontrar una raíz de dada función f
 continua en el intervalo [a, b]
"""
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
        input("Digite el numero de iteraciones máximas a para biseccionar su función (10 por defecto):\n")
        or 10)
    epsilon_in = float(
        input("Digite la tolerancia para la solución que reciba [FORMATO: 1e-x, con x el número de decimales que desea] (1^-3 por defecto):\n")
        or 1e-3)

    try:
        raiz = biseccion(f_in, a_in, b_in, m_in, epsilon_in)
        print(Salida.MSJ_EXITO.value, raiz)
    except ValueError as e:
        print(Salida.MSJ_FRACASO.value, e)


def biseccion(f_in, a, b, m=10, epsilon=1e-3):
    i = 0
    x = sp.symbols('x')
    try:
        expr = sp.sympify(f_in)
    except sp.SympifyError:
        raise ValueError("La funcion ingresada por consola no es válida. Revise e intente de nuevo.\n")

    f = sp.lambdify(x, expr, "math")

    #Verificación de aplicabilidad del teorema
    if a >= b:
        raise ValueError("El intervalo no es correcto. Intente con un intervalo tal que a < b.")
    fa = f(a)
    fb = f(b)
    if fa * fb > 0:
        raise ValueError("La función no cambia de signo en [a,b]. Intente con otra función o ajuste el intervalo.")

    while i < m:            #cumplir maximo de iteraciones
        p = a + ((b-a)/2)   #centro actual
        fp = f(p)
        if fp == 0 or (b-a)/2 < epsilon or abs(fp) < epsilon:
            return p

        if fa * fp > 0:         #si la raiz esta en [p, b]
            a = p
            fa = fp
        else:                   #si la raiz esta en [a, p]
            b = p
            fb = fp
        i += 1

    raise ValueError("No se ha podido llegar a la tolerancia deseada en el número de iteraciones digitado")

if __name__ == "__main__":
    main()