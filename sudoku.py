#!/usr/bin/env python3


class Line:
    def __init__(self, line):
        self.line = [Cell(line,j) for j in range(1, 10)]

    def __str__(self):
        return ' |'.join(str(c) for c in self.line)

    def __getitem__(self, key):
        return self.line[key]

    def __setitem__(self, key, value):
        self.line[key].set_value(value)

    def __contains__(self, item):
        return bool(item in [c.get_value() for c in self.line])

class Grid:
    def __init__(self):
        self.grid = []
        for i in range(1, 10):
            self.grid.append(Line(i))

    def __str__(self):
        return '\n'.join(str(l) for l in self.grid)

    def __getitem__(self, key):
        return self.grid[key]


class Cell:
    def __init__(self, posx, posy, value=0, possible_values=[]):
        self.posx = posx
        self.posy = posy
        self.value = value
        self.possible_values = possible_values

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value

    def __str__(self):
        if self.value:
            return str(self.value)
        else:
            return ' '

    def __repr__(self):
        return self.__str__()
