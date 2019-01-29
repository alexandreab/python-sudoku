#!/usr/bin/env python3


class Area:
    def __init__(self, position):
        self.area = []
        self._position = position

    @property
    def position(self):
        return self._position

    def append(self, value):
        if len(self.area) >= 9:
            raise IndexError('The max number of elements allowed is 9')
        self.area.append(value)

    def __getitem__(self, key):
        return self.area[key]

    def __setitem__(self, key, value):
        self.area[key].set_value(value)

    def __contains__(self, item):
        return bool(item in [c.get_value() for c in self.area])


class Line(Area):
    def fill(self):
        self.area = [Cell(self._position, j) for j in range(0, 9)]
        return self

    def __str__(self):
        return ' |'.join(str(c) for c in self.area)


class Column(Area):

    def fill(self):
        self.area = [Cell(i, self._position) for i in range(0, 9)]

    def __str__(self):
        return '\n'.join(str(c) for c in self.area)


class Box(Area):

    def fill(self, start_i, start_j):
        for i in range(start_i, start_i + 3):
            for j in range(start_j, start_j + 3):
                self.area.append(Cell(i, j))

    @property
    def position(self):
        i = (self._position // 3) * 3
        j = (self._position % 3) * 3
        return i, j

    def __str__(self):
        l1 = '|'.join(str(c) for c in self.area[:3])
        l2 = '|'.join(str(c) for c in self.area[3:6])
        l3 = '|'.join(str(c) for c in self.area[6:])

        return '\n'.join([l1, l2, l3])


class Grid:
    def __init__(self):

        # Fill lines
        for i in range(0, 9):
            self.lines = [Line(i).fill() for i in range(0, 9)]

        # Associate columns
        self.columns = [Column(j) for j in range(0, 9)]

        for c in self.columns:
            for i in range(0, 9):
                c.append(self[i][c.position])

        # Associate Boxes
        self.boxes = [Box(i) for i in range(0, 9)]
        for b in self.boxes:
            for v in range(0, 9):
                # position inside the box
                relative_i = v // 3
                relative_j = v % 3
                start_i, start_j = b.position

                # position inside the grid
                i = start_i + relative_i
                j = start_j + relative_j
                b.append(self[i][j])

    def __str__(self):
        return '\n'.join(str(l) for l in self.lines)

    def __getitem__(self, key):
        return self.lines[key]


class Cell:
    def __init__(self, posi, posj, value=0, possible_values=[]):
        self.posi = posi
        self.posy = posj
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
