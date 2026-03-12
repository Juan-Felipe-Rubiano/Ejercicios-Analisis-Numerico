"""
Author: Juan Felipe Rubiano Santacruz
Description: Método de la sustitución regresiva para resolver sistemas de ecuaciones lineales de la forma Rx = c,
 donde R es una matriz triangular superior
Constraints: La matriz R debe ser triangular superior, sin ceros en la diagonal
"""

import ast


def main():
    print("Para resolver un sistema de ecuaciones lineales de la forma Rx = c, donde R es una matriz triangular superior, digite los siguientes parámetros:\n")

    matriz = leer_matriz()
    n = len(matriz)
    if n == 0:
        raise ValueError("La matriz no puede estar vacía. Asegúrese de ingresar una matriz triangular superior con al menos una fila y una columna.")
    verificarCuadrada(matriz)
    verificarTriangular(matriz)
    verificarDiagonal(matriz)

    vector = leer_vector(n)
    verificarNumerica(matriz, vector)

    try:
        solucion = sustitucion_regresiva(matriz, vector)
        print("La solución del sistema es:", solucion)
    except ValueError as e:
        print("Error:", e)


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
            entrada = input("Ingrese la matriz R triangular superior (formato: [[r11, r12, ...], [0, r22, ...], ...]):\n")
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


def verificarTriangular(matriz):
    for i in range(len(matriz)):
        for j in range(i):
            if abs(matriz[i][j]) > 1e-12:
                raise ValueError("La matriz no es triangular superior. Asegúrese de que todos los elementos debajo de la diagonal sean cero.")



def verificarCuadrada(matriz):
    n = len(matriz)
    for fila in matriz:
        if len(fila) != n:
            raise ValueError("La matriz no es cuadrada. Asegúrese de que el número de filas y columnas sea igual.")


def verificarDiagonal(matriz):
    for i in range(len(matriz)):
        if abs(matriz[i][i]) < 1e-12:
            raise ValueError("La matriz tiene ceros en la diagonal. Asegúrese de que todos los elementos en la diagonal sean no nulos.")


def verificarNumerica(matriz, vector):
    for fila in matriz:
        for elemento in fila:
            if not isinstance(elemento, (int, float)):
                raise ValueError("La matriz contiene elementos no numéricos. Asegúrese de que todos los elementos sean números.")
    for elemento in vector:
        if not isinstance(elemento, (int, float)):
            raise ValueError("El vector contiene elementos no numéricos. Asegúrese de que todos los elementos sean números.")


if __name__ == "__main__":
    main()
