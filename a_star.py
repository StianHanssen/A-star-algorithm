from board import Board
from cell import Cell
from heapq import heappush, heappop
from time import time

def A_star(board):
        start_time = time()
        opened = []
        closed = set()
        heappush(opened, (board.START.get_f(), board.START))
        while opened:
            _, cell = heappop(opened)
            closed.add(cell)
            if cell is board.END:
                board.print_path()
                return time() - start_time
            for neighbour in board.get_neighbours(cell):
                if neighbour.WEIGHT is not None and neighbour not in closed:
                    if (neighbour.get_f(), neighbour) in opened:
                        if neighbour.get_g() > cell.get_g() + neighbour.WEIGHT:
                            board.update_cell(neighbour, cell)
                    else:
                        board.update_neightbour(neighbour, cell)
                        heappush(opened, (neighbour.get_f(), neighbour))

if __name__ == '__main__':
    board = Board("board-1-3.txt", True, True)
    print(board)
    time = A_star(board)
    print("\nA* Time:", time, "s")
