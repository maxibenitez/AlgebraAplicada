import numpy as np

def lights_out_solver(initial_state):
    n = len(initial_state)
    
    # Función para verificar si el tablero está apagado
    def is_board_off(board):
        return all(all(cell == 0 for cell in row) for row in board)
    
    # Función para cambiar el estado de las luces adyacentes
    def toggle_lights(board, row, col):
        directions = [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < n and 0 <= new_col < n:
                board[new_row][new_col] = 1 - board[new_row][new_col]
    
    # Función de retroceso para encontrar la solución
    def backtrack(board, row, col):
        if row == n:
            return is_board_off(board), []
        
        next_row, next_col = row, col + 1
        if next_col == n:
            next_row, next_col = row + 1, 0
        
        no_press, no_lights = backtrack(board.copy(), next_row, next_col)
        toggle_lights(board, row, col)
        yes_press, yes_lights = backtrack(board.copy(), next_row, next_col)
        if yes_press:
            yes_lights.append((row, col))
            return yes_press, yes_lights
        return no_press, no_lights
    
    _, lights_to_press = backtrack(initial_state.copy(), 0, 0)
    
    # Genera vector solución
    solution = [1 if (i // n, i % n) in lights_to_press else 0 for i in range(n**2)]
    
    return solution, lights_to_press

# Ejemplo:
initial_state = np.array([[0, 1, 0],
                          [1, 0, 0],
                          [1, 0, 1]])
solution, lights_to_press = lights_out_solver(initial_state)

print("Vector solución:", solution)
print("Luces a presionar:", lights_to_press)
