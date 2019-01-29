#!/usr/bin/env python3


class Area:
    def __init__(self, position):
        self.area = []
        self._position = position

    def fill(self, area):
        self.area = area
        return self

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

    def __str__(self):
        return '| ' + ' | '.join(str(c) for c in self.area) + ' |'


class Column(Area):

    def __str__(self):
        return '\n'.join('| {} |'.format(c) for c in self.area)


class Box(Area):

    @property
    def position(self):
        i = (self._position // 3) * 3
        j = (self._position % 3) * 3
        return i, j

    def __str__(self):
        l1 = '| ' + ' | '.join(str(c) for c in self.area[:3]) + ' |'
        l2 = '| ' + ' | '.join(str(c) for c in self.area[3:6]) + ' |'
        l3 = '| ' + ' | '.join(str(c) for c in self.area[6:]) + ' |'

        return '\n'.join([l1, l2, l3])


class Grid:
    def __init__(self):

        self.grid = []
        for i in range(0, 9):
            self.grid.append([Cell(i, j) for j in range(0, 9)])

        # Fill lines
        self.lines = [Line(i).fill(l) for i, l in enumerate(self.grid)]


        # Transpose Grid
        cols = []
        for j in range(0, 9):
            cols.append([self.grid[i][j] for i in range(0, 9)])

        # Fill columns
        self.columns = [Column(j).fill(c) for j, c in enumerate(cols)]

        box_list = []
        for box_id in range(0,9):
            box = []
            for v in range(0, 9):
                # position of the box
                start_i = (box_id // 3) * 3
                start_j = (box_id % 3) * 3

                # position inside the box
                relative_i = v // 3
                relative_j = v % 3

                # position inside the grid
                i = start_i + relative_i
                j = start_j + relative_j
                box.append(self.grid[i][j])
            box_list.append(box)

        # Fill boxes
        self.boxes = [Box(i).fill(b) for i, b in enumerate(box_list)]

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
