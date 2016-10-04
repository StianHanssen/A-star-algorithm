from time import time
from board import Board
from math import inf


def bfs(board):
    for cell in board.get_cells():
        cell.set_g(inf)
    board.START.set_g(0)
    start_time = time()

    visited = set([board.START])
    queue = [board.START]
    end = board.END

    while queue:
        node = queue.pop(0)
        if node == end:
            board.print_path()
            return time() - start_time
        for neighbour in board.get_neighbours(node):
            if neighbour not in visited and (neighbour.get_g() > node.get_g() + neighbour.WEIGHT):
                print(queue)
                board.update_neightbour(neighbour, node)
                queue.append(neighbour)
                visited.add(neighbour)

if __name__ == '__main__':
    board = Board("board-1-3.txt", True, True)
    print(board)
    print("BFS time: " + str(bfs(board)))
