from board import Board
from cell import Cell
from heapq import heappush, heappop
from time import time


def a_star(board):
        start_time = time()
        board.START.set_g(0)
        opened = [board.START]
        closed = set()
        while opened:
            cell = heappop(opened)
            if cell is board.END:
                return time() - start_time, board.get_path_str(opened, closed)
            closed.add(cell)
            for neighbour in board.get_neighbours(cell):
                if neighbour.WEIGHT is not None and neighbour not in closed:
                    if neighbour not in opened:
                        board.update_neighbour(neighbour, cell)
                        heappush(opened, neighbour)
                    elif neighbour.get_g() > cell.get_g() + neighbour.WEIGHT:
                        board.update_neighbour(neighbour, cell)
