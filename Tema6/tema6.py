import random
from math import pow, fabs

def read_coef_and_powers(input_file_path):
    input_file_handle = open(input_file_path, "r")
    line = input_file_handle.readline()

    polinom_list = []

    while line:
        line_info = line.split()
        coefficient = float (line_info[0])
        power = int (line.split()[1])
        polinom_list.append((coefficient, power))
        line = input_file_handle.readline()

    return polinom_list

def get_derivative(polinom_info):
    new_polinom = []

    for i in range(len(polinom_info)):
        new_coefficient = polinom_info[i][0] * polinom_info[i][1]
        new_power = polinom_info[i][1] - 1
        new_polinom.append((new_coefficient, new_power))

    if new_polinom[-1][0] == 0:
        new_polinom = new_polinom[:-1]

    return new_polinom


def compute_value(polinom_info, v):
    b = polinom_info[0][0]

    for i in range(len(polinom_info)):
        if i != 0:
            b = polinom_info[i][0] + b * v

        if i < len(polinom_info) - 1:
            for j in range(polinom_info[i][1] - polinom_info[i + 1][1] - 1):
                b = b * v
    return b


def get_next_x(polinom_info, prevx, precision):
    first_derivative = get_derivative(polinom_info)
    second_derivative = get_derivative(first_derivative)

    polinom_value = compute_value(polinom_info, prevx)
    first_derivative_value = compute_value(first_derivative, prevx)
    second_derivative_value = compute_value(second_derivative, prevx)

    ak = first_derivative_value / (polinom_value + precision) - second_derivative_value / (2 * first_derivative_value + precision)

    if ak <= precision:
        xk = prevx
    else:
        xk = prevx - 1 / ak

    return xk

def compute_halley_solution(polinom_info, x, kmax, epsilon):
    onepass = False
    k = 1

    xk = x

    delta = 10

    while (fabs(delta) >= epsilon and k <= kmax and fabs(delta) < pow(10, 8)) or (onepass == False):
        onepass = True
        xk = get_next_x(polinom_info, xk, 0.0000001)

        first_derivative = get_derivative(polinom_info)
        second_derivative = get_derivative(first_derivative)

        polinom_value = compute_value(polinom_info, x)
        polinom_value_xk = compute_value(polinom_info, xk)
        first_derivative_value = compute_value(first_derivative, x)
        second_derivative_value = compute_value(second_derivative, x)

        #print(polinom_value, first_derivative_value, second_derivative_value)

        A = 2 * first_derivative_value * first_derivative_value - polinom_value_xk * second_derivative_value

        if fabs(A) < epsilon:
            break

        delta = polinom_value * first_derivative_value / A
        x = x - delta
        k = k + 1

    return x


def find_solutions(polinom_info):
    a0 = polinom_info[0][0]
    amax = max([elem[0] for elem in polinom_info])
    solutions = []

    R = (fabs(a0) + amax) / fabs(a0)

    for i in range(100):
        xrandom = random.uniform(-R, R)
        solution = compute_halley_solution(polinom_info, xrandom, 100, 0.000000001)

        if fabs(compute_value(polinom_info, solution)) < 0.000001:
            is_present = 0
            for sol in solutions:
                if fabs(sol - solution) < 0.000001:
                    is_present = 1

            if not is_present:
                solutions.append(solution)
                print(xrandom, solution)

    if solutions:
        print("Solutiile sunt: {}".format(solutions))
    else:
        print("No solutions found!")


polinom_info = read_coef_and_powers("polinom.txt")
find_solutions(polinom_info)

