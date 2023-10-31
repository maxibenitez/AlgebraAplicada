import numpy as np

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

def lights_out_solver(initial_state):
    equation_system = get_equation_system(initial_state)
    triangular_matrix = forward_elimination(equation_system)
    solution_vector = back_substitution(triangular_matrix)
    return solution_vector

# Ejemplo
initial_state = np.array([[0, 1, 0],
                        [1, 1, 0],
                        [0, 0, 1]])
solution = lights_out_solver(initial_state)
print("Vector solución:", solution)
