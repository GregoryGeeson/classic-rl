import time


class Simulator(object):

    def __init__(self, env, agent, do_print):
        self.env = env
        self.agent = agent
        self.rep = None
        self.indexer = 0
        self.do_print = do_print

    def run(self, episodes=100, pause=0.0, max_moves=100):
        for i in range(episodes):
            print("\n-- Episode {} --\n".format(i + 1))
            self.episode(pause, max_moves)
            # self.agent.update_utilities(i+1, self.indexer)
            print("Utility estimate:")
            print(self.agent.utilities_string(self.indexer))

    def episode(self, pause, max_moves):
        self.agent.reset()
        # self.printout(pause)
        next_state = self.env.model.random()
        count = 0
        while count < max_moves:
            self.agent.update(next_state, self.indexer)
            count += 1
            self.printout(pause, self.agent.action)
            if self.agent.action is None or self.agent.state.terminal:
                break
            else:
                next_state = self.env.transition(
                        self.agent.state, self.agent.action)

    def printout(self, pause, action=None):
        if not self.do_print:
            return
        print("s =", self.agent.state)
        if action is not None:
            print("a =", action)
        print(self)
        if pause > 0:
            time.sleep(pause)


class GridWorldSimulator(Simulator):

    def __init__(self, env, agent, do_print=False):
        super().__init__(env, agent, do_print)
        self.rep = self.env.model
        self.indexer = self.rep.pmax.x

    def __str__(self):
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
