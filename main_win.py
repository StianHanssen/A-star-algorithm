from board import Board
from cell import Cell
from bfs import bfs
from a_star import A_star

if __name__ == '__main__':
    board = Board("board-1-2.txt")
    print(board)
    print("\nA* time:", A_star(board), "s\n")

    board = Board("board-2-4.txt")
    print(board)
    print("\nBFS time:", bfs(board), "s\n")
