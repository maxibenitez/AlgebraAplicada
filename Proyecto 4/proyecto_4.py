import numpy as np

A = np.array([[0, 1, 0],
              [1, 1, 0],
              [0, 0, 1]])


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


equation_system = None
for index_y, B in enumerate(A):
    for index_x, _ in enumerate(B):
        if equation_system is None:
            equation_system = get_equation_vector(A, index_x, index_y)
        else:
            equation_system = np.vstack((equation_system, get_equation_vector(A, index_x, index_y)))
print(equation_system)
