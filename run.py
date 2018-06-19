from state import Cell
from agent import PassiveGridNavigator
from environment import GridWorld, CellGrid2D
from simulator import GridWorldSimulator


xsize = 4
ysize = 3
goal = Cell(3, 2)
trap = Cell(3, 1)
r_norm = -0.04
r_goal = 1.0
r_trap = -1.0


def main():

    env = GridWorld(Cell(0, 0), Cell(xsize-1, ysize-1))
    for x in range(xsize):
        for y in range(ysize):
            env.set_cell(Cell(x, y), reward=r_norm)
    env.set_cell(goal, terminal=True, reward=r_goal)
    env.set_cell(trap, terminal=True, reward=r_trap)
    env.set_cell(Cell(1, 1), accessible=False)

    policy = CellGrid2D([
            Cell( 0, 1), Cell(0, 1), Cell(1, 0),
            Cell(-1, 0), Cell(0, 0), Cell(1, 0),
            Cell(-1, 0), Cell(0, 1), Cell(1, 0),
            Cell(-1, 0), Cell(0, 0), Cell(0, 0)
            ], Cell(0, 0), Cell(xsize-1, ysize-1))
    agent = PassiveGridNavigator(env, policy)

    sim = GridWorldSimulator(env, agent, Cell(3, 0))
    sim.run(episodes=2, pause=1.0)


if __name__ == '__main__':
    main()
