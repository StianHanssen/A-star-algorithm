from board import Board
from cell import Cell
from bfs import bfs
from a_star import a_star
from dijkstra import dijkstra
from math import inf

def averege_time(algorithm, board, cycles):
    time_sum = 0
    for _ in range(cycles):
        new_board = board.clone()
        time_sum += algorithm(new_board)[0]
    return time_sum/cycles

if __name__ == '__main__':
    board_name = "board-1-4.txt"

    board = Board(board_name)
    print(board)
    path = a_star(board)[1]
    time = averege_time(a_star, board, 500)
    print(path)
    print("\nA* time:", time, "s\n")

    board = Board(board_name, default_g=inf, default_h=0)
    print(board)
    path = bfs(board)[1]
    time = averege_time(bfs, board, 500)
    print(path)
    print("\nBFS time:", time, "s\n")

    board = Board(board_name, default_g=inf, default_h=0)
    print(board)
    time = averege_time(dijkstra, board, 500)
    path = dijkstra(board)[1]
    print(path)
    print("\nDijkstra time:", time, "s\n")
