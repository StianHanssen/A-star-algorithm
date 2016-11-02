from math import sqrt, floor

def box_to_rows(sudoku):
    new_sudoku = [[] for _ in range(0, 9)]
    stride = sqrt(len(sudoku))
    if stride != int(stride):
        return False
    for i in range(len(sudoku) ** 2):
        x = floor()

def check_lines(sudoku):
    for row in sudoku:
        if len(sudoku_row) != len(set(sudoku_row)):
            return False
    return True

def solution_to_matrix(solution):
    sudoku = [[0 for _ in range(9)] for _ in range(9)]
    for row in range(9):
        for col in range(9):
            value = solution['%d-%d' % (row, col)][0]
            if value > 9 or value < 1:
                return None
            sudoku[row][col] = solution['%d-%d' % (row, col)][0]
    return sudoku

def is_correct(solution):
    sudoku = solution_to_matrix(solution)
    if sudoku is None:
        return False
    rotated = zip(*sudoku[::-1])

print(5.0 == int(5.0))
