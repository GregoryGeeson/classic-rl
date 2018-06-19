import time


class Simulator(object):

    def __init__(self, env, agent, initial_state):
        self.env = env
        self.agent = agent
        self.rep = None
        self.initial_state = initial_state

    def run(self, episodes=100, pause=0.0):
        for i in range(episodes):
            print("-- Episode {} --\n".format(i + 1))
            self.episode(pause)

    def episode(self, pause=0.0):
        self.agent.state = self.initial_state
        while not self.agent.done():
            print(self)
            time.sleep(pause)
            self.agent.act()
        print(self)
        time.sleep(pause)


class GridWorldSimulator(Simulator):

    def __init__(self, env, agent, initial_state):
        super().__init__(env, agent, initial_state)
        self.rep = self.env.grid

    def __repr__(self):
        result = ""
        for i in range(len(self.rep)):
            state = self.rep.at_index(i)
            if self.agent.state == state:
                result += "@ "
            elif state.terminal:
                result += "x "
            elif state.accessible:
                result += "o "
            else:
                result += "# "
            if (i + 1) % self.rep.pmax.x == 0:
                result += "\n"
        return result
