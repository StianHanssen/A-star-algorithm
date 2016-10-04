class Cell():
    WEIGHTS = {'.': 1, '#': None, 'A': 0, 'B': 1, 'w': 100, 'm': 50, 'f': 10, 'g': 5, 'r': 1}

    def __init__(self, x, y, symbol):
        self.WEIGHT = Cell.WEIGHTS[symbol]
        self.SYMBOL = symbol
        self.X = x
        self.Y = y
        self.__parent = None
        self.__g = 0
        self.__h = 0
        self.__f = 0

    def __str__(self):
        return self.SYMBOL

    def __gt__(self, other):
        return self.__g > other.get_g()

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
