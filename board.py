import os
from math import floor, ceil
from cell import Cell

__author__ = 'Stian Hanssen'

class Board():
    def __init__(self, file_name):
        self.__cells = []

        self.START = None
        self.END = None
        self.BOARD_STR = Board.__read_file(Board.__get_board_path(file_name))
        self.WIDTH = Board.__find_width(self.BOARD_STR[0])
        self.HEIGHT = ceil(len(self.__cells) / self.WIDTH)

        self.__gen_cells(self.BOARD_STR)

    def __str__(self):
        return self.BOARD_STR

    @staticmethod
    def __get_board_path(file_name):
        path = os.path.dirname(os.path.abspath(__file__))
        path += "\\boards\\" + file_name
        return path

    @staticmethod
    def __read_file(file_path):
        with open(file_path) as f:
            read_data = f.read()
        return read_data

    @staticmethod
    def __find_width(first_symbol):
        if first_symbol in ('.', "#"):
            return 20
        else:
            return 40

    @staticmethod
    def __clean_up(text):
        clean_text = ""
        for c in text:
            if c in Cell.WEIGHTS:
                clean_text += c
        return clean_text

    def __get_heuristic(self, cell):
        diff_x = abs(cell.X - self.END.X)
        diff_y = abs(cell.Y - self.END.Y)
        v = 0
        if diff_x > 0 and diff_y > 0:
            v = 1
        return (abs(cell.X - self.END.X) + abs(cell.Y - self.END.Y)) - v

    def __gen_cells(self, board_string):
        board_string = Board.__clean_up(board_string)
        for i in range(len(board_string)):
            x = i % self.WIDTH
            y = floor(i / self.WIDTH)
            cell = Cell(x, y, board_string[i])
            self.__cells.append(cell)
            if cell.SYMBOL == 'A':
                self.START = cell
            elif cell.SYMBOL == 'B':
                self.END = cell
        for cell in self.__cells:
            cell.set_h(self.__get_heuristic(cell))

    def __is_cell(self, x, y):
        return x >= 0 and y >= 0 and x < self.WIDTH and y < self.HEIGHT

    def get_cell(self, x, y):
        return self.__cells[x + y * self.WIDTH]

    def get_neighbours(self, cell):
        neighbours = []
        for offset in (1, 0), (-1, 0), (0, 1), (0, -1):
            x, y = cell.X + offset[0], Cell.Y + offset[1]
            if self.__is_cell(x, y):
                neighbour = self.get_cell(x, y)
                if neighbour.WEIGHT is not None:  # None meaning a wall
                    neighbours.append(neighbour)
        return neighbours

    def update_neightbour(self, neighbour, cell):
        neighbour.set_g(cell.g + neighbour.WEIGHT)
        neighbour.parent = cell
