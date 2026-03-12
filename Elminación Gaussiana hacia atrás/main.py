"""
Author: Juan Felipe Rubiano Santacruz
Description: Método de la eliminación Gaussiana con sustitución hacia atrás para resolver sistemas de ecuaciones lineales
 de la forma Ax = b El método consiste en transformar la matriz A en una matriz triangular superior R mediante operaciones
 elementales, y luego resolver el sistema Rx = c utilizando sustitución hacia atrás.
Constraints: La matriz A debe ser no sigular. La matriz R debe ser triangular superior, sin ceros en la diagonal
"""

import ast
import sympy as sp

def main():
    print("Para resolver un sistema de ecuaciones lineales de la forma Rx = c, donde R es una matriz triangular superior, digite los siguientes parámetros:\n")

    matriz = leer_matriz()
    n = len(matriz)
    if n == 0:
        raise ValueError("La matriz no puede estar vacía. Asegúrese de ingresar una matriz triangular superior con al menos una fila y una columna.")
    verificarCuadrada(matriz)
    vector = leer_vector(n)
    verificarNumerica(matriz, vector)
    verificar_determinante(matriz)

    try:
        solucion = eliminacion_gaussiana(matriz, vector)
        print("La solución del sistema es:", solucion)
    except ValueError as e:
        print("Error:", e)


def eliminacion_gaussiana(matriz, vector):
    matriz = [fila[:] for fila in matriz]
    vector = vector[:]

    n = len(matriz)

    for i in range(n):
        p = i
        while p < n and abs(matriz[p][i]) < 1e-12:
            p += 1
        if p == n:
            raise ValueError("La matriz es singular o casi singular. Asegúrese de que la matriz A sea no singular.")
        if p != i:
            matriz[i], matriz[p] = matriz[p], matriz[i]
            vector[i], vector[p] = vector[p], vector[i]

        for j in range(i+1, n):
            m = matriz[j][i] / matriz[i][i]
            for k in range(i, n):
                matriz[j][k] -= m * matriz[i][k]
            vector[j] -= m * vector[i]
        if abs(matriz[i][i]) < 1e-12:
            raise ValueError("La matriz es singular o casi singular. Asegúrese de que la matriz A sea no singular.")

    x= [0] * n

    for i in range(n-1, -1, -1):
        suma = 0.0
        for j in range(i+1, n):
            suma += matriz[i][j] * x[j]

        x[i] = (vector[i] - suma) / matriz[i][i]
    return x



def leer_matriz():
    while True:
        try:
            entrada = input("Ingrese la matriz cuadrada A (formato: [[r11, r12, ...], [r21, r22, ...], ...]):\n")
            matriz = ast.literal_eval(entrada)

            if not isinstance(matriz, list):
                raise ValueError

            n = len(matriz)

            for fila in matriz:
                if not isinstance(fila, list) or len(fila) != n:
                    raise ValueError

            return matriz
        except (ValueError, SyntaxError):
            print("Entrada no válida. Asegúrese de ingresar una matriz cuadrada en el formato correcto:")
            print("\n[[2, 3],[5, 1]] para una matriz 2x2 con r11=2, r12=3, r22=1")


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


def verificar_determinante(matriz):
    det = sp.Matrix(matriz).det()
    if abs(det) < 1e-12:
        raise ValueError("La matriz es singular o casi singular. Asegúrese de que la matriz A sea no singular.")


if __name__ == "__main__":
    main()
