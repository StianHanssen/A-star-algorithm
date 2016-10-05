class Cell():
    """An individual cell for Board.

    The cell may have a heuristic value h, a cumuative cost g, a weight as well
    as a parent.
    The weight is how much it cost to travel from any adjacent cell to this cell.
    There is a relation between the symbol and weight of a cell accourding to
    the text given in the exercise.

    Properties:
        WEIGHT (int): Cost for traveling from an adjacent cell to this cell
        SYMBOL (string, chr): The string representation of this cell
        __cells (list): Holds all the cells in board
        X (int): x position of cell in board it is put into
        y (int): y position of cell in borad it is put into
        __parent (cell): Parent of cell
        __g (int): Total weight of path from start cell to this cell
        __h (int): Heuristic value of cell
        __f (int): Value derived by __g + __h

        WEIGHTS (dict): Dictionary used to translate symbol to weight
    """
    WEIGHTS = {'.': 1, '#': None, 'A': 0, 'B': 1, 'w': 100, 'm': 50, 'f': 10, 'g': 5, 'r': 1}

    def __init__(self, x, y, symbol):
        """
        Attributes:
            x (int): x position of cell in board it is put into
            y (int): y position of cell in borad it is put into
            symbol (string, char): Single ascii charater representing cell as string
        """
        self.WEIGHT = Cell.WEIGHTS[symbol]  # Finds weight of cell based on symbol
        self.SYMBOL = symbol
        self.X = x
        self.Y = y
        self.__parent = None
        self.__g = 0
        self.__h = 0
        self.__f = 0

    def __str__(self):
        """Returns:
            A string or char being the symbol representing the cell."""
        return self.SYMBOL

    def __gt__(self, other):
        """Compares cell based on f value, if h is set to 0, then f = g
        Args:
            other (cell): Another cell object you compare to.

        Returns:
            True if this cell has greater f than other, False otherwise.
        """
        return self.__f > other.get_f()

    def get_parent(self):
        return self.__parent

    def get_f(self):
        return self.__f

    def get_g(self):
        return self.__g

    def set_parent(self, parent):
        self.__parent = parent

    def set_h(self, h):
        self.__h = h

    def set_g(self, g):
        self.__g = g
        self.__f = self.__h + self.__g
