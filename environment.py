from state import Cell


class CellGrid2D(object):

    def __init__(self, grid, pmin=None, pmax=None):
        if pmin is None:
            self.pmin = Cell(0, 0)
        else:
            self.pmin = pmin
        if pmax is None:
            self.pmax = Cell(0, len(grid))
        else:
            self.pmax = pmax
        self.size = self.pmax - self.pmin + Cell(1, 1)
        self.grid = grid

    def at(self, cell):
        return self.grid[self.pmax.x * cell.x + cell.y]

    def at_index(self, i):
        return self.grid[i]

    def contains(self, cell):
        return cell.x >= self.pmin.x \
                and cell.x <= self.pmax.x \
                and cell.y >= self.pmin.y \
                and cell.y <= self.pmax.y

    def __len__(self):
        return len(self.grid)


class Environment(object):

    def __init__(self):
        pass

    def available_actions(self, s):
        """
        Return a list of actions that can be taken from the state s
        """
        pass


class GridWorld(Environment):

    def __init__(self, pmin, pmax):
        """
        Constructor.

        Args:
            grid (list<list<Cell>>): the grid map representation

        """
        super().__init__()
        self.grid = CellGrid2D( 
                [Cell(i, j) for i in range(pmax.x + 1)
                for j in range(pmax.y + 1)], pmin, pmax)

    def available_actions(self, s):
        actions = [Cell(1, 0), Cell(0, 1), Cell(-1, 0), Cell(0, -1)]
        return [a for a in actions if self.available(s, a)]

    def available(self, s, a):
        return self.grid.contains(s + a) and self.grid.at(s + a).accessible

    def transition(self, s, a):
        return self.grid.at(s + a) if self.available(s, a) else print("Nope")

    def set_cell(self, cell, reward=None, terminal=None, accessible=None):
        if reward is not None:
            self.grid.at(cell).reward = reward
        if terminal is not None:
            self.grid.at(cell).terminal = terminal
        if accessible is not None:
            self.grid.at(cell).accessible = accessible        

    def __repr__(self):
        result = ""
        for i in range(len(self.grid)):
            if self.grid.at_index(i).terminal:
                result += "x "
            elif self.grid.at_index(i).accessible:
                result += "o "
            else:
                result += "# "
            if (i + 1) % self.grid.pmax.x == 0:
                result += "\n"
        return result
