
import sympy as sp
from Salida import Salida


def main():
    f_in = None
    x_0 = None
    x_1 = None

    while not f_in:
        f_in = input("Digite la funcion a la que requiere encontrar raices [FORMATO: utilice la notación de python. ej: x^2 es x**2 y 2x es 2*x]:\n")

    while x_0 is None:
        try:
            x_0 = float(input(
                "Digite el valor incial x_0:\n"))
        except ValueError:
            print("Por favor ingrese un número")

    while x_1 is None:
        try:
            x_1 = float(input(
                "Digite el valor incial x_1:\n"))
        except ValueError:
            print("Por favor ingrese un número")

    m_in = int(
        input(
            "Digite el numero de iteraciones máximas para utilizar el método de la secante en su función (10 por defecto):\n")
        or 10)
    epsilon_in = float(
        input(
            "Digite la tolerancia para la solución que reciba [FORMATO: 1e-x, con x el número de decimales que desea] (1e-3 por defecto):\n")
        or 1e-3)

    try:
        raiz = metodo_secante(f_in, x_0, x_1, m_in, epsilon_in)
        print(Salida.MSJ_EXITO.value, raiz)
    except ValueError as e:
        print(Salida.MSJ_FRACASO.value, e)


def metodo_secante(f_in, x_0, x_1, m=10, epsilon=1e-3):
    i = 0
    x = sp.symbols('x')

    try:
        expr = sp.sympify(f_in)
    except sp.SympifyError:
        raise ValueError("La funcion ingresada por consola no es válida. Revise e intente de nuevo.\n")

    f = sp.lambdify(x, expr, "math")

    x_n_m1 = x_0
    x_n = x_1

    while i < m:
        if f(x_n) == f(x_n_m1):
            raise ValueError("División entre cero en f(x_n) = f(x_{n-1})")

        x_n_1 = calculo_xn1(x_n_m1, x_n, f)

        if abs(f(x_n_1)) < epsilon:
            return x_n_1

        if calculo_error(x_n, x_n_1) < epsilon:
            return x_n_1

        x_n_m1 = x_n
        x_n = x_n_1

        i += 1

    raise ValueError("No se ha podido llegar a la tolerancia deseada en el número de iteraciones digitado")


def calculo_xn1(x_n_m1, x_n, f):
    f_n = f(x_n)
    f_nm1 = f(x_n_m1)
    return (x_n_m1*f_n - x_n*f_nm1)/(f_n - f_nm1)


def calculo_error(x_n, x_n_1):
    if x_n_1 != 0:
        return abs((x_n_1 - x_n) / x_n_1)
    else:
        return abs(x_n_1 - x_n)


if __name__ == "__main__":
    main()
