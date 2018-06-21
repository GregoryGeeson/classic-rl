from state import Cell, CellGrid2D


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
        self.model = CellGrid2D( 
                [Cell(i, j) for i in range(pmax.x + 1)
                for j in range(pmax.y + 1)], pmin, pmax)

    def available_actions(self, s):
        actions = [Cell(1, 0), Cell(0, 1), Cell(-1, 0), Cell(0, -1)]
        return [a for a in actions if self.available(s, a)]

    def available(self, s, a):
        return self.model.contains(s + a) and self.model.at(s + a).accessible

    def reverse_of(self, a1, a2):
        return a1 == a2.mul(-1)

    def transition(self, s, a):
        return self.model.at(s + a) if self.available(s, a) else print("Nope")

    def set_cell(self, cell, reward=None, terminal=None, accessible=None):
        if reward is not None:
            self.model.at(cell).reward = reward
        if terminal is not None:
            self.model.at(cell).terminal = terminal
        if accessible is not None:
            self.model.at(cell).accessible = accessible        

    def __repr__(self):
        result = ""
        for i in range(len(self.model)):
            if self.model.at_index(i).terminal:
                result += "x "
            elif self.model.at_index(i).accessible:
                result += "o "
            else:
                result += "# "
            if (i + 1) % self.model.pmax.x == 0:
                result += "\n"
        return result
