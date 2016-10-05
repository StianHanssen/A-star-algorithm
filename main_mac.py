from board import Board
from cell import Cell
from bfs import bfs
from a_star import A_star


def average_time(algorithm, board, cycles):
    time_sum = 0
    for _ in range(cycles):
        new_board = board.clone()
        time_sum += algorithm(new_board)[0]
    return time_sum / cycles

if __name__ == '__main__':
    board = Board("board-2-3.txt", mac=True, emoji=True)
    print(board)
    path = a_star(board)[1]
    time = average_time(a_star, board, 500)
    print(path)
    print("\nA* time:", time, "s\n")

    board = Board("board-2-3.txt", inf, 0, True, True)
    print(board)
    path = bfs(board)[1]
    time = average_time(bfs, board, 500)
    print(path)
    print("\nBFS time:", time, "s\n")

    board = Board("board-2-3.txt", inf, 0, True, True)
    print(board)
    time = average_time(dijkstra, board, 500)
    path = dijkstra(board)[1]
    print(path)
    print("\nDijkstra time:", time, "s\n")
