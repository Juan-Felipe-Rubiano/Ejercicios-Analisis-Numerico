"""
Author: Juan Felipe Rubiano Santacruz
Description: Método de Gauss-Factorización LR o Factorización LUP para resolver sistemas de ecuaciones lineales
 de la forma Ax = b. El método consiste en factorizar la matriz A en el producto de una matriz triangular inferior L y una matriz triangular superior U,
    y luego resolver el sistema Ly = b utilizando sustitución hacia adelante, y posteriormente resolver el sistema Ux = y utilizando sustitución hacia atrás.
Constraints: La matriz A debe ser cuadrada, asegurando convergencia si es diagonalmente dominante
"""

import ast

def main():
    a_in = None
    b_in = None

    a_in = leer_matriz()
    n = len(a_in)
    if n == 0:
        raise ValueError("La matriz no puede estar vacía. Asegúrese de ingresar una matriz triangular superior con al menos una fila y una columna.")

    b_in = leer_vector(n)

    verificarCuadrada(a_in)
    verificarNumerica(a_in, b_in)

    try:
        p, l, u, b_permutaciones = factorizacion_lr(a_in, b_in)
        solucion = sustitucion_regresiva(u, b_permutaciones)
        print("\nMatriz P:\n")
        imprimir_matriz(p)
        print("\nMatriz L:\n")
        imprimir_matriz(l)
        print("\nMatriz U:\n")
        imprimir_matriz(u)
        print("\nLa solución del sistema es:", solucion)
    except ValueError as e:
        print("Error:", e)


def factorizacion_lr(matriz, vector):
    n = len(matriz)
    a = [fila[:] for fila in matriz]
    b = vector[:]
    p = list(range(n))

    for j in range(n):
        r = j
        for i in range(j+1, n):
            if abs(a[i][j]) > abs(a[r][j]):
                r = i
        if abs(a[r][j]) < 1e-12:
            raise ValueError("La matriz es singular. Asegúrese de que la matriz A sea no singular.")
        if r != j:
            p[j], p[r] = p[r], p[j]
            b[j], b[r] = b[r], b[j]
            for k in range(n):
                a[j][k], a[r][k] = a[r][k], a[j][k]
        for i in range(j+1, n):
            a[i][j] /= a[j][j]
            b[i] -= a[i][j] * b[j]
            for k in range(j+1, n):
                a[i][k] -= a[i][j] * a[j][k]
    if abs(a[n-1][n-1]) < 1e-12:
        raise ValueError("La matriz es singular. Asegúrese de que la matriz A sea no singular.")

    l = [[0.0] * n for _ in range(n)]
    u = [[0.0] * n for _ in range(n)]
    delta = [[0.0] * n for _ in range(n)]
    permutaciones = [[0.0] * n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            if i != j:
                delta[i][j] = 0.0
            else:
                delta[i][j] = 1.0
            if i <= j:
                l[i][j] = delta[i][j]
            else:
                l[i][j] = a[i][j]
            if i <= j:
                u[i][j] = a[i][j]
            else:
                u[i][j] = 0.0
            permutaciones[i][j] = delta[p[i]][j]

    return permutaciones, l, u, b


def sustitucion_regresiva(matriz, vector):
    n = len(matriz)
    x = [0] * n
    for i in range(n-1, -1, -1):
        suma = 0.0
        for j in range(i+1, n):
            suma += matriz[i][j] * x[j]

        x[i] = (vector[i] - suma) / matriz[i][i]

    return x


def leer_matriz():
    while True:
        try:
            entrada = input("Ingrese la matriz A (formato: [[a11, a12, ...], [a21, a22, ...], ...]):\n")
            matriz = ast.literal_eval(entrada)

            if not isinstance(matriz, list):
                raise ValueError

            n = len(matriz)

            for fila in matriz:
                if not isinstance(fila, list) or len(fila) != n:
                    raise ValueError

            return matriz
        except (ValueError, SyntaxError):
            print("Entrada no válida. Asegúrese de ingresar una matriz triangular superior en el formato correcto:")
            print("\n[[2, 3],[0, 1]] para una matriz 2x2 con r11=2, r12=3, r22=1")


def leer_vector(n):
    while True:
        try:
            entrada = input("Ingrese el vector c (formato: [c1, c2, ...]):\n")
            vector = ast.literal_eval(entrada)

            if not isinstance(vector, list) or len(vector) != n:
                raise ValueError

            return vector

        except (ValueError, SyntaxError):
            print("Entrada no válida. Asegúrese de ingresar un vector con el formato correcto:")
            print("\n[5, 3] para un vector de tamaño 2 con c1=5 y c2=3")


def verificarCuadrada(matriz):
    n = len(matriz)
    for fila in matriz:
        if len(fila) != n:
            raise ValueError("La matriz no es cuadrada. Asegúrese de que el número de filas y columnas sea igual.")


def verificarNumerica(matriz, vector):
    for fila in matriz:
        for elemento in fila:
            if not isinstance(elemento, (int, float)):
                raise ValueError("La matriz contiene elementos no numéricos. Asegúrese de que todos los elementos sean números.")
    for elemento in vector:
        if not isinstance(elemento, (int, float)):
            raise ValueError("El vector contiene elementos no numéricos. Asegúrese de que todos los elementos sean números.")


def imprimir_matriz(matriz):
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            print(f"{matriz[i][j]:.6f}", end=" ")
        print("\n")
    print("\n")


if __name__ == "__main__":
    main()