"""Sudoku manipulation classes."""


class Area:
    """Class that defines a area of the Sudoku's grid."""

    def __init__(self, position):
        self.area = []
        self._position = position

    def fill(self, area):
        """Set the area list witha given value."""

        self.area = area
        return self

    @property
    def position(self):
        """Return the line and/or colum position of the area."""

        return self._position

    def validate(self, value):
        """Check if is valid to add the value to this area."""

        if value in self:
            raise ValueError('The value is already in the area.')

    def __getitem__(self, key):
        return self.area[key]

    def __setitem__(self, key, value):
        self.area[key].set_value(value)

    def __contains__(self, item):
        return bool(item in [c.get_value() for c in self.area])


class Line(Area):
    """Class that defines a subarea (line) of the Sudoku's grid."""

    def __str__(self):
        return '| ' + ' | '.join(str(c) for c in self.area) + ' |'


class Column(Area):
    """Class that defines a subarea (column) of the Sudoku's grid."""

    def __str__(self):
        return '\n'.join('| {} |'.format(c) for c in self.area)


class Box(Area):
    """Class that defines a subarea (box) of the Sudoku's grid."""

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
    """Class that defines a Sudoku grid."""

    def __init__(self, grid_data=None):

        self.grid = []
        if grid_data and isinstance(grid_data, list):
            for i, line in enumerate(grid_data):
                self.grid.append(
                    [Cell(i, j, int(v)) for j, v in enumerate(line)]
                )
        else:
            for i in range(0, 9):
                self.grid.append([Cell(i, j) for j in range(0, 9)])

        self.map_grid()
        self.register_validators()

    @property
    def data(self):
        """Return the grid's cells as a matrix (list of lists)."""

        data = []
        for line in self.grid:
            values = [c.get_value() for c in line]
            data.append(values)
        return data

    @property
    def empty_values(self):
        """Return the list of cells that have no value."""

        return len([c in l for l in self.grid for c in l if c.empty])

    def map_grid(self):
        """Map the grid's cells, associating each one with its areas."""

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
        """Register the validators of each area into the cell."""

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

    def __lt__(self, other):
        return bool(self.empty_values < other.empty_values)

    def __gt__(self, other):
        return bool(self.empty_values > other.empty_values)


class Cell:
    """Class that represents a cell of the Sudoku's grid."""

    def __init__(self, posi: int, posj: int, value: int = 0):
        self.validators = []
        self.posi = posi
        self.posj = posj
        self.value = value

    def validate(self, value: int):
        """Call the cell registered validators.

        The registered validators should throw an exception, if necessary.
        """
        for validator in self.validators:
            validator.validate(value)

    @property
    def empty(self):
        """Check if the cell has not an empty value."""

        return not self.value

    def set_value(self, value: int):
        """Setter to value attribute. Validate the value before set it."""

        self.validate(value)
        self.value = int(value)

    def get_value(self):
        """Getter to value attribute."""

        return self.value

    @property
    def possible_values(self):
        """Check which values can be added to the cell."""

        possibilities = []

        if not self.value:
            for i in range(1, 10):
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
