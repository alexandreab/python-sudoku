"""Sudoku'grids search tree module."""

from queue import PriorityQueue, Queue

from sudoku import Grid


class Searcher:
    """Class that implements methods to find valid sudoku grids."""

    def __init__(self, grid, queue_class=None):
        if not queue_class:
            queue_class = PriorityQueue
        self.solved = Queue()
        self.pending = queue_class()
        self.pending.put(grid)

    def play(self, max_iter: int = 10000):
        """Iterate over possibilites storing valid grids found."""

        i = 0
        while (i < max_iter and
               not self.pending.empty() and
               self.solved.empty()):
            grid = self.pending.get()
            self.search(grid)
            i += 1
        return i

    def search(self, grid):
        """Do a depth first search for valid grid values."""

        cells = [c for l in grid.lines for c in l]
        sorted_cells = sorted(cells, key=lambda c: len(c.possible_values))
        unsolved = []
        for cell in sorted_cells:
            possibles = cell.possible_values
            if not cell.empty:
                continue
            elif possibles == 1:
                cell.set_value(possibles[0])
            else:
                unsolved.append(cell)

        if not unsolved:
            self.solved.put(grid)
        else:
            easiest_cell = unsolved[0]
            for value in easiest_cell.possible_values:
                new_grid = Grid(grid.data)
                i = easiest_cell.posi
                j = easiest_cell.posj
                new_grid[i][j] = value
                self.pending.put(new_grid)
