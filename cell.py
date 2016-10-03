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

    def get_f(self):
        return self.__f

    def get_g(self):
        return self.__g

    def get_h(self):
        return self.__h

    def set_h(self, h):
        self.__h = h

    def set_g(self, f):
        self.__g = g
        self.__f = self.__h + self.__g
