#!/usr/bin/env python3

from copy import deepcopy
from queue import LifoQueue, Queue

from sudoku import Grid

class Punter:
    def __init__(self, grid=None):
        self.solved = Queue()
        self.pending = LifoQueue()
        self.pending.put(grid)

    def play(self, max_iter: int = 10000):
        i = 0
        while i<max_iter and not self.pending.empty():
            grid = self.pending.get()
            self.guess(grid)
            i += 1
        return i

    def guess(self, grid):
        cells = [c for l in grid.lines for c in l]
        sorted_cells = sorted(cells, key=lambda c:len(c.possible_values))
        unsolved = []
        for cell in sorted_cells:
            possibles = cell.possible_values
            if not cell.empty():
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
                #data = deepcopy(grid.grid)
                new_grid = Grid(grid.data)
                i = easiest_cell.posi
                j = easiest_cell.posj
                new_grid[i][j] = value
                self.pending.put(new_grid)
