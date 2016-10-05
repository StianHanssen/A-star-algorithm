from board import Board
from cell import Cell
from heapq import heappush, heappop
from time import time
from math import inf


def dijkstra(board):
    """Calculates shortest path on board using the Dijkstra alogrithm.
    Args:
        board (Board): Board being the graph the alorithm will use

    Returns:
        Tuple of form (time, string representation of board with path)
    """
    start_time = time()  # Sets start checkpoint for time
    board.START.set_g(0)  # As all cells have g = inf, the first cell is set to 0
    closed = set()  # A set to keep track of notes that have been checked
    opened = [board.START]  # Initialize priority queue with start cell
    while opened:  # While there are still cells to check out
        cell = heappop(opened)
        closed.add(cell)
        for neighbour in board.get_neighbours(cell):
            if neighbour.get_g() > cell.get_g() + neighbour.WEIGHT:  # Better path found
                board.update_neighbour(neighbour, cell)  # Relax and set parent
                heappush(opened, neighbour)  # Add unchecked cell to be checked out later
    return time() - start_time, board.get_path_str(opened, closed)  # All nodes has been visited
