import random


class State(object):
    def __init__(self, accessible, terminal):
        self.accessible = accessible
        self.terminal = terminal
        self.reward = 0.0

    def transition(self, change):
        pass


class Cell(State):
    def __init__(self, x, y, accessible=True, terminal=False):
        super().__init__(accessible, terminal)
        self.x = x
        self.y = y

    def __eq__(self, c):
        return self.x == c.x and self.y == c.y

    def __add__(self, c):
        return Cell(self.x + c.x, self.y + c.y)

    def __sub__(self, c):
        return Cell(self.x - c.x, self.y - c.y)

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return "Cell({}, {})".format(self.x, self.y)

    def mul(self, k):
        return Cell(k * self.x, k * self.y)


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

    def random(self):
        state = random.choice(self.grid)
        while state.terminal or not state.accessible:
            state = random.choice(self.grid)
        return state


if __name__ == '__main__':
    d = {(Cell(0, 0), Cell(0, 1)) : 0.04, (Cell(1, 1), Cell(-1, 0)) : 0.5}
    print(d.get((Cell(0, 0), Cell(0, 1))))
    print(d.get((Cell(1, 1), Cell(-1, 0))))
    
