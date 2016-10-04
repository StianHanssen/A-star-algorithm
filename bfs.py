from time import time
from board import Board
from heapq import heappush, heappop
from math import inf


def bfs(board):
    start_time = time()
    board.START.set_g(0)
    queue = []
    end = board.END
    heappush(queue, board.START)
    while queue:
        cell = heappop(queue)
        for neighbour in board.get_neighbours(cell):
            if neighbour.get_g() > cell.get_g() + neighbour.WEIGHT:
                board.update_neighbour(neighbour, cell)
                heappush(queue, neighbour)
    return time() - start_time, board.get_path_str()
