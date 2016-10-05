from board import Board
from cell import Cell
from heapq import heappush, heappop
from time import time
from math import inf

'''
def dijkstra(board):
    start_time = time()
    board.START.set_g(0)
    opened = [board.START]
    closed = set()
    while opened:
        cell = heappop(opened)
        if cell is board.END:
            return time() - start_time, board.get_path_str()
        closed.add(cell)
        for neighbour in board.get_neighbours(cell):
            if neighbour.WEIGHT is not None and neighbour not in closed:
                if neighbour not in opened:
                    board.update_neighbour(neighbour, cell)
                    heappush(opened, neighbour)
                elif neighbour.get_g() > cell.get_g() + neighbour.WEIGHT:
                    board.update_neighbour(neighbour, cell)
'''

def dijkstra(board):
    start_time = time()
    board.START.set_g(0)
    closed set()
    queue = []
    end = board.END
    heappush(queue, board.START)
    while queue:
        cell = heappop(queue)
        closed.add(cell)
        for neighbour in board.get_neighbours(cell):
            if neighbour.get_g() > cell.get_g() + neighbour.WEIGHT:
                board.update_neighbour(neighbour, cell)
                heappush(queue, neighbour)
    return time() - start_time, board.get_path_str()
