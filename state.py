
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

    def __add__(self, c):
        return Cell(self.x + c.x, self.y + c.y)

    def __sub__(self, c):
        return Cell(self.x - c.x, self.y - c.y)

    def __eq__(self, c):
        return self.x == c.x and self.y == c.y

    def __repr__(self):
        return "Cell({}, {})".format(self.x, self.y)

