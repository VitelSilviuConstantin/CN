import math
import numpy as np

A = [[1, 2, 1, 1],
    [1, 4, -1, 7],
    [4, 9, 5, 11],
    [1, 0, 6, 4]]


A = [[1.5, 3, 3],
    [2, 6.5, 14],
    [1, 3, 8]]

precision = 10**(-10)

b = [1, 2, 3]

matrix_dim = 3

def read_matrix(file_name):
    A = []
    b = []

    file_handle = open(file_name, "r")

    first_line = file_handle.readline()
    matrix_dim = int(first_line)

    for i in range(matrix_dim):
        string_row = file_handle.readline()
        row = []
        for elem in string_row.split():
            row.append(float(elem))
        A.append(row)

    b_string = file_handle.readline()

    for elem in b_string.split():
        b.append(float(elem))

    return (A, b, matrix_dim)

def print_mat(matrix):
    for line in matrix:
        print(line)

def getColumnElement(i, j, A, A_desc):
    sum = 0

    for t in range(matrix_dim):
        if t == j:
            sum += A_desc[i][t]
        else:
            sum += A_desc[i][t] * A_desc[t][j]

    if math.fabs(A_desc[i][i] > precision):
        u_element = (A[i][j] - sum) / A_desc[i][i]
    else:
        print("Impartire la aproape 0")
        return

    return u_element

def getRowElement(i, j, A, A_desc):
    sum = 0

    for t in range(matrix_dim):
        if t == j:
            sum += A_desc[i][t]
        else:
            sum += A_desc[i][t] * A_desc[t][j]

    l_element = A[i][j] - sum

    return l_element

def getColumnForU(i, A, A_desc):
    for j in range(i):
        A_desc[j][i] = getColumnElement(j, i, A, A_desc)

def getLineForL(i, A, A_desc):
    for j in range(i + 1):
        A_desc[i][j] = getRowElement(i, j, A, A_desc)


def computeAdesc(A, matrix_dim):
    A_desc = []

    for i in range(matrix_dim):
        line = [0] * matrix_dim
        A_desc.append(line)

    for i in range(matrix_dim):
        getColumnForU(i, A, A_desc)
        getLineForL(i, A, A_desc)

    return A_desc

def computeDet(A, matrix_dim):
    det = 1
    for i in range(matrix_dim):
        det = det * A[i][i]

    return det

def getLsolution(A_desc, b, matrix_dim):
    Lsol = [0] * matrix_dim

    for i in range(matrix_dim):
        known_sum = 0
        for j in range(i):
            known_sum += A_desc[i][j] * Lsol[j]

        if math.fabs(A_desc[i][i] > precision):
            Lsol[i] = (b[i] - known_sum) / A_desc[i][i]
        else:
            print("Impartire aproape la 0")

    return Lsol

def getUsolution(A_desc, b, matrix_dim):
    Usol = [0] * matrix_dim

    for i in range(matrix_dim - 1, -1, -1):
        known_sum = 0
        for j in range(matrix_dim - 1, i, -1):
            if i == j:
                known_sum += Usol[j]
            else:
                known_sum += A_desc[i][j] * Usol[j]
        Usol[i] = b[i] - known_sum

    return Usol

def solve(A, b, matrix_dim):
    A_desc = computeAdesc(A, matrix_dim)
    Lsol = getLsolution(A_desc, b, matrix_dim)
    Usol = getUsolution(A_desc, Lsol, matrix_dim)

    return Usol

def compute_norm(A, matrix_dim, sol, result):
    diff_list = [0] * matrix_dim

    for i in range(matrix_dim):
        value = 0
        for j in range(matrix_dim):
            value += A[i][j] * sol[j]

        diff_list[i] = value - result[i]

    norm = math.sqrt(sum([x * x for x in diff_list]))

    return norm

def check_solution(A, matrix_dim, b):
    solution = solve(A, b, matrix_dim)
    norm = compute_norm(A, matrix_dim, solution, b)

    return norm

def solve_with_module(A, b, matrix_dim):
    np_A = np.array(A)
    np_b = np.array(b)

    solution = np.linalg.solve(A, b)
    return solution

def compute_inverse(A):
    np_A = np.array(A)

    try:
        inverse = np.linalg.inv(A)
        return inverse
    except(np.linalg.LinAlgError):
        return []

def show_norms(A, b, matrix_dim):
    solution = solve(A, b, matrix_dim)
    module_solution = solve_with_module(A, b, matrix_dim)

    norm_1_diff = [0] * matrix_dim

    for i in range(matrix_dim):
        norm_1_diff[i] = solution[i] - module_solution[i]

    norm_1 = math.sqrt(sum([x * x for x in norm_1_diff]))

    A_inverse = compute_inverse(A)

    print('Inversa: ')
    print(A_inverse)

    A_inverse_mul_b = np.dot(A_inverse, b)

    norm_2_diff = [0] * matrix_dim

    for i in range(matrix_dim):
        norm_2_diff[i] = solution[i] - A_inverse_mul_b[i]

    norm_2 = math.sqrt(sum([x * x for x in norm_2_diff]))

    print("Norm 1:", norm_1)
    print("Norm 2:", norm_2)


def tema2(A, b, matrix_dim):
    A_desc = computeAdesc(A, matrix_dim)
    print("Matricea descompusa: ")
    print_mat(A_desc)

    print("Determinantul: ")
    print(computeDet(A_desc, matrix_dim))

    computed_solution = solve(A, b, matrix_dim)
    print("Solutia calculata: ")
    print(computed_solution)

    norm = check_solution(A, matrix_dim, b)
    print("Norma: ")
    print(norm)

    show_norms(A, b, matrix_dim)


#A, b, matrix_dim = read_matrix("data.txt")
#tema2(A, b, matrix_dim)

if __name__ == "__main__":
    print("VSK module for sistem solve")