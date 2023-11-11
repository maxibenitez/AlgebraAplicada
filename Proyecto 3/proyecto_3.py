import numpy as np
import os
import sys


def get_equation_vector(matrix, x, y):
    matrix_size = len(matrix)
    zero_matrix = np.zeros((matrix_size, matrix_size))
    possible_changes = [(x, y), (x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1)]
    for entry in possible_changes:
        entry_x = entry[0]
        entry_y = entry[1]
        if len(matrix[0]) > entry_x >= 0 and len(matrix) > entry_y >= 0:
            zero_matrix[entry_y][entry_x] = 1
    equation_vector = zero_matrix.ravel()
    return np.append(equation_vector, matrix[y][x])


def get_equation_system(matrix):
    equation_system = None
    for index_y, B in enumerate(matrix):
        for index_x, _ in enumerate(B):
            if equation_system is None:
                equation_system = get_equation_vector(matrix, index_x, index_y)
            else:
                equation_system = np.vstack((equation_system, get_equation_vector(matrix, index_x, index_y)))
    return equation_system


def forward_elimination(matrix):
    size = len(matrix)
    triangular_matrix = np.copy(matrix).astype(int)
    for i in range(0, size - 1):
        next_row = i + 1
        max_column = abs(triangular_matrix[i:, i])
        where_max = np.argmax(max_column)
        if where_max != 0:
            temp = np.copy(triangular_matrix[i, :])
            triangular_matrix[i, :] = triangular_matrix[where_max + i, :]
            triangular_matrix[where_max + i, :] = temp
        for k in range(next_row, size):
            if triangular_matrix[k, i] == 1:
                triangular_matrix[k, :] = triangular_matrix[k, :] ^ triangular_matrix[i, :]
    return triangular_matrix


def back_substitution(matrix):
    rows, columns = np.shape(matrix)
    x = np.zeros(rows).astype(int)
    for i in range(rows - 1, -1, -1):
        res = matrix[i, -1]
        for j in range(i + 1, columns - 1, 1):
            res ^= matrix[i, j] & x[j]
        x[i] = res
    return x


def system_have_solution(equation_system):
    row_length, columns = np.shape(equation_system)
    for i in range(row_length):
        result = equation_system[i][columns - 1]
        if result == 1:
            have_one = False
            for j in range(columns - 1):
                if equation_system[i][j] == 1:
                    have_one = True
                    break
            if not have_one:
                sys.exit("\n#############¡La Matriz ingresada no tiene solución!#############\n")




def lights_out_solver(initial_matrix):
    equation_system = get_equation_system(initial_matrix)
    triangular_matrix = forward_elimination(equation_system)
    system_have_solution(triangular_matrix)
    solution_vector = back_substitution(triangular_matrix)
    return solution_vector


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


def placeholder_matrix(matrix, row_position):
    clear_console()
    print("Matriz ingresada:\n")
    for i in range(len(matrix)):
        actual_row = matrix[i]
        if i == row_position:
            actual_row = f"> {actual_row} <"
        print(actual_row)


def charge_input_matrix():
    matrix_size = int(input("\nIngrese el tamaño del tablero: "))
    charged_matrix = np.full((matrix_size, matrix_size), "x")
    for i in range(matrix_size):
        for j in range(matrix_size):
            element = -1
            while element not in ["0", "1"]:
                placeholder_matrix(charged_matrix, i)
                element = input(f"\nIngrese el estado de la  (1 = encendidad 0 = apagada) en la posición {i} {j}: ")

            charged_matrix[i][j] = element
            clear_console()
    return charged_matrix


def matrix_logger(matrix):
    for line in matrix:
        print(line)


def solver_logger(initial_game, solution_vector):
    matrix_size = len(initial_game)
    matrix_solution = solution_vector.reshape((matrix_size, matrix_size))

    print("\nMatriz solución:\n")
    matrix_logger(matrix_solution)
    print("\nVector solución:", solution_vector)


def start_game_solution():
    clear_console()
    input_matrix = charge_input_matrix().astype(int)
    print("¡Matriz ingresada con éxito!\n")
    print("Matriz final ingresada:\n")
    matrix_logger(input_matrix)
    start_game = input("\nDesea encontrar la solución de esta matriz? (y = si otro = no): ")
    if start_game != "y":
        sys.exit()
    solution = lights_out_solver(input_matrix)
    solver_logger(input_matrix, solution)


start_game_solution()
