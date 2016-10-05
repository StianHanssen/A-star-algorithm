import os
from math import floor, ceil
from cell import Cell
import emoji as em


class Board():
    """A board representing the text given by exercise.

    Properties:
        __INPUT (tuple): Tuple keeping the exact input, used for clone
        __EMOJI (bool): If set True will allow usage of emojies in visualization
        __cells (list): Holds all the cells in board
        START (Cell): The cell the search algorithm should start at
        END (Cell): The goal of the search algorithm
        BOARD_STR (str): A string representation of board
        WIDTH (int): Width of board
        HEIGHT (int): Height of board
    """
    def __init__(self, file_name, default_g=None, default_h=None, mac=False, emoji=False):
        """
        Attributes:
            file_name (str): Name of the txt we want to import a board from
            default_g (int): A initial g value set for all cells, 0 if None
            default_h (int): A initial h value set for all cells, manhatten if None
            mac (bool): If True will work for mac, works for windows otherwise
            emoji (bool): If set True will allow usage of emojies in visualization
        """
        self.__INPUT = (file_name, default_g, default_h, mac, emoji)
        self.__EMOJI = emoji
        self.__cells = []
        self.START = None
        self.END = None
        self.BOARD_STR = Board.__read_file(Board.__get_board_path(file_name, mac))
        self.WIDTH = self.__find_width()
        self.__gen_cells(self.BOARD_STR)
        self.__set_default_g(default_g)
        self.__set_default_h(default_h)
        self.HEIGHT = ceil(len(self.__cells) / self.WIDTH)

    def __str__(self):
        """Returns:
            A string represening the board."""
        return self.BOARD_STR

    @staticmethod
    def __get_board_path(file_name, mac=False):
        """Gets file path to given file_name, which has to be in the folder boards
        Args:
            file_name (str): Name of the txt we want to import a board from
            mac (bool): If True will work for mac, works for windows otherwise

        Returns:
            A string being the file path to the given filename.
        """
        folder = "/boards/" if mac else "\\boards\\"
        path = os.path.dirname(os.path.abspath(__file__))
        path += folder + file_name
        return path

    @staticmethod
    def __read_file(file_path):
        """Extracts content of a txt file
        Args:
            file_path (str): File path to a txt file

        Returns:
            A string with the contents of the txt file
        """
        with open(file_path) as f:
            read_data = f.read()
        return read_data

    @staticmethod
    def __clean_up(text):
        """Removes any illegal symbols from text
        Args:
            text (str): A string representation of a board

        Returns:
            The cleaned up string
        """
        clean_text = ""
        for c in text:
            if c in Cell.WEIGHTS:
                clean_text += c
        return clean_text

    def __get_heuristic(self, cell):
        """Finds manhatten distance from cell to end cell (END)
        Args:
            cell (Cell): The cell you want to manhatten distance to

        Returns:
            An int represening the manhatten histance between cell and end cell
        """
        diff_x = abs(cell.X - self.END.X)
        diff_y = abs(cell.Y - self.END.Y)
        v = 0
        if diff_x > 0 and diff_y > 0:
            v = 1
        return (abs(cell.X - self.END.X) + abs(cell.Y - self.END.Y)) - v

    def __find_width(self):
        """Finds the width f the board based on the string representation
        Returns:
            An int represening width of the board
        """
        return len(self.BOARD_STR.split("\n")[0])

    def __gen_cells(self, board_string):
        """Creates all the cells in the board.
        Based on the string representation the board will generate cells
        being contained in the board. These are held as a flat list in the
        property __cells. Additionally, it sets the cells that are the start and
        end cell for the algorithm running on the board.

        Args:
            board_string (str): String represenatation of the board
        """
        board_string = Board.__clean_up(board_string)
        for i in range(len(board_string)):
            x = i % self.WIDTH  # Caluclates x value from a flat list
            y = floor(i / self.WIDTH)  # Calculates y value from a flat list
            cell = Cell(x, y, board_string[i])
            self.__cells.append(cell)
            if cell.SYMBOL == 'A':
                self.START = cell
            elif cell.SYMBOL == 'B':
                self.END = cell

    def __set_default_h(self, h):
        """Sets an initial h value for all cells.
        Finds manhatten distance if h is None and set that as h

        Args:
            h (int): Initial h value being set for all cells
        """
        for cell in self.__cells:
            if h is None:
                cell.set_h(self.__get_heuristic(cell))
            else:
                cell.set_h(h)

    def __set_default_g(self, g):
        """Sets an initial g value for all cells.
        Does nothing if g is None, and g is by default 0

        Args:
            g (int): Initial g value being set for all cells
        """
        if g is not None:
            for cell in self.__cells:
                cell.set_g(g)

    def __is_cell(self, x, y):
        """Check if coordinates points to a cell.
        Args:
            x (int): An x position
            y (int): A y position

        Returns:
            True if (x, y) is a valid position on board, False otherwise
        """
        return (x >= 0 and x < self.WIDTH) and (y >= 0 and y < self.HEIGHT)

    def __get_path(self):
        """Gives calcuated by algorithm.
        Will not give a result untill after a search algorithm has been executed.
        Finds path created by algorithm by backtracking from END by looking at
        parents.

        Returns:
            List of valid adjacent cells
        """
        cell = self.END
        path = [(cell.X, cell.Y)]
        while cell.get_parent() is not self.START:
            cell = cell.get_parent()
            path.append((cell.X, cell.Y))
        path.append((self.START.X, self.START.Y))
        path.reverse()
        return path

    def get_cell(self, x, y):
        """Gets a cell at the coordinate (x, y) on the board.
        As it does not check validity of position, __is_cell should check input
        before use.

        Args:
            x (int): An x position on the board
            y (int): A y position on the board

        Returns:
            The cell at the (x, y) position
        """
        return self.__cells[x + y * self.WIDTH]

    def get_cells(self):
        """Gives you all the cells in board

        Returns:
            A flat list containing all the cells in board
        """
        return self.__cells

    def initial_clone(self):
        """Gives you a copy of the intial board before it was edited

        Returns:
            A new board object idential to the inital version of ths board
        """
        file_name, default_g, default_h, mac, emoji = self.__INPUT
        return Board(file_name, default_g, default_h, mac, emoji)

    def get_neighbours(self, cell):
        """Finds adjacent cells to the given cell
        Finds adjacent cells based on moor connectivity that are not walls

        Args:
            cell (Cell): Cell you want to find adjacent cells to

        Returns:
            List of valid adjacent cells
        """
        neighbours = []
        for offset in (1, 0), (-1, 0), (0, 1), (0, -1):
            x, y = cell.X + offset[0], cell.Y + offset[1]
            if self.__is_cell(x, y):
                neighbour = self.get_cell(x, y)
                if neighbour.WEIGHT is not None:  # None meaning a wall
                    neighbours.append(neighbour)
        return neighbours

    def update_neighbour(self, neighbour, cell):
        """Updates a neighbour by setting parent and g.
        Sets cell as parent to neighbour and neightbour's g is set to cells's
        g + weight it costs to travel to neighbour. Ergo total cost of path thus
        far if neighbour is front of the path.

        Args:
            cell (Cell): Cell you want to find adjacent cells to

        Returns:
            List of valid adjacent cells
        """
        neighbour.set_g(cell.get_g() + neighbour.WEIGHT)
        neighbour.set_parent(cell)

    def get_path_str(self, opened=None, closed=None):
        """Gets a string representation of board with path.
        Will not be able to give a result untill after a search alogithm has been
        executed on the board. Will also visualize opened and closed cells if
        given. If opend and/or closed is None, the list being None will not
        be visualized.

        Args:
            opened (list): List containing open cells
            closed (list): List containing closed cells

        Returns:
            String representation of board with path, opened and closed cells
        """
        path = self.__get_path()
        text = list(Board.__clean_up(self.BOARD_STR))
        if closed is not None:
            closed -= {self.START, self.END}
            for c in closed:
                text[c.X + c.Y * self.WIDTH] = 'x'
        if opened is not None:
            opened = set(opened)
            opened -= {self.START, self.END}
            for c in opened:
                text[c.X + c.Y * self.WIDTH] = '*'
        for x, y in path[1:-1]:
            text[x + y * self.WIDTH] = em.emojize(':runner:', use_aliases=True) if self.__EMOJI else "o"
        board = "".join(text)
        path_str = ""
        for i in range(self.HEIGHT):
            path_str += board[i * self.WIDTH: i * self.WIDTH + self.WIDTH] + '\n'
        return path_str[:-1]
        
