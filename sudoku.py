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
            raise IndexError('The max number of elements allowed is 9.')
        self.area.append(value)

    def validate(self, value):
        if value in self:
            raise ValueError('The value is already in the area.')

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
        return '\n'.join([
            '| ' + ' | '.join(str(c) for c in self.area[:3]) + ' |',
            '| ' + ' | '.join(str(c) for c in self.area[3:6]) + ' |',
            '| ' + ' | '.join(str(c) for c in self.area[6:]) + ' |',
        ])


class Grid:
    def __init__(self, grid_data=None):

        self.grid = []
        if grid_data and type(grid_data) is list:
            for i, l in enumerate(grid_data):
                self.grid.append([Cell(i, j, int(v)) for j,v in enumerate(l)])
        else:
            for i in range(0, 9):
                self.grid.append([Cell(i, j) for j in range(0, 9)])

        self.map_grid()
        self.register_validators()

    @property
    def data(self):
        data = []
        for line in self.grid:
            l = [c.get_value() for c in line]
            data.append(l)
        return data

    @property
    def empty_values(self):
        return len([c in l for l in self.grid for c in l if c.empty()])

    def map_grid(self):
        # Fill lines
        self.lines = [Line(i).fill(l) for i, l in enumerate(self.grid)]

        # Transpose Grid
        cols = []
        for j in range(0, 9):
            cols.append([self.grid[i][j] for i in range(0, 9)])

        # Fill columns
        self.columns = [Column(j).fill(c) for j, c in enumerate(cols)]

        box_list = []
        for box_id in range(0, 9):
            box = []
            for value in range(0, 9):
                # position of the box
                start_i = (box_id // 3) * 3
                start_j = (box_id % 3) * 3

                # position inside the box
                relative_i = value // 3
                relative_j = value % 3

                # position inside the grid
                i = start_i + relative_i
                j = start_j + relative_j
                box.append(self.grid[i][j])
            box_list.append(box)

        # Fill boxes
        self.boxes = [Box(i).fill(b) for i, b in enumerate(box_list)]

    def register_validators(self):
        for i, line in enumerate(self.grid):
            for j, cell in enumerate(line):
                box_id = (i - i % 3) + j // 3
                cell.validators = [
                    self.lines[i],
                    self.columns[j],
                    self.boxes[box_id],
                ]

    def __str__(self):
        return '\n'.join(str(line) for line in self.lines)

    def __getitem__(self, key):
        return self.lines[key]

    def __cmp__(self, other):
        return cmp(self.empty_values, other.empty_values)

    def __lt__(self, other):
        return bool(self.empty_values < other.empty_values)


class Cell:
    def __init__(self, posi: int, posj: int, value: int = 0):
        self.validators = []
        self.posi = posi
        self.posj = posj
        self.value = value

    def validate(self, value: int):
        for validator in self.validators:
            validator.validate(value)

    def empty(self):
        if self.value==0:
            return True
        else:
            return False

    def set_value(self, value: int):
        self.validate(value)
        self.value = int(value)

    def get_value(self):
        return self.value

    @property
    def possible_values(self):
        possibilities = []

        if not self.value:
            for i in range(1,10):
                try:
                    self.validate(i)
                    possibilities.append(i)
                except ValueError:
                    continue
        return possibilities

    def __str__(self):
        if self.value:
            return str(self.value)
        return ' '

    def __repr__(self):
        return '{{({},{}): {}}}'.format(self.posi, self.posj, self.value)
