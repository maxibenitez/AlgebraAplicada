import numpy as np

def create_equation_system(matrix):
    matrix_size = len(matrix)
    equation_system = None
    
    for index_y, B in enumerate(matrix):
        for index_x, _ in enumerate(B):
            zero_matrix = np.zeros((matrix_size, matrix_size))
            possible_changes = [(index_x, index_y), (index_x + 1, index_y), (index_x, index_y + 1), (index_x - 1, index_y), (index_x, index_y - 1)]
            
            for entry in possible_changes:
                entry_x = entry[0]
                entry_y = entry[1]
                
                if len(matrix[0]) > entry_x >= 0 and len(matrix) > entry_y >= 0:
                    zero_matrix[entry_y][entry_x] = 1
            
            equation_vector = zero_matrix.ravel()
            equation_vector = np.append(equation_vector, matrix[index_y][index_x])
            
            if equation_system is None:
                equation_system = equation_vector
            else:
                equation_system = np.vstack((equation_system, equation_vector))
    
    return equation_system

def gaussian_method(matrix):
    n = matrix.shape[0]
    m = matrix.shape[1]
    
    # Eliminación hacia adelante
    for i in range(n):
        pivot = matrix[i, i]
        if pivot == 0:
            for j in range(i + 1, n):
                if matrix[j, i] != 0:
                    matrix[i, :], matrix[j, :] = matrix[j, :].copy(), matrix[i, :].copy()
                    break
            pivot = matrix[i, i]
        
        for j in range(i + 1, n):
            if matrix[j, i] == 1:
                matrix[j, i:] = (matrix[j, i:] + matrix[i, i:]) % 2
    
    # Sustitución hacia atrás
    last_row = n-1
    last_column = m-1
    solution = np.zeros(n, dtype=int)

    for i in range(last_row, -1, -1):
        solution[i] = matrix[i, -1]
        for j in range(i + 1, last_column, 1):
            solution[i] ^= matrix[i, j] & solution[j]
    
    return solution

def lights_out_solver(initial_state):
    equation_system = create_equation_system(initial_state).astype(int)
    solution_vector = gaussian_method(equation_system)
    return solution_vector

# Ejemplo
initial_state = np.array([[0, 1, 0],
                        [1, 1, 0],
                        [0, 0, 1]])
solution = lights_out_solver(initial_state)
print("Vector solución:", solution)
