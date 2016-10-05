from board import Board
from time import time


def bfs(board):
    start_time = time()

    visited = set()
    queue = [board.START]

    while queue:
        cell = queue.pop(0)
        if cell == board.END:
            return time() - start_time, board.get_path_str(queue, visited)
        for neighbour in board.get_neighbours(cell):
            if neighbour not in visited:
                neighbour.set_parent(cell)
                visited.add(neighbour)
                queue.append(neighbour)
