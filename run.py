from state import Cell, CellGrid2D
from agent import *
from environment import GridWorld
from simulator import GridWorldSimulator
import random


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

    policy = CellGrid2D([ # optimal for standard 4x3 world
            env.U, env.U, env.R,
            env.L, env.N, env.R,
            env.L, env.U, env.R,
            env.L, env.N, env.N
            ], Cell(0, 0), Cell(xsize-1, ysize-1))

    # policy = [None] * xsize * ysize # indicates random online policy

    # agent = DirectLearner(policy, discount=1.0)
    # agent = TemporalDifferenceLearner(policy, discount=1.0)
    agent = ADPLearner(policy, discount=1.0)

    sim = GridWorldSimulator(env, agent, do_print=True)
    sim.run(episodes=100, pause=0.0, max_moves=100)


if __name__ == '__main__':
    main()
