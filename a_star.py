from board import Board
from cell import Cell
from heapq import heappush, heappop
from time import time


def a_star(board):
    """Calculates shortest path on board using A* alogrithm.
    Args:
        board (Board): Board being the graph the alorithm will use

    Returns:
        Tuple of form (time, string representation of board with path)
    """
    start_time = time()  # Sets start checkpoint for time
    board.START.set_g(0)  # As all cells have g = inf, the first cell is set to 0
    opened = [board.START]  # Initialize priority queue with start cell
    closed = set()  # A set to keep track of notes that have been checked
    while opened:
        cell = heappop(opened)
        if cell is board.END:  # Once cell being check is end cell, we are done
            return time() - start_time, board.get_path_str(opened, closed)
        closed.add(cell)
        for neighbour in board.get_neighbours(cell):
            if neighbour not in closed:
                if neighbour not in opened:  # If neighbour is untouched
                    board.update_neighbour(neighbour, cell)  # Relax and set parent
                    heappush(opened, neighbour)  # Add unchecked cell to be checked out later
                elif neighbour.get_g() > cell.get_g() + neighbour.WEIGHT:  # Already in open, but better path found
                    board.update_neighbour(neighbour, cell)  # Relax and set parent
