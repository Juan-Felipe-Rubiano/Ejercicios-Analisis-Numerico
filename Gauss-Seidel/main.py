"""
Author: Juan Felipe Rubiano Santacruz
Description: Método de Gauss Seidel para resolver sistemas de ecuaciones lineales
 de la forma Ax = b El método consiste en iterar sobre cada variable,
  actualizando su valor utilizando los valores más recientes de las otras variables.
Constraints: La matriz A debe ser cuadrada, asegurando convergencia si es diagonalmente dominante
"""

import ast
import sympy as sp
import numpy as np


def main():

    n_ec_in = None
    n_vars_in = None
    a_in = None
    b_in = None
    semilla_in = None
    eps = None
    n_itr_max = None

    print("Para resolver un sistema de ecuaciones lineaes de la forma Ax = b utilizando el método de Gauss-Seidel, digite los siguientes parámetros:\n")

    while n_ec_in is None:
        try:
            n_ec_in = int(input("Digite el número de ecuaciones del sistema:\n"))
        except ValueError:
            print("Ingrese un número entero válido.")

    while n_vars_in is None:
        try:
            n_vars_in = int(input("Digite el número de variables del sistema:\n"))
        except ValueError:
            print("Ingrese un número entero válido.")
    if(n_ec_in != n_vars_in):
        print("Error: El número de ecuaciones debe ser igual al número de variables para que la matriz A sea cuadrada")
        return

    a_in = leer_matriz(n_ec_in, n_vars_in)
    b_in = leer_vector(n_ec_in, "b")
    semilla_in = leer_vector(n_vars_in, "semilla")
    if(len(semilla_in) != n_vars_in):
        print(f"Error: La semilla debe tener {n_vars_in} elementos. Se utilizará una semilla por defecto de ceros.")
        semilla_in = [0] * n_vars_in

    eps = float(
        input("Digite la tolerancia para la solución que reciba [FORMATO: 1e-x, con x el número de decimales que desea] (1e-3 por defecto):\n")
        or 1e-3)
    if eps <= 0:
        print("La tolerancia debe ser un número positivo. Se utilizará el valor por defecto de 1e-3.")
        eps = 1e-3

    n_itr_max = int(
        input("Digite el número máximo de iteraciones para utilizar el método de Gauss-Seidel en su sistema (10 por defecto):\n")
        or 10)

    verificarCuadrada(a_in)
    verificarNumerica(a_in, b_in)
    verificar_determinante(a_in)

    es_dominante = verificar_diagonal_dominante(a_in)
    if not es_dominante:
        print("La matriz A no es diagonalmente dominante. El método de Gauss-Seidel puede no converger. Desea continuar?(s/n)")
        continuar = input()
        if continuar.lower() not in ['s', 'si']:
            print("Ha decidido no continuar debido a la falta de diagonal dominante en la matriz A. Por favor revise su matriz e intente de nuevo.")
            return

    verificar_diagonal_no_cero(a_in)

    try:
        solucion = gauss_seidel(a_in, b_in, semilla_in, eps, n_itr_max)
        print("La solución del sistema es:", solucion)
    except ValueError as e:
        print("Error:", e)


def gauss_seidel(matriz, vector, semilla, eps=1e-3, n_itr_max=10):
    n = len(matriz)
    x = semilla[:]
    for itr in range(n_itr_max):
        x_anterior = x[:]
        for i in range(n):
            suma_1 = sum(matriz[i][j] * x[j] for j in range(i))
            suma_2 = sum(matriz[i][j] * x_anterior[j] for j in range(i+1, n))
            x[i] = (vector[i] - suma_1 - suma_2) / matriz[i][i]

        resta = [abs(x[i] - x_anterior[i]) for i in range(n)]
        err = np.linalg.norm(resta)
        if err < eps:
            return x
    raise ValueError("El método de Gauss-Seidel no convergió dentro del número máximo de iteraciones."
                     " Intente con una semilla diferente, cambie la matriz o aumente el número máximo de iteraciones.")


def leer_matriz(n_ec, n_vars):
    while True:
        try:
            entrada = input("Ingrese la matriz cuadrada A (formato: [[a11, a12, ..., a1n], [a21, a22, ..., a2n], ..., [an1, an2, ..., ann]]):\n")
            matriz = ast.literal_eval(entrada)

            if len(matriz) != n_ec or any(len(fila) != n_vars for fila in matriz):
                print(f"Error: La matriz debe tener {n_ec} filas y {n_vars} columnas. Intente de nuevo.")
                continue
            if not isinstance(matriz, list) or any(not isinstance(fila, list) for fila in matriz):
                print("Error: La entrada debe ser una matriz (lista de listas). Intente de nuevo.")
                continue
            return matriz
        except (SyntaxError, ValueError):
            print("Entrada no válida. Asegúrese de ingresar una matriz cuadrada en el formato correcto:")
            print("\n[[2, 3],[5, 1]] para una matriz 2x2 con a11=2, a12=3, a22=1...\n")


def leer_vector(n_ec, nombre):
    while True:
        try:
            entrada = input(f"Ingrese el vector {nombre} (formato: [b1, b2, ..., bn]):\n")
            vector = ast.literal_eval(entrada)

            if len(vector) != n_ec:
                print(f"Error: El vector debe tener {n_ec} elementos. Intente de nuevo.")
                continue
            if not isinstance(vector, list):
                print("Error: La entrada debe ser un vector (lista). Intente de nuevo.")
                continue
            return vector
        except (SyntaxError, ValueError):
            print("Entrada no válida. Asegúrese de ingresar un vector en el formato correcto:")
            print("\n[5, 10] para un vector con b1=5 y b2=10...\n")


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


def verificar_diagonal_dominante(matriz):
    n = len(matriz)
    for i in range(n):
        sum_fila = sum(abs(matriz[i][j]) for j in range(n) if j != i)
        if abs(matriz[i][i]) <= sum_fila:
            return False
    return True


def verificar_diagonal_no_cero(matriz):
    for i in range(len(matriz)):
        if abs(matriz[i][i]) < 1e-12:
            raise ValueError("La matriz tiene ceros en la diagonal.")

if __name__ == "__main__":
    main()